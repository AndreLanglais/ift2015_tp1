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

        for winning_case in winners:
            count_x = 0
            count_o = 0
            for j in winning_case:
                valeur = self._jeu >> ((8 - j) << 1) & 3
                if valeur == 1:
                    count_x += 1
                elif valeur == 2:
                    count_o += 1
                if count_x == 3:
                    win = 1
                    return win
                if count_o == 3:
                    win = 2
                    return win

        return nulle if (cases_vides == 0 and win == 0) else win


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
        meta_tictactoe = 1  # UTT sous forme d'un tictactoe 3x3
        for i in range(0, 9):
            r = range(0 + i * 9, 9 + i * 9)  # extraction d'une sous-partie
            tmp_game = 1  # entier pour stocker une sous-partie
            for j in r:
                value = self._entier >> ((80 - j) << 1) & 3
                tmp_game = (tmp_game << 2) + value
            tmpgame = Game(tmp_game)
            value = tmpgame.winner()  # test chaque sous-partie pour un gagnant
            value = 0 if value == 3 else value
            meta_tictactoe = (meta_tictactoe << 2) + value

        # meta_tictactoe devient un obj Game, test pour winner
        tmpgame = Game(meta_tictactoe)
        return tmpgame.winner()

    def getInt(self, move):
        new_int = (self._player << ((80 - move) << 1)) + self._entier
        new_int &= ~(127 << 162)  # Supprime dernier bit jouer ( 7 1er bits )
        new_int += (move << 162)
        return new_int

    def possibleMoves(self):
        possible = []
        if self.winner() != 0:  # la partie est deja gagnée
            return possible

        if self._entier == 0:
            for i in range(0, 81):
                possible.append(i)
            return possible

        next_case = self._last % 9
        indice_deb = next_case * 9
        range_indice = range(indice_deb, indice_deb + 9)
        tmp_game = 1  # entier pour stocker une sous-partie

        for i in range_indice:
            value = self._entier >> ((80 - i) << 1) & 3
            tmp_game = (tmp_game << 2) + value  # construire un petit tic tac toe
            if value == 0:
                possible.append(i)  # garder les coups possibles en memoire

        tmpgame = Game(tmp_game)
        if tmpgame.winner() != 0:
            possible = []

        if not possible:  # Il faut jouer dans une autre sous-partie.
            for i in range(0, 9):
                if i == next_case:  # Skip la case analyser precedemment
                    continue
                r = range(0 + i * 9, 9 + i * 9)
                tmp_game = 1
                tmp_possible = []

                for j in r:
                    value = self._entier >> ((80 - j) << 1) & 3
                    tmp_game = (tmp_game << 2) + value
                    if value == 0:
                        tmp_possible.append(j)

                tmpgame = Game(tmp_game)
                winstate = tmpgame.winner()  # test chaque sous partie pour un gagnant
                if winstate == 0:  # la partie n'est pas fini, on peut y jouer
                    possible.extend(tmp_possible)

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

                    if value != self._last:
                        ligne += signe[valuea]
                    else:
                        ligne += (signe[valuea]).upper()
                    if value + 1 != self._last:
                        ligne += signe[valueb]
                    else:
                        ligne += (signe[valueb]).upper()
                    if value + 2 != self._last:
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


def p_mode(entier):
    MetaGame(entier).OutputBoard()


def no_mode(entier):
    # créer une partie a partir de l'entier
    # Essait X combinaison de partie jusqua la fin
    # analyse statistics sortie selon les statistiques (W)
    # Joue le meilleur coup calculer a ce moment
    main_tree = GameTree(Node(MetaGame(entier)))
    stats = []
    ratio = []

    coups_possibles = main_tree.get_root().get_data().possibleMoves()
    for coup in coups_possibles:
        game_possible = MetaGame(main_tree.get_root().get_data().getInt(coup))
        main_tree.get_root().add_child(Node(game_possible))

    # test chaque enfant pour une fin de partie
    for child in main_tree.get_root().get_children():
        #print(child)
        if child.get_data().winner() == main_tree.get_root().get_data().get_player():  # si le winner est le parent, win
            print(child.get_data().get_entier())
            # print(bin(child.get_data().get_entier()))
            # print(child.get_data().get_last())
            # child.get_data().OutputBoard()
            sys.exit(0)

    # aucun enfant ne termine la partie, constuire les stats
    i = 0
    for child in main_tree.get_root().get_children():
        print(i)
        i += 1
        stats.append(child.sample(1000))

    print(stats)
    # choisir meilleure stat
    for i in range(0, len(stats)):
        ratio.append(stats[i][main_tree.get_root().get_data().get_player()] / stats[i][0])  # nombre de partie/total

    # get le best coup a jouer
    best_coup = main_tree.get_root().get_children()[ratio.index(max(ratio))]
    print(best_coup.get_data())


def a_mode(profondeur,entier):
    # créer une partie a partir de l'entier
    # genere un arbre avec la profondeur demandé
    # afficher l'arbre generer en breadth-first
    # Fin
    rootgame = MetaGame(entier)
    child = [rootgame]
    next_child = []
    printer = ""

    for i in range(0,profondeur+1):
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

