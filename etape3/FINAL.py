# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# =============================================================================
# Etapepepe 1
# =============================================================================

import geopandas as gpd
import numpy as np
from math import sin
from math import pi

rho = 900        # ice density (kg m^-3)
g = 9.81         # gravitational acceleration (m s^-2)
A = 2.4e-24      # flow rate factor (Pa^-3 s^-1)
n = 3            # Glen's flow law exponent
C = 0.8          # correction factor for valley shape, sliding, etc.


gdf = gpd.read_file("H:\projet info/Glacier.csv")       #Ouvre nos données

alpha_i = gdf['slope_deg'].astype(float)        #récupération de la pente moyenne de la surface le long de la ligne d'écoulement
q_i = gdf['mean_flux_m2a'].astype(float)        #récupération du flux de glace en chaque point



def etape1_main ():
    
    rho = 900        # ice density (kg m^-3)
    g = 9.81         # gravitational acceleration (m s^-2)
    A = 2.4e-24      # flow rate factor (Pa^-3 s^-1)
    n = 3            # Glen's flow law exponent
    C = 0.8  
    
    gdf = gpd.read_file("H:\projet info/Glacier.csv")       #Ouvre nos données

    alpha_i = gdf['slope_deg'].astype(float)        #récupération de la pente moyenne de la surface le long de la ligne d'écoulement
    q_i = gdf['mean_flux_m2a'].astype(float)        #récupération du flux de glace en chaque point
    print("Calcul de l'épaisseur de glace en chaque point...")
    L = []
    for k in range(len(q_i)):                       #boucle pour effectuer le calcul à chaaque point
        h =  ((q_i[k]*(n+2)) / (2*A * (C * rho * g * sin(alpha_i[k]*pi/180))**n ))**(1 / (n + 2))    #calcul de l'épaisseur via la formule donnée
        L.append(h)
    print("Les valeurs d'épaisseurs de glace sont : " + str(L) + ".")
    return L

# =============================================================================
# Etaaaaape 2
# =============================================================================

# --- Données connues ---
x_connus = gdf['distance_m'].astype(float)
e_connus = etape1_main ()

# --- Fonction IDW 1D ---
def interpolation_spatiale_1d(P=50, puissance=2):
    x_arr = np.asarray(x_connus, dtype=float)
    e_arr = np.asarray(e_connus, dtype=float)
   
    # Grille d'interpolation
    x_interp = np.linspace(min(x_arr), max(x_arr), P)
   
    # Calcul des distances
    dist = np.abs(x_interp[:, None] - x_arr[None, :])
    dist[dist == 0] = 1e-12
   
    # Poids IDW
    poids = 1.0 / (dist ** puissance)
    poids /= np.sum(poids, axis=1, keepdims=True)
   
    # Interpolation
    e_interp = np.sum(poids * e_arr[None, :], axis=1)
   
    return list(e_interp)  # ← retourne la liste des épaisseurs

# --- Exécution ---
epaisseurs_interpolees = interpolation_spatiale_1d(P=50, puissance=2)

# --- Affichage (optionnel) ---
#print(epaisseurs_interpolees)


# =============================================================================
# EEEEtapeee 3
# =============================================================================

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
            l.append(a[-1])
    return l

e=epaisseurs_interpolees
a=interpolerA(e,gdf['slope_deg'].astype(float))

# =============================================================================
# étapepe intermédiaire
# =============================================================================

#essayons d'interpoler les angles un peu mieux

a_connus = gdf['slope_deg'].astype(float)

def interpolationA2(P=50, puissance=2):
    x_arr = np.asarray(x_connus, dtype=float)
    a_arr = np.asarray(a_connus, dtype=float)
   
    # Grille d'interpolation
    x_interp = np.linspace(min(x_arr), max(x_arr), P)
   
    # Calcul des distances
    dist = np.abs(x_interp[:, None] - x_arr[None, :])
    dist[dist == 0] = 1e-12
   
    # Poids IDW
    poids = 1.0 / (dist ** puissance)
    poids /= np.sum(poids, axis=1, keepdims=True)
   
    # Interpolation
    a_interp = np.sum(poids * a_arr[None, :], axis=1)
   
    return list(a_interp)  # ← retourne la liste des épaisseurs

a2=interpolationA2(P=50, puissance=2)
# =============================================================================
# étaaaaape 3
# =============================================================================
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

# =============================================================================
# Etatatatatapepepepe 4
# =============================================================================

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

élévation=gdf['élévation_m'].astype(float)
def interpolationélévation(P=50, puissance=2):
    x_arr = np.asarray(x_connus, dtype=float)
    é_arr = np.asarray(élévation, dtype=float)
   
    # Grille d'interpolation
    x_interp = np.linspace(min(x_arr), max(x_arr), P)
   
    # Calcul des distances
    dist = np.abs(x_interp[:, None] - x_arr[None, :])
    dist[dist == 0] = 1e-12
   
    # Poids IDW
    poids = 1.0 / (dist ** puissance)
    poids /= np.sum(poids, axis=1, keepdims=True)
   
    # Interpolation
    é_interp = np.sum(poids * é_arr[None, :], axis=1)
   
    return list(é_interp)  # ← retourne la liste des épaisseurs

interpol_élévation=interpolationélévation(P=50, puissance=2)
a2=interpolationA2(P=50, puissance=2)

def graph2(e, a):
    epaisseur_corr = etape3_main(e, a)
    terrain = interpol_élévation
    for i in range(0, len(a)):
        dz = m.tan(m.radians(a[i])) 
        terrain.append(terrain[0] + dz)
        terrain.pop(0)
    glacier_initial = [terrain[k] + e[k]   for k in range(len(e))]
    glacier_corrige = [terrain[b] + epaisseur_corr[b]  for b in range(len(e))]
    x = range(len(e))
    plt.figure(figsize=(14, 6))
    plt.plot(x, terrain, color="olive", linewidth=3, label="Terrain")
    plt.fill_between(
        x, terrain, glacier_corrige,
        color="lightskyblue", alpha=0.5, label="Glacier corrigé"
    )
    plt.plot(x, glacier_initial, color="blue", linewidth=2, label="Glacier initial")

    plt.xlabel("Distance (point n°)")
    plt.ylabel("Altitude")
    plt.title("Profil du glacier ")

    plt.legend()
    plt.grid(True)

    plt.show()
    print(terrain)

    

# =============================================================================
# en +
# =============================================================================

for k in range(5):
    print()
print('les fonctions graph(e,a) et graph2(e,a)  donne les graphiques correspondants à l epaisseur du glacier après toutes les corrections, si l on prend comme variable a2 et non a (quand même e pour l epaisseur), on obtient les même graphes mais avec des angles interpollé par la technique utilisée précèdement pour extrapoller l epaisseur')
























