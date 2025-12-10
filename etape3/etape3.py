from numpy import *
import math as m

def interpolerA(e,a):
    le=len(e)
    la=len(a)
    l=[]
    if la<=le:
        d=le//la
        for k in a:
            for i in range(d):
                l.append(k)
        while len(l)<len(e):
            l.append(e[-1])
    return l

e=etape1_main()
a=interpolerA(e,[12,11.5,10.5,10,9,8.5,8,7.5,7,6.5])

def epaisseur_fact(n,alpha):
    if alpha<=5:                                       #inutile ici car aucune pente n'est inférieure ou égale à 5 mais si jamais dans le paper ils disent que alpha<=5 c'est de la pente de merde et ne doit pas être prise en compte (variation de hauteur de glace =0)
        return 0
    return pow(m.sin(m.radians(alpha)),(n/(n+2)))       #formule donnée par le paper, alpha en degré


def multiplication_par_epaisseur(n,e,a):
    r=[]
    for k in range(len(e)):
        t=e[k] * epaisseur_fact(n,a[k])                 
        r.append(t)
    return r

def prise_en_compte_de_la_pente(e,a):                                      # e est la liste d'épaisseur extrapollé par l'étape 5 IL FAUT QUE CE SOIT UNE LISTE EN 1 DIMENSION sinon on doit repenser le code et c'est le caca boudin
    ef=[]
    l=multiplication_par_epaisseur(3,e,a)                              #le paper dit que n = 3
    for k in range(len(e)):
        i=e[k]-l[k]
        ef.append(i)
    return ef

def etape3_main(e,a):
    return prise_en_compte_de_la_pente(e,a)

import matplotlib.pyplot as plt


def graph(e,a):
    epaisseur_corr = etape3_main(e,a)
    effet_pente = [e[i] - epaisseur_corr[i] for i in range(len(e))]

    x = range(len(e))

    plt.figure(figsize=(len(e), 6))

    plt.plot(x, e, label="Épaisseur initiale extrapolée", marker="o")
    plt.plot(x, epaisseur_corr, label="Épaisseur corrigée (pente)", marker="o")
    plt.plot(x, effet_pente, label="Effet de la pente", linestyle="--")

    plt.xlabel("Point n°")
    plt.ylabel("Épaisseur")
    plt.title("Effet de la pente sur l'épaisseur de glace")
    plt.legend()
    plt.grid(True)

    plt.show()