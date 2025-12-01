# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# def etape1_main():
#     print("Exécution de l'étape 1...")
#     # Exemple : lecture d’un fichier ou génération de données
#     data = [1, 2, 3]
#     print("Input data is " + str(data) + ".")
#     return data






# gdf = gpd.read_file("H:/project-2/etape1/SGI_2016_centerlines.shp")
# print(gdf.head())
# print(gdf.columns)
# gdf.plot()



# import fiona 
# from shapely.geometry import shape

# shapefile_path = "H:/project-2/etape1/SGI_2016_centerlines.shp"

# #Ouvrir le shapefile
# with fiona.open(shapefile_path,"r") as src:
#     #boucler sur chaque feature
#     for feature in src:
#         geom = shape(feature["geometry"])  #convertit en shapely
#         # si l'aire est déjà calculée dans 'AREA'
#         area_attr = feature["properties"].get("area_km2")
#         print("Aire (attribut):", area_attr)
#         #si tu veux calculer l'aire avec shapely directement
#         area_calculated = geom.area
#         print("Aire (calculée avec Shapely):",area_calculated)


import geopandas as gpd
import numpy as np
from math import sin
from math import pi



rho = 900        # ice density (kg m^-3)
g = 9.81         # gravitational acceleration (m s^-2)
A = 2.4e-24      # flow rate factor (Pa^-3 s^-1)
n = 3            # Glen's flow law exponent
C = 0.8          # correction factor for valley shape, sliding, etc.


gdf = gpd.read_file("H:/project-2/etape1/flowline_points_step4_input(1).csv")       #Ouvre nos données

alpha_i = gdf['slope_deg'].astype(float)        #récupération de la pente moyenne de la surface le long de la ligne d'écoulement
q_i = gdf['mean_flux_m2a'].astype(float)        #récupération du flux de glace en chaque point



def etape1_main ():
    
    rho = 900        # ice density (kg m^-3)
    g = 9.81         # gravitational acceleration (m s^-2)
    A = 2.4e-24      # flow rate factor (Pa^-3 s^-1)
    n = 3            # Glen's flow law exponent
    C = 0.8  
    
    gdf = gpd.read_file("H:/project-2/etape1/flowline_points_step4_input(1).csv")       #Ouvre nos données

    alpha_i = gdf['slope_deg'].astype(float)        #récupération de la pente moyenne de la surface le long de la ligne d'écoulement
    q_i = gdf['mean_flux_m2a'].astype(float)        #récupération du flux de glace en chaque point
    print("Calcul de l'épaisseur de glace en chaque point...")
    L = []
    for k in range(len(q_i)):                       #boucle pour effectuer le calcul à chaaque point
        h =  ((q_i[k]*(n+2)) / (2*A * (C * rho * g * sin(alpha_i[k]*pi/180))**n ))**(1 / (n + 2))    #calcul de l'épaisseur via la formule donnée
        L.append(h)
    print("Les valeurs d'épaisseurs de glace sont : " + str(L) + ".")
    return L