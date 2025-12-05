from numpy import *
import math as m

#e=[4,5,6,7,8,9,4,6,8,2] #données extrapollées lors de l'étape 5 là jsp encore c'est quoi lais le grp de léo est sur le coup

a=[12,11.5,10.5,10,9,8.5,8,7.5,7,6.5] #pentes alpha fictives données par la prof

def epaisseur_fact(n,alpha):
    if alpha<=5:                                       #inutile ici car aucune pente n'est inférieure ou égale à 5 mais si jamais dans le paper ils disent que alpha<=5 c'est de la pente de merde et ne doit pas être prise en compte (variation de hauteur de glace =0)
        return 0
    return pow(m.sin(m.radians(alpha)),(n/(n+2)))       #formule donnée par le paper, alpha en degré


def multiplication_par_epaisseur(n,e):
    r=[]
    for k in range(len(e)):
        t=e[k] * epaisseur_fact(n,a[k])                 
        r.append(t)

    return r

def prise_en_compte_de_la_pente(e):                                      # e est la liste d'épaisseur extrapollé par l'étape 5 IL FAUT QUE CE SOIT UNE LISTE EN 1 DIMENSION sinon on doit repenser le code et c'est le caca boudin
    ef=[]
    l=multiplication_par_epaisseur(3,e)                              #le paper dit que n = 3
    for k in range(len(e)):
        i=e[k]-l[k]
        ef.append(i)
    return ef

def etape3_main(e):
    prise_en_compte_de_la_pente(e)
    