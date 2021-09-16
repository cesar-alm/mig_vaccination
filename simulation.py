import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import Individu
import vaccin


"""
MIG SANTE - Décembre 2020
Mini Projet Vaccination
Simulation de la vaccination du Covid

Auteurs : Jean-Pierre-Louis Communal, Mathilde Ceripa, Maëlle Thaller, Antoine Poirier & César Almecija

Voir rapport pour avoir d'éventuels détails
"""

"""
Constantes de la simulation :
- N : population totale
- Temps : en jour, de la simulation
- infectes_dep : nombre d'infectés au départ, par catégorie d'âge

- etats_possibles : nombre d'états
- noms_etats : nom des états choisis

- nb_categories : nombre de catégories d'âge (il y a donc en réalité deux fois ce nombre de catégories, en comptant les vaccinés)
- noms_categories : les noms pour les nb_categories*2 catégories totales
- prctage_categories : pourcentages de la population totale pour chacune des nb_categories*2 catégories, à t=0.
- objets_categories : les objets de type Individu correspondant à chacune des nb_categories*2 catégories
- noms_categories_regroupes : les noms des nb_categories d'âges (regroupement vaccinées/non-vaccinés)

- strategie_vaccinale : indique la stratégie choisie, parmi :
  0 : aucune vaccination
  1 : vaccination HAS, centres+ambulatoire
  2 : vaccination HAS, ambulatoire
  3 : vaccination HAS, centres
  4 : vaccination HAS, centres, sans hésitation
  5 : vaccination réelle
  6 : vaccination réelle, sans hésitation
  7 : vaccination réelle, en ajoutant ambulatoire
- noms_strategies : table des noms des stratégies vaccinales
- j0 : jour d'arrivée des vaccins
- seconde_vac : temps avant seconde vaccination
- fin_etape1_amb et al. : temps avant la fin de l'étape 1 de la stratégie de la HAS, en utilisant uniquement la médecine ambulatoire

- vaccins : liste des vaccins disponibles (actuellement un seul vaccin "moyen")

- vaccinables_par_jour et al. : vaccinables par jour selon le mode de vaccination choisi

On utilise les chiffres suivants (qd hesitation vaccinale):
- etape 1 : 5 700 000 à vacciner
- etape 2 : 6 450 000 à vacciner
- etape 3 : 18 600 000 à vacciner
"""

N = 66000000
temps = 365*2
infectes_dep = 10000

patient_rea_reel = [771, 1002, 1297, 1453, 1674, 2080, 2516, 2935, 3351, 3758, 4236, 4592, 5056, 5496, 5940, 6305, 6556, 6723, 6859, 6948, 7004, 7019, 6937, 6875, 6752, 6714, 6690, 6599, 6331, 6139, 5922, 5733, 5644, 5584, 5334, 5127, 4967, 4785, 4641, 4598, 4526, 4392, 4128, 3947, 3819, 3770, 3762, 3639, 3375, 3095, 2911, 2820, 2764, 2728, 2666, 2496, 2385, 2256, 2162, 2091, 2047, 1958, 1854, 1754, 1708, 1664, 1628, 1618, 1572, 1519, 1467, 1395, 1328, 1293, 1287, 1270, 1221, 1179, 1133, 1065, 1030, 1024, 995, 926, 904, 875, 851, 843, 841, 818, 792, 744, 724, 699, 687, 687, 673, 654, 630, 623, 606, 594, 594, 591, 574, 554, 545, 533, 517, 521, 521, 511, 503, 486, 471, 470, 473, 467, 465, 457, 456, 452, 450, 448, 442, 430, 420, 411, 385, 368, 367, 374, 361, 356, 357, 347, 344, 345, 360, 364, 360, 366, 359, 366, 368, 372, 367, 355, 351, 344, 353, 353, 361, 357, 362, 368, 367, 368, 371, 387, 401, 375, 373, 381, 394, 396, 403, 418, 440, 458, 467, 476, 480, 531, 568, 593, 608, 628, 655, 662, 705, 752, 796, 793, 820, 827, 834, 912, 944, 995, 1041, 1092, 1105, 1112, 1158, 1198, 1232, 1259, 1270, 1289, 1335, 1409, 1426, 1416, 1427, 1448, 1465, 1492, 1548, 1642, 1673, 1750, 1800, 1877, 1948, 2099, 2177, 2248, 2319, 2441, 2500, 2584, 2770, 2918, 3045, 3156, 3377, 3452, 3578, 3730, 3878, 4089, 4230, 4331, 4421, 4539, 4690, 4750, 4803, 4899, 4903, 4871, 4896, 4919, 4854, 4775, 4653, 4582, 4509, 4509, 4454, 4289, 4148, 4018, 3883, 3777, 3756, 3751, 3605, 3488, 3425, 3293]

