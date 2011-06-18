from PyQt4.QtCore import pyqtSignal, Qt, QObject, QByteArray, QDataStream, QCoreApplication
from PyQt4.QtNetwork import QTcpSocket

class Message(object):
    (
        Pong,
        RequestState,
        Join,
        Rejoin,
        RequestPlayerList,
        RequestChatHistory,
        RequestName,
        ChangeName,
        ChangeColor,
        SendChat,
        SendWhisper,
    ) = range(11)

    (
        Ping,
        CurrentState,
        JoinSuccess,
        NameTaken,
        NameAccepted,
        BeginPlayerList,
        PlayerInfo,
        EndPlayerList,
        PlayerJoined,
        PlayerLeft,
        ColorChanged,
        NameChanged,
        NameChangeSuccess,
        ReceiveChat,
        ReceiveWhisper,
    ) = range (100, 115)
        
    validArgs = {
        Pong: (),
        RequestState: (),
        CurrentState: (),
        Join: (),
        RequestPlayerList: (),
        RequestChatHistory: (),
        RequestName: (str,),
        Rejoin: (str,),
        ChangeName: (str,),
        ChangeColor: (int, int, int),
        SendChat: (str,),
        SendWhisper: (str, int),
        
        Ping: (),
        CurrentState: (),
        NameTaken: (),
        JoinSuccess: (),
        NameAccepted: (str,),
        BeginPlayerList: (),
        PlayerInfo: (str, int, int, int),
        EndPlayerList: (),
        PlayerJoined: (str,),
        PlayerLeft: (str,),
        ColorChanged: (str, int, int, int),
        NameChanged: (str, str),
        NameChangeSuccess: (str,),
        ReceiveChat: (str, str),
        ReceiveWhisper: (str, str),
    }

    @staticmethod
    def argMatch(msg, args):
        try:
            valid = Message.validArgs[msg]
            for i, a in enumerate(args):
                if not type(a) == valid[i]:
                    return False
        except:
            return False
        return True

class Connection(QTcpSocket):
    socketError = pyqtSignal(int)
    closed = pyqtSignal(QObject)
    connectionFailed = pyqtSignal()
    messageSent = pyqtSignal(int, list)
    messageReceived = pyqtSignal(int, list)

    def __emitError(self, err):
        if err == self.RemoteHostClosedError:
            self.done()
            return
        self.socketError.emit(int(err))

    def done(self):
        self.closed.emit(self)
        self.valid = False
        self.moveToThread(QCoreApplication.instance().thread())

    def __init__(self, id = None, parent = None):
        QTcpSocket.__init__(self, parent)
        self.valid = True
        if id:
            if not self.setSocketDescriptor(id):
                self.done()
                return
            self.id = id
        self.player = None
        self.setSocketOption(self.LowDelayOption, True)
        self.error.connect(self.__emitError, Qt.DirectConnection)
        self.readyRead.connect(self.receiveMessage, Qt.DirectConnection)
        
    def tryConnectToHost(self):
        self.abort()
        self.connectToHost(self.host, self.port)
        if not self.waitForConnected(10000):
            self.connectionFailed.emit()

    def waitForBytes(self, n):
        while self.bytesAvailable() < n:
            if not self.waitForReadyRead(10000):
                self.done()

    def sendMessage(self, msg, args, id = None):
        if id:
            if self.socketDescriptor() != id:
                return
        data = QByteArray()
        stream = QDataStream(data, self.WriteOnly)
        stream.writeInt32(msg)
        for arg in args:
            if type(arg) == str:
                stream.writeInt32(len(arg))
                stream.writeRawData(arg)
            elif type(arg) == int:
                stream.writeInt32(arg)
        self.write(data)
        self.messageSent.emit(msg, args)

    def receiveMessage(self):
        stream = QDataStream(self)
        self.waitForBytes(4)
        msg = stream.readInt32()
        argTypes = Message.validArgs[msg]
        args = []
        for aType in argTypes:
            if aType == str:
                self.waitForBytes(4)
                length = stream.readInt32()
                self.waitForBytes(length)
                args.append(stream.readRawData(length))
            elif aType == int:
                self.waitForBytes(4)
                args.append(stream.readInt32())        
        self.messageReceived.emit(msg, args)
        if self.bytesAvailable() > 0:
            self.readyRead.emit()

