import sys
import random

class Game:
    def __init__(self, jeu):
        self._jeu = jeu

    def winner(self):
        # 0 partie non terminee
        # 1 x gagnant
        # 2 o gagnant
        # 3 partie nulle
        winners = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                   [0, 3, 6], [1, 4, 7], [2, 5, 8],
                   [0, 4, 8], [2, 4, 6]]
        win = 0
        cases_vides = 0
        nulle = 3  # code pour partie nulle

        for i in range(0, 9):
            valeur = self._jeu >> ((8 - i) << 1) & 3
            if valeur == 0:
                cases_vides += 1

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

        return nulle if (cases_vides == 0 and win == 0) else win


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
        value = entier >> ((80 - self._last) << 1) & 3
        self._player = value ^ 0b11  # XOR avec 0b11 pour inverser le player

    def get_entier(self):
        return self._entier

    def get_last(self):
        return self._last

    def get_player(self):
        return self._player

    def __str__(self):
        return str(self._entier)

    def winner(self):
        q = 1
        for i in range(0, 9):
            r = range(0 + i * 9, 9 + i * 9)
            t = 1
            for j in r:
                value = self._entier >> ((80 - j) << 1) & 3
                t = (t << 2) + value
            tmpgame = Game(t)
            value = tmpgame.winner()  # test chaque sous partie pour un gagnant
            value = 0 if value == 3 else value
            q = (q << 2) + value

        # q devient un obj Game, test pour winner
        tmpgame = Game(q)
        return tmpgame.winner()

    def getInt(self, move):
        new_int = (self._player << ((80 - move) << 1)) + self._entier
        new_int &= ~(127 << 162)  ##Supprime dernier bit jouer ( 7 1er bits )
        new_int += (move << 162)
        return new_int
		
		
    def possibleMoves(self):
        possible = []
        if self.winner() != 0:
            return possible
        next_case = self._last % 9
        indice_deb = next_case * 9
        range_indice = range(indice_deb, indice_deb + 9)  # les coups possibles dans le petit tic tac toe
        t = 1

        for i in range_indice:
            value = self._entier >> ((80 - i) << 1) & 3
            t = (t << 2) + value  # construire un petit tic tac toe
            if value == 0:
                possible.append(i)  # garder les coups possibles en memoire

        tmpgame = Game(t)
        if tmpgame.winner() != 0:  # test s'il est possible de jouer dans le petit tic tac toe
            possible = []

        if not possible:  # on peut jouer dans un autre tic tac toe
            for i in range(0, 9):
                if i == next_case:  # skip celui qu'y vient d'etre analyser
                    continue
                r = range(0 + i * 9, 9 + i * 9)
                t = 1
                tmp_possible = []

                for j in r:
                    value = self._entier >> ((80 - j) << 1) & 3
                    t = (t << 2) + value
                    if value == 0:
                        tmp_possible.append(j)

                tmpgame = Game(t)
                winstate = tmpgame.winner()  # test chaque sous partie pour un gagnant
                if winstate == 0:  # la partie n'est pas fini, on peut y jouer
                    possible.extend(tmp_possible)
                else:
                    continue

        return possible

    def OutputBoard(self):
        a = 0  # Mettre plus significatif
        ligne = ""
        signe = [" . ", " x ", " o ", " ? "]

        for k in range(0, 3):
            for j in range(0, 3):
                for i in range(0, 3):

                    # TROUVER BELLE ALTERNATIVE ou plus clair
                    valuea = self._entier >> ((80 - (a + i * 9)) << 1) & 3
                    valueb = self._entier >> ((80 - ((a + 1) + i * 9)) << 1) & 3
                    valuec = self._entier >> ((80 - ((a + 2) + i * 9)) << 1) & 3

                    # TROUVER BELLE ALTERNATIVE (IF ELSE) ou plus clair
                    value = a + i * 9

                    if (value != self._last):
                        ligne += signe[valuea]
                    else:
                        ligne += (signe[valuea]).upper()
                    if (value + 1 != self._last):
                        ligne += signe[valueb]
                    else:
                        ligne += (signe[valueb]).upper()
                    if (value + 2 != self._last):
                        ligne += signe[valuec]
                    else:
                        ligne += (signe[valuec]).upper()

                    ligne += "|"

                print(ligne[:-1])
                ligne = ""
                a += 3
            if k != 2:
                print("-" * 29)
            a += 18


"""
if __name__ == '__main__':

    entier = 459329034283597291728327479273734123420780266358036
    print(bin(entier))
    meta = MetaGame(entier)
    meta.OutputBoard()
    meta.getInt(54)
    meta = MetaGame(meta.getInt(54))
    print(meta.possibleMoves())
"""


