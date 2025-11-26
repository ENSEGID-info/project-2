# ============================================
# Interpolation IDW (1/d^2) de l'épaisseur de glace
# avec frontière forcée à 0 m
# ============================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------
# 1. Charger les données de mesure
# --------------------------------------------
data = pd.read_csv("epaisseur_glace.csv")

x = data['longitude'].values
y = data['latitude'].values
z = data['epaisseur_glace'].values

# --------------------------------------------
# 2. Charger la frontière du glacier (contour)
# Le fichier doit contenir : longitude, latitude
# --------------------------------------------
border = pd.read_csv("contour_glacier.csv")

xb = border['longitude'].values
yb = border['latitude'].values
zb = np.zeros_like(xb)   # frontière = épaisseur 0 m

# --------------------------------------------
# 3. Combiner données + frontière
# --------------------------------------------
x_all = np.concatenate([x, xb])
y_all = np.concatenate([y, yb])
z_all = np.concatenate([z, zb])

# --------------------------------------------
# 4. Fonction IDW (Inverse Distance Weighting)
# --------------------------------------------
def idw(x, y, z, xi, yi, power=2):
    """
    Interpolation IDW avec puissance = 2 (1/d²)
    """
    # Distances entre chaque point d'interpolation et les points connus
    dist = np.sqrt((xi[..., None] - x)**2 + (yi[..., None] - y)**2)

    # Éviter div/0 si xi,yi contient un point exact de mesure
    dist[dist == 0] = 1e-12

    # Poids = 1 / d^power
    weights = 1 / dist**power

    # Formule IDW
    zi = np.sum(weights * z, axis=2) / np.sum(weights, axis=2)
    return zi

# --------------------------------------------
# 5. Créer la grille pour interpolation
# --------------------------------------------
xi = np.linspace(x_all.min(), x_all.max(), 200)
yi = np.linspace(y_all.min(), y_all.max(), 200)
xi, yi = np.meshgrid(xi, yi)

# --------------------------------------------
# 6. Interpolation IDW
# --------------------------------------------
zi = idw(x_all, y_all, z_all, xi, yi, power=2)

# --------------------------------------------
# 7. Visualisation
# --------------------------------------------
plt.figure(figsize=(9, 7))
plt.pcolormesh(xi, yi, zi, shading='auto', cmap='coolwarm')
plt.scatter(x_all, y_all, c=z_all, cmap='coolwarm', edgecolor='k', s=40)
plt.colorbar(label="Épaisseur de glace (m)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Interpolation IDW (1/d²) de l'épaisseur de la glace")
plt.show()


