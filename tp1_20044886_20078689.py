import sys
import random


class Game:
    """
    Classe pour une sous-partie
    """
    def __init__(self, jeu):
        self._jeu = jeu

    def winner(self):
        """
        Retourne le gagnant d'une sous-partie
        si non terminée: 0
        si x gagne: 1
        si o gagne: 2
        si nulle: 3
        :return: état de la partie en int
        """
        # Liste des possibilités de gagner.
        winners = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                   [0, 3, 6], [1, 4, 7], [2, 5, 8],
                   [0, 4, 8], [2, 4, 6]]
        win = 0
        cases_vides = 0
        nulle = 3  # Code pour partie nulle.

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
# End Game Class


class MetaGame:
    """
    Classe pour stocker un jeu de UTT
    """
    def __init__(self, entier):
        self._entier = entier
        self._last = entier >> 162 & 127
        value = entier >> ((80 - self._last) << 1) & 3
        if entier == 0:
            self._player = 1  # Premier coup de la partie, joueur = x.
        else:
            self._player = value ^ 0b11  # Obtenir le joueur courant.

    def get_entier(self):
        return self._entier

    def get_last(self):
        return self._last

    def get_player(self):
        return self._player

    def __str__(self):
        return str(self._entier)

    def winner(self):
        """
        Crée une sous-partie abstraite pour tester si la partie de UTT est terminée
        si non-terminée: 0
        si x gagne: 1
        si o gagne: 2
        si nulle : 3
        :return: état de la partie en int
        """
        meta_tictactoe = 1  # UTT sous forme d'un tictactoe 3x3.
        for i in range(0, 9):
            r = range(0 + i * 9, 9 + i * 9)  # Extraction d'une sous-partie.
            tmp_game = 1  # Entier pour stocker une sous-partie.
            for j in r:
                value = self._entier >> ((80 - j) << 1) & 3
                tmp_game = (tmp_game << 2) + value
            tmpgame = Game(tmp_game)
            value = tmpgame.winner()  # Test chaque sous-partie pour un gagnant.
            value = 0 if value == 3 else value
            meta_tictactoe = (meta_tictactoe << 2) + value

        tmpgame = Game(meta_tictactoe)
        return tmpgame.winner()

    def getInt(self, move):
        """
        Retourne une nouvelle représentation d'une partie suite à un coup joué
        :param move: Position où le coup est joué
        :return: Partie sous forme d'un int
        """
        new_int = (self._player << ((80 - move) << 1)) + self._entier
        new_int &= ~(127 << 162)  # Supprime dernier bit jouer ( 7 1er bits ).
        new_int += (move << 162)
        return new_int

    def possibleMoves(self):
        """
        Retourne les coups possibles pour le joueur courant
        :return: Liste de int représentant les indices
        """
        possible = []
        if self.winner() != 0:  # La partie est deja gagnée.
            return possible

        if self._entier == 0:
            return list(range(0, 81))

        next_case = self._last % 9
        indice_deb = next_case * 9
        range_indice = range(indice_deb, indice_deb + 9)
        tmp_game = 1  # Entier pour stocker une sous-partie.

        for i in range_indice:
            value = self._entier >> ((80 - i) << 1) & 3
            tmp_game = (tmp_game << 2) + value  # Construire une sous-partie.
            if value == 0:
                possible.append(i)  # Garder les coups possibles en mémoire.

        tmpgame = Game(tmp_game)
        if tmpgame.winner() != 0:
            possible = []

        if not possible:  # Il faut jouer dans une autre sous-partie.
            for i in range(0, 9):
                if i == next_case:  # Skip la case analyser precedemment.
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
                winstate = tmpgame.winner()  # Test chaque sous partie pour un gagnant.
                if winstate == 0:  # La sous-partie n'est pas fini, on peut y jouer.
                    possible.extend(tmp_possible)

        return possible

    def OutputBoard(self):
        """
        Imprime la partie pour la lecture humaine
        """
        indicator = 0
        line = ""
        signe = [" . ", " x ", " o ", " ? "]

        for k in range(0, 3):
            for j in range(0, 3):
                for i in range(0, 3):

                    values = []
                    # Valeur des 3 cases d'une ligne d'une petite partie.
                    for ii in range(0,3):
                        value = self._entier >> ((80 - ((indicator + ii) + i * 9)) << 1) & 3
                        values.append(value)

                    slot = indicator + i * 9

                    # Ajoute les 3 cases à notre ligne d'affichage.
                    for ii in range(0, 3):
                        # Vérifie si on affiche le dernier coup jouer.
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
# End MetaGame Class


class Node:
    """
    Classe pour la gestion d'un noeud d'un arbre
    """
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
        """
        Teste un nombre n de partie aléatoire pour générer des statistiques sur les coups possibles
        Une statistique est stockée ainsi:
            [nombre de parties jouées, gagné par x, gagné par o]
        :param n: nombre de partie à jouer pour chaque coup
        :return: Liste de statistiques pour chaque coup
        """
        stats_win = [n, 0, 0]
        possible = self._data.possibleMoves()  # Obtenir les coups possibles de l'adversaire.

        if not possible:
            return 0

        for i in range(0, n):  # Faire n simulation, chaque simulation se fait jusqu'a la fin de la partie.
            tmpmeta = self._data  # Réinitialiser la partie temporaire.
            fin_de_partie = False

            while not fin_de_partie:
                player = tmpmeta.get_player()
                possible = tmpmeta.possibleMoves()

                if not possible:
                    break

                choix_random = random.choice(possible)  # Prendre un coup au hasard.

                tmpmeta = MetaGame(tmpmeta.getInt(choix_random))  # Faire le coup.

                # Teste pour une fin de partie et mise à jour des stats.
                win = tmpmeta.winner()

                if win == player:
                    stats_win[player] += 1
                    break
                elif win == 3:  # La partie est nulle, pas de stats.
                    break

        return stats_win

    def __str__(self):
        return str(self.get_data())
# End Node Class


def p_mode(entier):
    """
    Gère le paramètre p, imprime la partie pour la lecture
    :param entier: partie de UTT sous forme de int
    """
    MetaGame(entier).OutputBoard()


def no_mode(entier):
    """
    Choisis le prochain coup à jouer pour gagner
    :param entier: Partie de UTT sous forme de int
    """
    main_node = Node(MetaGame(entier))
    stats = []
    ratio = []

    coups_possibles = main_node.get_data().possibleMoves()
    for coup in coups_possibles:
        game_possible = MetaGame(main_node.get_data().getInt(coup))
        main_node.add_child(Node(game_possible))

    for child in main_node.get_children():  # Test chaque enfant pour une fin de partie.
        if child.get_data().winner() == main_node.get_data().get_player():  # Le joueur courant gagne.
            print(child.get_data().get_entier())
            sys.exit(0)  # On a trouvé le coup à jouer

    for child in main_node.get_children():  # Construire les stats.
        stats.append(child.sample(1000))

    for i in range(0, len(stats)):
        ratio.append(stats[i][main_node.get_data().get_player()] / stats[i][0])  # Nombre de partie/total.

    best_coup = main_node.get_children()[ratio.index(max(ratio))]  # Choisir le meilleur coup.
    print(best_coup.get_data())


def a_mode(profondeur, entier):
    """
    Gère le paramètre a.
    Imprime les coups possibles selon la profondeur
    :param profondeur: Profondeur de l'arbre à imprimer
    :param entier: Partie de UTT
    """
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