class Node:
    def __init__(self, data):
        self._data = data
        self._children = []

    def get_data(self):
        return self._data

    def add_child(self, obj):
        self._children.append(obj)

    def get_children(self):
        return self._children

    def sample(self, n):
        # faire les stats sur le dernier coup joué
        # ex: quels sont les chances de win si on joue sur la case 54
        # le prochain coup est a faire par l'adversaire
        # last = self._data.get_last()

        # structure pour stat [0] nombre total de simulation [1] win de x [2] win de o

        stats_win = [n, 0, 0]
        possible = self._data.possibleMoves()  # get les coups possibles de l'adversaire
        tmpmeta = self._data

        print(self._data.get_last())
        print(self._data.get_player())
        tmpmeta.OutputBoard()

        if not possible:
            return 0

        for i in range(0, n):  # faire n simulation, chaque simulation se fait jusqu'a la fin de la partie
            tmpmeta = self._data
            fin_de_partie = False

            while not fin_de_partie:
                player = tmpmeta.get_player()  # bug : player devient 3 et corrupt la game
                possible = tmpmeta.possibleMoves()

                if not possible:
                    break

                choix_random = random.choice(possible)  # prendre un coup au hasard
                print(possible)
                print("next play: " + str(choix_random) + " by " + str(player))
                tmpmeta = MetaGame(tmpmeta.getInt(choix_random))  # faire le coup
                tmpmeta.OutputBoard()
                # test fin de partie et update stats
                win = tmpmeta.winner()
                print("WIN_STATE: " + str(win))
                print("player: " + str(player))
                if win == player:
                    stats_win[player] += 1
                    print(stats_win)
                    break
                elif win == 3:  # partie est nulle, pas de stats
                    break
            print("new stats")

        #print(self._data.get_last())
        return stats_win

    def __str__(self):
        return str(self.get_data())


class GameTree:
    def __init__(self, root):
        self._root = root

    def get_root(self):
        return self._root

    def print_tree(self):
        print(str(self._root.get_data()))
        line = ""
        for child in self._root.get_children():
            line += str(child.get_data()) + " "
        print(line)

        def root(self):
            return self._root

        def children(self, p):
            p.get_children()

        def breadth_first_print(self):
            ### TO DO : Generer larbre avec X étages
            Q = ArrayQueue()
            Q.enqueue(self.root())
            while not Q.is_empty():
                p = Q.dequeue()
                print(p)
                for c in self.children(p):
                    Q.enqueue(c)


##Queue pour afficher l'arbre de possibilité
class ArrayQueue:
    def __init__(self, capacity=1):
        self._data = [None] * capacity
        self._capacity = capacity
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def enqueue(self):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = elem
        self._size += 1

    def _resize(self, newcapacity):
        old = self._data
        self._data = [None] * newcapacity
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0
        self._capacity = newcapacity

    def dequeue(self):
        if self.is_empty():
            return False
        else:
            elem = self._data[self._front]
            self._data[self._front] = None
            self._front = (self._front + 1) % len(self._data)
            return elem

    def is_empty(self):
        return self._size == 0


# debut programme

"""
def p_mode(entier):
    MetaGame(entier).OutputBoard()

def no_mode(entier):
    ##créer une partie a partir de l'entier
    ##Essait X combinaison de partie jusqua la fin
    ##analyse statistics sortie selon les statistiques (W)
    ##Joue le meilleur coup calculer a ce moment
def a_mode(profondeur,entier):
    ##créer une partie a partir de l'entier
    ##genere un arbre avec la profondeur demandé
    ##afficher l'arbre generer en breadth-first
    ##Fin
entier = 0;

if(sys.argv[1] == "p") :
    p_mode(int(sys.argv[2]))

elif(sys.argv[1] == "a") :
    profondeur = int(sys.argv[2])
    entier = int(sys.argv[3])
    a_mode(profondeur,entier)

else:
    entier = int(sys.argv[1])
    no_mode(entier)
"""

entier = 459329034283597291728327479273734123385595894269204
# 459329034283597291728327479273734123420780266358036 exemple du tp
# 457867532646266388810123794441017840401124333815060 modifié le o en pos 0 pour un x
# 459329034283597291728327479273734123385595894269204 mod 0 en pos 58 en .
#print(int(entier))
# 0b1001110100100100100100010010000000110011010010000010010000100001010010110011010101010000110100010010101010000010000000100011001100110100010100110000001011000010100010100
MAINGAME = MetaGame(entier)
#MAINGAME.OutputBoard()
# arbre avec profondeur de 1
root = Node(MAINGAME)
coups_possibles = root.get_data().possibleMoves()

for coup in coups_possibles:
    game_possible = MetaGame(MAINGAME.getInt(coup))
    root.add_child(Node(game_possible))

# test chaque enfant pour une fin de partie
"""
for child in root.get_children():
    #print(child.get_data().winner())
    #print(child.get_data().get_player())
    if child.get_data().winner() == root.get_data().get_player():  # si le winner est le parent, win
        #print(child.get_data().get_entier())
        #print(bin(child.get_data().get_entier()))
        #print(child.get_data().get_last())
        #child.get_data().OutputBoard()
        break
"""
MAINTREE = GameTree(root)
print("sample")
#print(MAINTREE.get_root().get_children()[0].sample(1))
#for child in MAINTREE.get_root().get_children():
#    print(child.sample(10))
""" bug lorsqu'on joue 2 cases de suite
print(str(MAINGAME.getInt(19)))
t = MetaGame(114414647873514836856224138079674561203278056883476)
t.OutputBoard()
t = MetaGame(t.getInt(20))
print("separator")
t.OutputBoard()
"""