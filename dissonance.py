# algorithme de calcul de dissonance
# prenant en argument une liste de fréquences
# ou de notes, et déterminant si l'accord obtenu
# est consonnant ou dissonnant.

# utiliser http://www.mandolintab.net/abcconverter.php pour créer des partitions avec la syntaxe abc

import random
import math

notes = {'la': 440., 'si': 493.883, 'do': 261.63, 're': 293.665, 'mi': 329.628, 'fa': 349.228, 'sol': 391.995}
liste_note = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']
dic_note_vers_abc = {'do': 'c', 're': 'd', 'mi': 'e', 'fa': 'f', 'sol': 'g', 'la': 'a', 'si': 'b'}


# Fonction qui ramène une fréquence dans un intervalle [261.63 ; 493.883]
def same_freq(frequence):
    while frequence < 261.63:
        frequence *= 2.
    while frequence > 493.883:
        frequence /= 2.
    return float(frequence)

# Fonction qui convertit une note (ex. la3) en fréquence (ex. 440)
def conversion(note):  # ex la3
    hauteur = note[-1:]  # découpe la string note en ne gardant que le dernier caractère (la hauteur d'octave)
    nom = note[:-1]  # découpe en n'enlevant que le dernier caractère
    if hauteur == "1":
        puissance = 1. / 3  # f(do1)=1/4 f(do3)
    elif hauteur == "2":
        puissance = 1. / 2  # f(do2)=1/2 f(do3)
    else:
        puissance = int(hauteur) - 2  # f(do<n>) = 2^n (f(do3))
    frequence = notes[nom] * (2 ** int(puissance))
    return frequence

# Fonction qui parcourt un tableau de notes/fréquences, le change en tableau de fréquences
# dans un intervalle précis
def frequencificateur(tableau):
    tab = []
    for i in enumerate(tableau):  # on convertit les notes en fréquences et on les alignes dans la plage  [261.63 ; 493.883]
        if str(i[1])[:-1] in liste_note: # si i est une note (ex. fa4), on la convertit en fréquence
            tab.append(conversion(i[1])) # sinon on aligne juste dans l'intervalle
        else:
            tab.append(i[1])
        tab[int(i[0])] = same_freq(tab[i[0]])
    return tab

# Fonction qui vérifie que toutes les notes d'un accord sont consonnantes entre elles
# et retourne True le cas échéant
def consonnant(accord):
    tab = frequencificateur(accord)
    # tableau avec les rapports d'octave, quinte J, quarte J, tierce M et m et sixte
    # Comme les calculs utilisent des floats on aura besoin d'approximer les rapports
    rapports = [1., 2.,  2 ** (7. / 12), 2 ** (5. / 12), 2 ** (4. / 12),  2 ** (3. / 12), 2 ** (9. / 12), 2 ** (10. / 12)]
    final = 0 # compteur pour vérifier avec accord de plus de deux notes
    if len(tab) == 2: # trick pour les accords de deux notes
        final += 1
    for i in range(0,len(tab)):      # on compare les fréquences une à une
        for j in range(0,len(tab)):  # pour valider si leur rapport est consonnant
            if i != j:
                rapport = float(tab[i]) / float(tab[j])
                for rap in rapports:
                    if math.isclose(rap, rapport, abs_tol=1e-3) is True: # la fonction math.isclose() permet d'admettre
                        final += 1                                       # une marge d'erreur sur les calculs de floats
    if final == len(tab): # Si pour chaque note, elle est consonnante par rapport à toutes les autres, retourne True
        return True
    else:
        return False

# Fonction qui crée une note aléatoire (de do à si)
# à une hauteur donnée
def generer_note(hauteur):
    nom = liste_note[random.randint(0, 6)]  # une note de do à si
    note = str(nom) + str(hauteur)  # par exemple fa2
    return str(note)


# Fonction pour générer la partie de basse de notre musique
# utilisant la fonction generer_note()
def generer_basse():
    return generer_note(2)  # 2ème octave pour la ligne de basse