nb_etats = 7
noms_etats = ["Sains", "Incubations", "Contagieux Asympt.", "Contagieux Sympt.", "Reanimations", "Immunisés", "Décès"]

nb_categories = 7*2
noms_categories = ["0-14 non vaccinés", "15-25 non vaccinés", "26-34 non vaccinés", "35-49 non vaccinés", "50-65 non vaccinés", "66-74 non vaccinés", "75+ non vaccinés",
"0-14 vaccinés", "15-25 vaccinés", "26-34 vaccinés", "35-49 vaccinés", "50-65 vaccinés", "66-74 vaccinés", "75+ vaccinés"]
prctage_categories = np.array([17.8, 11.8, 11.5, 19.1, 19.2, 11.2, 9.4, 0, 0, 0, 0, 0, 0, 0])/100
objets_categories = []
noms_categories_regroupes = ["0-14", "15-25", "26-34", "35-49", "50-65", "66-74", "75+"]

strategie_vaccinale = 7
j0 = 365 +14
noms_strategies = ["aucune vaccination, j0=" + str(j0), "vaccination centres+ambulatoire, j0=" + str(j0), "vaccination ambulatoire, j0=" + str(j0), "vaccination centres, j0=" + str(j0), "vaccination centres sans hésitation, j0=" + str(j0), "vaccination réelle", "vaccination sans hésitation vaccinale", "vaccination réelle + ambulatoire"]
seconde_vac = 0

vaccinables_par_jour_ambulatoire = 150000
vaccinables_par_jour_centres = 200000
vaccinables_par_jour_tot = vaccinables_par_jour_ambulatoire + vaccinables_par_jour_centres
vaccinables_par_jour_vrai = 70000
vaccinables_par_jour_vrai_plusamb = vaccinables_par_jour_vrai + vaccinables_par_jour_ambulatoire

fin_etape1_amb = 38
fin_etape2_amb = 81
fin_etape3_amb = 205

fin_etape1_centres = 28
fin_etape2_centres = 60
fin_etape3_centres = 153

fin_etape1_tout = 16
fin_etape2_tout = 35
fin_etape3_tout = 88

fin_etape1_nohes_centres = 69
fin_etape2_nohes_centres = 134
fin_etape3_nohes_centres = 321

fin_etape1_vrai = 5700000/vaccinables_par_jour_vrai
fin_etape2_vrai = fin_etape1_vrai + 6450000/vaccinables_par_jour_vrai
fin_etape3_vrai = fin_etape2_vrai + 18600000/vaccinables_par_jour_vrai

fin_etape1_vrai_plusamb = 5700000/vaccinables_par_jour_vrai_plusamb
fin_etape2_vrai_plusamb = fin_etape1_vrai_plusamb + 6450000/vaccinables_par_jour_vrai_plusamb
fin_etape3_vrai_plusamb = fin_etape2_vrai_plusamb + 18600000/vaccinables_par_jour_vrai_plusamb

fin_etape1_vrai_nohes = 2*fin_etape1_vrai
fin_etape2_vrai_nohes = fin_etape1_vrai_nohes + 2*(6450000/vaccinables_par_jour_vrai)
fin_etape3_vrai_nohes = fin_etape2_vrai_nohes + 2*(18600000/vaccinables_par_jour_vrai)

vaccins = []


