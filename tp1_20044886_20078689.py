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
##End Game Class

class MetaGame:
    def __init__(self, entier):
        self._entier = entier
        self._last = entier >> 162 & 127
        value = entier >> ((80 - self._last) << 1) & 3
        if entier == 0:
            self._player = 1  # premier coup de la partie, joueur = x
        else:
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
        new_int &= ~(127 << 162)  # Supprime dernier bit jouer ( 7 1er bits )
        new_int += (move << 162)
        return new_int

    def possibleMoves(self):
        possible = []
        if self.winner() != 0:
            return possible

        if self._entier == 0:
            return list(range(0, 81))

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
        indicator = 0
        line = ""
        signe = [" . ", " x ", " o ", " ? "]

        for k in range(0, 3):
            for j in range(0, 3):
                for i in range(0, 3):

                    values = []
                    ## valeur des 3 cases d'une ligne d'une petite partie
                    for ii in range(0,3):
                        value = self._entier >> ((80 - ((indicator + ii) + i * 9)) << 1) & 3
                        values.append(value)

                    slot = indicator + i * 9

                    ##ajoute les 3 cases à notre ligne d'affichage
                    for ii in range(0, 3):
                        ## vérifie si on affiche le dernier coup jouer
                        if slot + ii != self._last:
                            line += signe[values[ii]]
                        else:
                            line += (signe[values[ii]]).upper()

                    line += "|"

                print(line[:-1])
                line = ""
                indicator += 3
            if k != 2:
                print("-" * 29)
            indicator += 18
##End MetaGame Class

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

        if not possible:
            return 0

        for i in range(0, n):  # faire n simulation, chaque simulation se fait jusqu'a la fin de la partie
            tmpmeta = self._data
            fin_de_partie = False

            while not fin_de_partie:
                player = tmpmeta.get_player()
                possible = tmpmeta.possibleMoves()

                if not possible:
                    break

                choix_random = random.choice(possible)  # prendre un coup au hasard

                tmpmeta = MetaGame(tmpmeta.getInt(choix_random))  # faire le coup

                # test fin de partie et update stats
                win = tmpmeta.winner()

                if win == player:
                    stats_win[player] += 1
                    break
                elif win == 3:  # partie est nulle, pas de stats
                    break

        return stats_win

    def __str__(self):
        return str(self.get_data())
##End Node Class



##Function for p parameter
def p_mode(entier):
    MetaGame(entier).OutputBoard()

##Function for no parameter
def no_mode(entier):
    main_node = Node(MetaGame(entier))
    stats = []
    ratio = []

    coups_possibles = main_node.get_data().possibleMoves()
    for coup in coups_possibles:
        game_possible = MetaGame(main_node.get_data().getInt(coup))
        main_node.add_child(Node(game_possible))

    # test chaque enfant pour une fin de partie
    for child in main_node.get_children():
        # print(child)
        if child.get_data().winner() == main_node.get_data().get_player():  # si le winner est le parent, win
            print(child.get_data().get_entier())
            # print(bin(child.get_data().get_entier()))
            # print(child.get_data().get_last())
            # child.get_data().OutputBoard()
            sys.exit(0)

    # aucun enfant ne termine la partie, constuire les stats
    for child in main_node.get_children():
        stats.append(child.sample(1000))

    print(stats)
    # choisir meilleure stat
    for i in range(0, len(stats)):
        ratio.append(stats[i][main_node.get_data().get_player()] / stats[i][0])  # nombre de partie/total

    # get le best coup a jouer
    best_coup = main_node.get_children()[ratio.index(max(ratio))]
    print(best_coup.get_data())
##end no_mode Function


##Function for a parameter
def a_mode(profondeur, entier):
    rootgame = MetaGame(entier)
    child = [rootgame]
    next_child = []
    printer = ""

    for i in range(0, profondeur + 1):
        for game in child:
            printer += str(game.get_entier()) + " "

            for move in game.possibleMoves():
                next_child.append(MetaGame(game.getInt(move)))

        print(printer)
        child = next_child
        next_child = []
        printer = ""


entier = 0

if sys.argv[1] == "p":
    p_mode(int(sys.argv[2]))

elif sys.argv[1] == "a":
    profondeur = int(sys.argv[2])
    entier = int(sys.argv[3])
    a_mode(profondeur, entier)

else:
    entier = int(sys.argv[1])
    no_mode(entier)

# entier = 459329034283597291728327479273734123385595894269204
# 459329034283597291728327479273734123420780266358036 exemple du tp
# 457867532646266388810123794441017840401124333815060 modifié le o en pos 0 pour un x
# 459329034283597291728327479273734123385595894269204 mod 0 en pos 58 en .