# Fonction pour générer la partie mélodique en fonction de la partie de basse
# pour des raisons de place on génère la mélodie à la troisième octave (hauteur
# "moyenne" mélodique, en utilisant la notation abc. Dans les faits, la note
# est générée à hauteur 2 puis réhaussée d'une octave
def generer_melodie(basse):
    melodie = [generer_note(random.randint(2, 2)), generer_note(random.randint(2, 2))]
    while consonnant(melodie + [basse]) is False:
        melodie = [generer_note(random.randint(2, 2)), generer_note(random.randint(2, 2))]
    return melodie

# Fonction qui génère une liste de trois listes de notes afin de créer une musique
# composée d'accords consonnants
def generer_musique():
    basse = []
    melodie1 = []
    melodie2 = []
    for i in range(16):
        if i % 4 == 0: # On génère une note de la partie de basse tous les quatre temps
            basse.append(generer_basse()) # afin d'alléger la structure musicale
        else:
            basse.append(basse[i - 1])
        melodie_double = generer_melodie(basse[i]) # on génère la mélodie selon la
        melodie1.append(melodie_double[0])         # partie de basse
        melodie2.append(melodie_double[1])
    return [basse, melodie1, melodie2]

# Fonction qui génère une ligne de texte de partition au format abc en convertissant un tableau de notes
def ligne_abc_basse(tableau):
    sortie = " "
    for i in range(16):
        if i % 4 == 0:
            # attention à la syntaxe : On prend la clef du dictionnaire qui correspond à la note sans sa hauteur
            # ex. : dic_note_vers_abc['fa'] au lieu de fa5, pour le convertir simplement en "f"
            sortie += " "
            sortie += dic_note_vers_abc[str(tableau[i])[:-1]]  # la ligne de la complication syntaxique d'un homme aux abois
            sortie += "4"
            sortie += " |"
    return str(sortie)


# exemple output :
# >>>  f4 | c4 | e4 | d4 |

# Fonction qui génère une ligne de texte de partition mélodique au format abc en convertissant un tableau de notes
def ligne_abc(tableau):
    sortie = ""
    for i in range(16):
        if i % 2 == 0:
            sortie += " "
        # attention à la syntaxe : On prend la clef du dictionnaire qui correspond à la note sans sa hauteur
        # ex. : dic_note_vers_abc['fa'] au lieu de fa5, pour le convertir simplement en "f"
        if random.randint(0, 10) == 5:
            sortie += "z"
        else:
            sortie += dic_note_vers_abc[str(tableau[i])[:-1]]  # la ligne de la complication syntaxique d'un homme aux abois
            num = int(tableau[i][-1:]) - 2
            for octave in range(num):
                sortie += "'"  # aligne la hauteur avec les apostrophes en abc ( " ' " )
        if i % 2 == 0:
            sortie += " "
        if i % 4 == 3:
            sortie += "|"
    return sortie


# exemple output :
# >>> f'c cd | d'e f'z | f'c zd | d'e f'g |

# Fonction appelant ligne_abc() et ligne_abc_basse() pour écrire du abc dans un fichier texte
def generer_fichier_abc(triple_table):
    file = open('./maPartition.txt', 'w')
    file.write("X:1\nT:Douce Nuit de Printemps sur la Colline\nM:2/4\nC:Francois Gwillou\nQ:1/4=92\nL:1/4\n")
    file.write("V:T1           clef=treble-8  name=\"Tenore I\"   snm=\"T.I\"\n")
    file.write("V:T2           clef=treble-8  name=\"Tenore II\"   snm=\"T.II\"\n")
    file.write("V:B1  middle=d clef=bass      name=\"Basso I\"    snm=\"B.I\"  transpose=-24\n")
    file.write("K:C\n")
    file.write("%On commence la partition\n")
    file.write("[V:T1]  " + ligne_abc(triple_table[1]) + "|\n")
    file.write("[V:T2] " + ligne_abc(triple_table[2]) + "|\n")
    file.write("[V:B1] " + ligne_abc_basse(triple_table[0]) + "|\n")

# Début du programme
# accord_de_base contient les notes à tester
accord_de_base = ['mi4','sol4']
# on teste la consonnance de notre accord
if consonnant(accord_de_base) is True:
    print("Ca passe trois fois !")
else:
    print("Je l'tenterais pas")
    print(349.228 / 261.63)
print("Maintenant, on génère une partition !")
# voir ligne du dessus
mes_trois_voix = generer_musique()
generer_fichier_abc(mes_trois_voix)