def etatVaccination(t):
    """
    Nombre de personnes vaccinées par jour, si provision

    Retourne un tableau de taille nb_categories qui contient, pour chaque catégorie de population, le nombre de personnes vaccinées par jour

    Basé sur la constante strategie_vaccinale :
    0 : aucune vaccination
    1 : vaccination HAS, centres+ambulatoire
    2 : vaccination HAS, ambulatoire
    3 : vaccination HAS, centres
    4 : vaccination HAS, centres, sans hésitation
    5 : vaccination réelle
    6 : vaccination réelle, sans hésitation

    Rappel de la stratégie de la HAS (simplification avec uniquement les tranches d'âge, sans prendre en compte les à risque, personnels, etc.):
    - Etape 1 = On vaccine en premier les catégories de population 5 & 6 (65+)
    - Etape 2 = On vaccine ensuite la catégorie 4 (50-65)
    - Etape 3 = On vaccine enfin 1, 2 & 3 (15+)

    On considère que le jour de lancement de la stratégie de vaccination correspond à j0 + seconde_vac, ie le temps mis avant que les secondes
    vaccinations ne soient distribuées (ralentit donc le processus)
    """

    tableau_vaccination = np.zeros( (nb_categories,) )

    if strategie_vaccinale == 0:
        return tableau_vaccination

    jour_lancement = j0 + seconde_vac

    fin_etape1 = 0
    fin_etape2 = 0
    fin_etape3 = 0
    vaccinables_par_jour = 0

    if strategie_vaccinale == 1:
        fin_etape1 = fin_etape1_tout
        fin_etape2 = fin_etape2_tout
        fin_etape3 = fin_etape3_tout
        vaccinables_par_jour = vaccinables_par_jour_tot

    if strategie_vaccinale == 2:
        fin_etape1 = fin_etape1_amb
        fin_etape2 = fin_etape2_amb
        fin_etape3 = fin_etape3_amb
        vaccinables_par_jour = vaccinables_par_jour_ambulatoire

    if strategie_vaccinale == 3:
        fin_etape1 = fin_etape1_centres
        fin_etape2 = fin_etape2_centres
        fin_etape3 = fin_etape3_centres
        vaccinables_par_jour = vaccinables_par_jour_centres

    if strategie_vaccinale == 4:
        fin_etape1 = fin_etape1_nohes_centres
        fin_etape2 = fin_etape2_nohes_centres
        fin_etape3 = fin_etape3_nohes_centres
        vaccinables_par_jour = vaccinables_par_jour_centres

    if strategie_vaccinale == 5:
        fin_etape1 = fin_etape1_vrai
        fin_etape2 = fin_etape2_vrai
        fin_etape3 = fin_etape3_vrai
        vaccinables_par_jour = vaccinables_par_jour_vrai

    if strategie_vaccinale == 6:
        fin_etape1 = fin_etape1_vrai_nohes
        fin_etape2 = fin_etape2_vrai_nohes
        fin_etape3 = fin_etape3_vrai_nohes
        vaccinables_par_jour = vaccinables_par_jour_vrai

    if strategie_vaccinale == 7:
        fin_etape1 = fin_etape1_vrai_plusamb
        fin_etape2 = fin_etape2_vrai_plusamb
        fin_etape3 = fin_etape3_vrai_plusamb
        vaccinables_par_jour = vaccinables_par_jour_vrai_plusamb

    if 0 <= t < jour_lancement:
        # Pas encore de vaccin
        return tableau_vaccination

    if jour_lancement <= t < jour_lancement + fin_etape1:
        # Vaccin, étape 1
        tableau_vaccination[5] = vaccinables_par_jour * 0.46
        tableau_vaccination[6] = vaccinables_par_jour * 0.54
        return tableau_vaccination
    elif jour_lancement + fin_etape1 <= t < jour_lancement + fin_etape2:
        # Vaccin étape 2
        tableau_vaccination[4] = vaccinables_par_jour
        return tableau_vaccination
    elif jour_lancement + fin_etape2 <= t < jour_lancement + fin_etape3:
        # Vaccin étape 3
        tableau_vaccination[1] = vaccinables_par_jour * 0.3
        tableau_vaccination[2] = vaccinables_par_jour * 0.29
        tableau_vaccination[3] = vaccinables_par_jour * 0.41
        return tableau_vaccination
    
    return tableau_vaccination

def etatReglementation(t):
    """
    Donne l'état de la réglementation au temps t
    0 si aucune réglementation
    1 si confinement
    2 si gestes barrieres
    """

    if 0 <= t <70:
        return 0
    elif 70 <= t < 132:
        return 1
    elif 132 <= t < 232:
        return 2
    elif 232 <= t < 302:
        return 0
    elif 302 <= t < 335:
        return 1
    elif 335 <= t < 365:
        return 2
    elif 410 <= t < 470:
        return 1

    return 0


