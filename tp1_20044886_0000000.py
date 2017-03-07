import sys


class Game:
    def __init__(self,jeu):
        self._jeu = jeu

    def winner(self):
        winners = [[0,1,2], [3,4,5], [6,7,8],
                   [0,3,6], [1,4,7], [2,5,8],
                   [0,4,8], [2,4,6]]
        win = 0
        for winning_case in winners:  # check if x wins
            count = 0
            for j in winning_case:
                valeur = self._jeu >> ((8 - j) << 1) & 3
                if valeur == 1:
                    count += 1
                if count == 3:
                    win = 1
                    return win

        for winning_case in winners:  # check if o wins
            count = 0
            for j in winning_case:
                valeur = self._jeu >> ((8 - j) << 1) & 3
                if valeur == 2:
                    count += 1
                if count == 3:
                    win = 2
                    return win
        return win

"""
if __name__ == '__main__':

    r = range(45, 54)
    entier = 459329034283597291728327479273734123420780266358036
    t = 1
    for i in r:
        value = entier >> ((80 - i) << 1) & 3
        t = (t << 2) + value
        print(str(bin(t)))

    testGame = Game(t)
    print(testGame.winner())

"""


class MetaGame:
    def __init__(self, entier):
        self._entier = entier
        self._last = entier >> 162 & 127
        self._Player = (entier >> ((80 - self._last) << 1) & 3) ^ 0b11 # XOR avec 0b11 pour inverser le player

    def get_entier(self):
        return self._entier

    def get_last(self):
        return self._last

    def winner(self):
        q = 1
        for i in range(0, 9):
            r = range(0 + i*9, 9 + i*9)
            t = 1
            for j in r:
                value = self._entier >> ((80 - j) << 1) & 3
                t = (t << 2) + value
            tmpgame = Game(t)
            value = tmpgame.winner()  # test chaque sous partie pour un gagnant
            q = (q << 2) + value

        # q devient un obj Game, test pour winner
        tmpgame = Game(q)
        return tmpgame.winner()

    def getInt(self,move):
        tmp = (self._Player << ((80 - move) << 1)) + self._entier
        tmp &= 11692013098647223345629478661730264157247460343807  # remove 7 premiers bits avec un masque de 162bits
        tmp += move << 162  # padding de 0 et combinaison
        return tmp

    def possibleMoves(self):
        possible = []

if __name__ == '__main__':

    entier = 459329034283597291728327479273734123420780266358036
    print(bin(entier))
    meta = MetaGame(entier)
    print(meta._Player)
    meta.getInt(56)


class Node:
    def __init__(self,data):
        self._data = data
        self._children = []

    def add_child(self, obj):
        self._children.append(obj)


class GameTree:
    def __init__(self, root):
        self._root = root

    def __str__(self):
        return "tree"


# debut programme

#entier = sys.argv[0]

#METAGAME = MetaGame(entier)

