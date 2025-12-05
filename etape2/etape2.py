import pandas as pd

# Charger les points de mesure
data = pd.read_csv("epaisseur_glace.csv")

x = data['longitude'].values
y = data['latitude'].values
z = data['epaisseur_glace'].values

import numpy as np

# Définir la grille spatiale
xi = np.linspace(x.min(), x.max(), 200)
yi = np.linspace(y.min(), y.max(), 200)
xi, yi = np.meshgrid(xi, yi)

from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# Interpolation (choisir 'linear', 'cubic', ou 'nearest')
zi = griddata((x, y), z, (xi, yi), method='cubic')

plt.figure(figsize=(8,6))
plt.pcolormesh(xi, yi, zi, shading='auto', cmap='coolwarm')
plt.scatter(x, y, c=z, edgecolor='k', cmap='coolwarm')
plt.colorbar(label="Épaisseur de glace (m)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Interpolation spatiale de l'épaisseur de la glace (cubic)")
plt.show()