def initialiserObjets():
    """
    Instancie les objets Individu (nb_categories*2) et Vaccin (un seul) dont la simulation a besoin 
    """
    vaccins.append(vaccin.Vaccin())

    for age in range(nb_categories//2):
        objets_categories.append(Individu.Individu(age, None))

    for age in range(nb_categories//2, nb_categories):
        objets_categories.append(Individu.Individu(age, vaccins[0]))



def conditionsInitiales():
    """
    Conditions initiales, assez arbitraires
    """
    ci = np.zeros( (nb_categories * nb_etats) )

    for categorie in range(nb_categories//2):
        ci[categorie*nb_etats] = N*prctage_categories[categorie] - infectes_dep
        ci[categorie*nb_etats + 1] = infectes_dep
    
    return ci





def fonction(x, t):
    '''
    Fonction utilisée pour la résolution, permettant de calculer dx/dt en fonction de x et t
    où :
         0     1     2      3      4       5       6         7
    x = (s(t), i(t), ca(t), cs(t), rea(t), imm(t), dead(t)), vaccine(t)

    et ceci nb_categories*2 fois
    '''

    resultat = np.zeros( (nb_etats * nb_categories,) )

    #On calcule le nombre de personnes vivantes à l'instant t
    alive = np.sum(x)
    for categorie in range(nb_categories):
        alive -= x[categorie * nb_etats + 6]

    for categorie in range(nb_categories):
        #On récupère les infos de l'individu dont il est question dans cette catégorie
        individu = objets_categories[categorie]
        individu.confinement = etatReglementation(t)
        petit_beta = individu.beta()
        
        beta = np.empty( (nb_categories, nb_categories) )
        beta[:nb_categories//2,:nb_categories//2] = petit_beta
        beta[nb_categories//2:,:nb_categories//2] = petit_beta
        beta[:nb_categories//2,nb_categories//2:] = petit_beta
        beta[nb_categories//2:,nb_categories//2:] = petit_beta

        #Les données à l'instant t
        s = x[nb_etats * categorie + 0]
        inf = x[nb_etats * categorie + 1]
        ca = x[nb_etats * categorie + 2]
        cs = x[nb_etats * categorie + 3]
        rea = x[nb_etats * categorie + 4]
        imm = x[nb_etats * categorie + 5]

        # En vue de calculer la variation des futurs infectés,
        # on veut une matrice colonne de nb_categories lignes, qui à chaque ligne a ca + cs de la catégorie en question
        contamines = np.zeros((nb_categories,))
        for categorie2 in range(nb_categories):
            contamines[categorie2] = x[nb_etats * categorie2+ 2] + x[nb_etats * categorie2+ 3]
            
        # Combien de personnes faut-il vacciner par jour à t ?
        a_vacciner = etatVaccination(t)[categorie % (nb_categories//2) ]

        # vaut 1 si cette catégorie est vaccinée, -1 sinon
        epsilon = (categorie >= (nb_categories // 2))*2 - 1

        # On calcule la variation de personnes infectés dans cette catégorie à t
        infectes = 0
        if alive != 0:
            infectes = beta.dot(contamines)[categorie] * (s / alive)

        # On calcule la variation des personnes qui perdent leur immunité
        perte_immunite = individu.k() * individu.l() * imm


        if categorie >= nb_categories//2:
            # On est dans une catégorie de vaccinés.
            # On enlève aux sains de cette catégorie les infectés (habituel)
            # On ajoute aux sains de cette catégorie ceux qui viennent de se faire vacciner
            # On ajoute aux sains de la catégorie correspondante non vaccinée ceux qui perdent l'immunité vaccinale
            resultat[nb_etats * categorie + 0] += - infectes + epsilon * a_vacciner
            resultat[nb_etats * (categorie % (nb_categories//2))] += perte_immunite
        else:
            # On est dans une catégorie de non-vaccinés
            # On enlève aux sains de cette catégorie les infectés (habituel)
            # On enlève aux sains de cette catégorie ceux qui viennent de se faire vacciner
            # On ajoute aux sains de cette catégorie ceux qui perdent l'immunité
            resultat[nb_etats * categorie + 0] += - infectes + epsilon * a_vacciner + perte_immunite
        

        # Calculs selon les équa diffs
        resultat[nb_etats * categorie + 1] += infectes - individu.b() * inf
        resultat[nb_etats * categorie + 2] += individu.c() * individu.b() * inf - individu.d() * ca
        resultat[nb_etats * categorie + 3] += (1 - individu.c()) * individu.b() * inf - (individu.e + individu.h()) * individu.f() * cs - (1 - individu.e - individu.h()) * individu.d() * cs
        resultat[nb_etats * categorie + 4] += individu.e * individu.f() * cs - individu.g() * individu.i() * rea - (1 - individu.g()) * individu.j() * rea
        resultat[nb_etats * categorie + 5] += individu.d() * ca + (1 - individu.e - individu.h()) * individu.d() * cs + (1-individu.g()) * individu.j() * rea - perte_immunite
        resultat[nb_etats * categorie + 6] += individu.h() * individu.f() * cs + individu.g() * individu.i() * rea


    return np.array(resultat)


def afficher(y, t):
    """
    Fonction pour afficher ce qui est intéressant
    """
    # On affiche un bilan général, état par état indépendamment de la catégorie
    for i in range(nb_etats):
        result = np.sum(y[:, i::nb_etats], axis = 1)
        plt.plot(t, result, label = noms_etats[i], linewidth=3)
    
    plt.title("Etats de la population française (" + noms_strategies[strategie_vaccinale] + ")")
    plt.xlabel("Temps (jours)")
    plt.ylabel("Nombre de personnes")
    plt.legend()
    plt.figure()


    # On affiche les pourcentages de réanimation par catégorie
    total = np.sum(y[:,4::nb_etats], axis=1)

    for categorie in range(nb_categories//2):
        plt.plot(t, (y[:,categorie*nb_etats + 4] + y[:,(categorie + nb_categories//2)*nb_etats + 4]) / total,
                    label=noms_categories_regroupes[categorie], linewidth=3)
    
    plt.legend()
    plt.title("Pourcentage des patients en réanimation par âge (" + noms_strategies[strategie_vaccinale] + ")")
    plt.xlabel("Temps (jours)")
    plt.ylabel("Pourcentage")
    plt.figure()


    # On affiche le nombre de réanimations par catégorie
    for categorie in range(nb_categories//2):
       plt.plot(t, y[:,categorie*nb_etats + 4] + y[:,(categorie + nb_categories//2)*nb_etats + 4],
                   label=noms_categories_regroupes[categorie], linewidth=3)
    plt.plot(t, total, label="Total", linewidth=3)
    # plt.plot(t[78:340], patient_rea_reel, label = "Chiffres réels", linewidth = 3)
    
    plt.legend()
    plt.title("Nombre de patients en réanimation (" + noms_strategies[strategie_vaccinale] + ")")
    plt.xlabel("Temps (jours)")
    plt.ylabel("Nombre de personnes")
    plt.figure()

    # On affiche juste le total des réanimations
    plt.plot(t, total, label="Total", linewidth=4)

    plt.legend()
    plt.title("Nombre de patients en réanimation (" + noms_strategies[strategie_vaccinale] + ")")
    plt.xlabel("Temps (jours)")
    plt.ylabel("Nombre de personnes")
    plt.axes().set_ylim(None, 8000)
    plt.grid(True)
    plt.figure()


    # On affiche le nombre de réa, selon si vacciné ou non
    for v in range(2):
        plt.plot(t,
            np.sum(y[:, v*nb_etats*(nb_categories // 2) + 4:(v+1)*nb_etats*(nb_categories // 2) + 4:nb_etats],
                axis=1),
            label= ("Non vacciné" if (v == 0) else "Vacciné"),
            linewidth=3)
    plt.plot(t, total, label = "Total", linewidth = 3)
    plt.legend()
    plt.xlabel("Temps (jours)")
    plt.ylabel("Nombre de personnes")
    plt.title("Réanimations en fonction de la vaccination (" + noms_strategies[strategie_vaccinale] + ")")
    plt.figure()
    

    # On affiche le nombre de vaccinés par catégorie
    for categorie in range(nb_categories//2, nb_categories):
        plt.plot(t,
            np.sum(y[:, categorie*nb_etats:(categorie+1)*nb_etats], axis = 1),
            label=(noms_categories[categorie] + " (tous états)"),
            linewidth = 3)
    plt.plot(t, np.sum(y[:, nb_etats*nb_categories//2:], axis = 1), label = "Total", linewidth = 3)
    plt.title("Nombre de vaccinés par âge (tous états confondus) (" + noms_strategies[strategie_vaccinale] + ")")
    plt.xlabel("Temps (jours)")
    plt.ylabel("Nombre de personnes")
    plt.legend()
    plt.figure()
    
    
    # On affiche, état par état, les différentes catégories de la population française
    for etat in range(1):
        for categorie in range(nb_categories):
            label = noms_etats[etat] + " de la catégorie " + noms_categories[categorie]
            plt.plot(t, y[:, categorie*nb_etats + etat], label = label)
        titre = noms_etats[etat] + " par catégorie de la population française"
        plt.title(titre)
        plt.legend()
        plt.figure()

    plt.show()


def corriger(y):
    for ligne in range(y.shape[0]):
        for colonne in range (y.shape[1]):
            if y[ligne, colonne] < 0:
                y[ligne, colonne] = 0

    return y

def resolution():
    """
    Initialise, résout et affiche
    """
    initialiserObjets()
    ci = conditionsInitiales()

    t = np.linspace(0,temps,temps)
    y = odeint(fonction,ci,t)

    y = corriger(y)
    
    afficher(y, t)


resolution()