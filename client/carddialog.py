from itertools import combinations
from PyQt4.QtGui import QDialog, QListWidget, QListWidgetItem, QDialogButtonBox, QHBoxLayout, QVBoxLayout
from common.board import Card

class CardDialog(QDialog):
    def __init__(self, cards, parent = None):
        super(CardDialog, self).__init__(parent)
        cardList = QListWidget()
        units = ("Infantry", "Cavalry", "Artillery", "Wild")
        cardToIndex = {}
        for i, c in enumerate(cards):
            label = "%d: %s: %s" % (i, c.territory.name, units(c.unit))
            cardList.addItem(label)
            cardToIndex[c] = i
        combinationList = QListWidget()
        combinationList.currentItemChanged.connect(self.__setCombination)
        combinationList.itemDoubleClicked.connect(self.__setCombination)
        combinationList.itemDoubleClicked.connect(self.accepted)
        self.combinations = {}
        for combo in combinations(cards, 3):
            if [c.unit for c in combo] in Card.validCombinations:
                indexes = [cardToIndex[c] for c in combo]
                label = "%d, %d, %d" % tuple(indexes)
                combinationList.addItem(label)
                self.combinations[label] = indexes
        listLayout = QHBoxLayout()
        listLayout.addWidget(cardList)
        listLayout.addWidget(combinationList)

        layout = QVBoxLayout()
        layout.addLayout(listLayout)
        layout.addWidget(QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, accepted=self.accepted, rejected=self.rejected))

        self.setLayout(layout)

    def __setCombination(self, current, previous = None):
        if current:
            self.combination = self.combinations[current.text()]
