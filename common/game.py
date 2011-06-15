class State(object):
    (
        OutOfSync,
        Lobby,
        ChoosingOrder,
        InitialPlacement,
        InitialDraft,
        Draft,
        Attack,
        AttackerRoll,
        DefenderRoll,
        Fortify,
        GameOver,
    ) = range(11)

class Action(object):
    (
        AddPlayer,
        RemovePlayer,
        StartGame,
        RollDice,
        ExchangeCards,
        PlaceTroops,
        Attack,
        Retreat,
        EndAttack,
        Fortify,
        EndTurn,
     ) = range(11)

    validArgs = {
        AddPlayer: (str, int),
        RemovePlayer: (str),
        StartGame: (),
        RollDice: (),
        ExchangeCards: (int, int, int),
        PlaceTroops: (str, int),
        Attack: (str, str, int),
        Retreat: (),
        EndAttack: (),
        Fortify: (str, str, int),
        EndTurn: (),
    }

    @staticmethod
    def argMatch(action, args):
        try:
            valid = Action.validArgs[action]
            for i, a in enumerate(args):
                if not type(a) == valid[i]:
                    return False
        except:
            return False
        return True
