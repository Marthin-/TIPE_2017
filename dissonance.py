# algorithme de calcul de dissonance
# prenant en argument une liste de fréquences
# ou de notes, et déterminant si l'accord obtenu
# est consonnant ou dissonnant.

# utiliser http://www.mandolintab.net/abcconverter.php pour créer des partitions avec la syntaxe abc

import random

notes = {'la': 440., 'si': 493.883, 'do': 293.665, 're': 311.13, 'mi': 329.628, 'fa': 349.228, 'sol': 391.995}
liste_note = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']
dic_note_vers_abc = {'do': 'c', 're': 'd', 'mi': 'e', 'fa': 'f', 'sol': 'g', 'la': 'a', 'si': 'b'}


def same_freq(f1):
    while f1 < 440:
        f1 *= 2
    while f1 > 880:
        f1 /= 2
    return f1


def frequencificateur(tableau):
    for i in tableau:  # on convertit les notes en fréquences et on les alignes dans la plage  [293.665 ; 493.883]
        if type(i) == str:
            i = conversion(i)
        i = same_freq(i)
    return tableau


def conversion(note):  # ex la3
    hauteur = note[1:]  # découpe la string note en ne gardant que le dernier caractère
    nom = note[:-1]  # découpe en n'enlevant que le dernier caractère
    if hauteur == "1":
        puissance = 1. / 3  # f(do1)=1/4 f(do3)
    elif hauteur == "2":
        puissance = 1. / 2  # f(do2)=1/2 f(do3)
    else:
        puissance = int(hauteur) - 2  # f(do<n>) = 2^n (f(do3))
    frequence = notes[nom] ** int(puissance)
    return frequence


def consonnant(accord):
    tab = frequencificateur(accord)
    for i in tab:
        for j in tab:
            rapport = i / j
            # octave, quinte J, quarte J, tierce M et m et sixte
            if rapport != 1 and rapport != 2 and rapport != 2 ** (7. / 12) and rapport != 2 ** (5. / 12) and rapport != 2 ** (4. / 12) and rapport != 2 ** (3. / 12) and rapport != 2 ** (9. / 12) and rapport != 2 ** (10. / 12):
                return False
    return True


def generer_note(hauteur):
    nom = liste_note[random.randint(0, 6)]  # une note de do à si
    note = str(nom) + str(hauteur)  # par exemple fa2
    return str(note)


# fonction pour générer la partie de basse de notre musique
def generer_basse():
    return generer_note(2)  # 2ème octave pour la ligne de basse


# fonction pour générer la partie mélodique en fonction de la partie de basse
def generer_melodie(basse):
    melodie = [generer_note(random.randint(3, 5)), generer_note(random.randint(3, 5))]
    while consonnant(melodie + [basse]) is False:
        melodie = [generer_note(random.randint(3, 5)), generer_note(random.randint(3, 5))]
    return melodie


def generer_musique():
    basse = []
    melodie1 = []
    melodie2 = []
    for i in range(16):
        if i % 4 == 0:
            basse.append(generer_basse())
        else:
            basse.append(basse[i - 1])
        melodie_double = generer_melodie(basse[i])
        melodie1.append(melodie_double[0])
        melodie2.append(melodie_double[1])
    return [basse, melodie1, melodie2]


def ligne_abc_basse(tableau):
    sortie = " "
    for i in range(16):
        if i % 4 == 0:
            # attention à la syntaxe : On prend la clef du dictionnaire qui correspond à la note sans sa hauteur
            # ex. : dic_note_vers_abc['fa'] au lieu de fa5, pour le convertir simplement en "f"
            sortie += " "
            sortie += dic_note_vers_abc[
                str(tableau[i])[:-1]]  # la ligne de la complication syntaxique d'un homme aux abois
            sortie += "4"
            sortie += " |"
    return str(sortie)


# exemple output :
# >>>  f4 | c4 | e4 | d4 |


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
            sortie += dic_note_vers_abc[
                str(tableau[i])[:-1]]  # la ligne de la complication syntaxique d'un homme aux abois
            sortie += "'" * int(tableau[i][1:] - 2)  # aligne la hauteur avec les apostrophes en abc ( " ' " )
        if i % 2 == 1:
            sortie += " "
        if sortie % 4 == 0:
            sortie += "|"


# exemple output :
# >>> f'c cd | d'e f'z | f'c zd | d'e f'g |

def generer_fichier_abc(triple_table):
    file = open('maPartition.txt', 'w')
    file.write("X:1\nT:Douce Nuit de Printemps sur la Colline\nM:2/4\nC:Francois Gwillou\nQ:1/4=92")
    file.write("V:T1           clef=treble  name=\"Tenore I\"   snm=\"T.I\"")
    file.write("V:T2           clef=treble  name=\"Tenore II\"   snm=\"T.II\"")
    file.write("V:B1  middle=d clef=bass      name=\"Basso I\"    snm=\"B.I\"  transpose=-24")
    file.write("K:C")
    file.write("%On commence la partition")
    file.write("[V:T1]  " + ligne_abc(triple_table[1]) + "|")
    file.write("[V:T2] " + ligne_abc(triple_table[2]) + "|")
    file.write("[V:B1] " + ligne_abc_basse(triple_table[0]) + "|")

    # Début du programme
accord_de_base = ['la3', 'si5', 334]
if consonnant(accord_de_base) is True:
    print("Ca passe trois fois !")
else:
    print("Je l'tenterais pas")
print("Maintenant, on génère une partition !")
mes_trois_voix = generer_musique()
generer_fichier_abc(mes_trois_voix)