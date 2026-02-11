import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

# Paramètres
size = 50
n_steps = 100
proie_rep = 0.2
seuil_reproduction_predateur = 10
duree_vie_max1 = 15
duree_vie_max2 = 25
seuil_predateurs_bas = 50
boost_reproduction = 0.8

# Initialisation
proies = np.random.choice([0, 1], size*size, p=[0.7, 0.3]).reshape(size, size)  # 30% de proies
predateurs = np.where(proies == 1, 0, np.random.choice([0, 2], size=(size, size), p=[0.98, 0.02]))  # 2% de prédateurs
proies_mangees = np.zeros((size, size))  # Compteur de proies mangées par prédateur
age_predateurs = np.zeros((size, size))  # Âge de chaque prédateur
age_proies = np.zeros((size, size))  # Âge de chaque proie
sante_predateurs = np.ones((size, size))  # Santé (1 au début)

population_proies = []
population_predateurs = []

# Couleurs
cmap = ListedColormap(['white', "#7c94bc", "#f65047"])  # Vide, Proie, Prédateur

# Fonction

def update(frame):
    global proies, predateurs, proies_mangees, age_predateurs, age_proies, sante_predateurs, seuil_reproduction_predateur
    
    # On travaille sur des copies pour pas modifier la grille en cours de lecture
    
    nouv_proies = proies.copy()
    nouv_predateurs = predateurs.copy()
    nouv_proies_mangees = proies_mangees.copy()
    nouv_age = age_predateurs.copy()
    nouv_ageo = age_proies.copy()
    nouv_sante = sante_predateurs.copy()
    nouv_seuil_reproduction_predateur = seuil_reproduction_predateur
    
    for i in range(size):
        for j in range(size):
            
            # Comportement des proies
            if proies[i, j] == 1:  
                
                nouv_ageo[i, j] += 1  # Vieillissement
                
                # Calcul dynamique du taux de reproduction
                taux_actuel = proie_rep
                if np.sum(predateurs) < seuil_predateurs_bas:
                    taux_actuel += boost_reproduction
                    
                # Phase 1 : Reproduction
                if np.random.rand() < taux_actuel and np.sum(proies) < size*size * 0.8:
                    ni, nj = np.random.randint(0, size, 2)
                    if nouv_proies[ni, nj] == 0:
                        nouv_proies[ni, nj] = 1
                    
                # Phase 2 : Mortalité
                if (nouv_ageo[i, j] > duree_vie_max1):
                    nouv_proies[i, j] = 0

            
            # Comportement des prédateurs
            elif predateurs[i, j] == 2:
                
                nouv_age[i, j] += 1  # Vieillissement
                
                # Liste les voisins
                voisins = [(i+di, j+dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] 
                          if 0 <= i+di < size and 0 <= j+dj < size and (di != 0 or dj != 0)]
                np.random.shuffle(voisins)
                deplacement = False
                
                # Phase 1 : Chasse
                for ni, nj in voisins:
                    if nouv_proies[ni, nj] == 1:
                        nouv_proies[ni, nj] = 0  # Mange la proie
                        nouv_proies_mangees[i, j] += 1
                        nouv_sante[i, j] = nouv_sante[i, j] + 0.1  # Améliore la santé
                        deplacement = True
                        break
                # Phase 2 : Déplacement
                if not deplacement:
                    nouv_sante[i, j]= nouv_sante[i, j] -0.25  # Pénalité santé si ne mange pas
                    for ni, nj in voisins:
                        if nouv_predateurs[ni, nj] == 0:
                            nouv_predateurs[i, j] = 0
                            nouv_predateurs[ni, nj] = 2
                            nouv_proies_mangees[ni, nj] = nouv_proies_mangees[i, j]
                            nouv_age[ni, nj] = nouv_age[i, j]
                            nouv_sante[ni, nj] = nouv_sante[i, j]
                            break
                if np.sum(predateurs) < 25:  # Seuil critique des prédateurs
                    nouv_sante[i, j] = max(1.2, nouv_sante[i, j] + 0.3)  # Bonus santé
                    nouv_seuil_reproduction_predateur = 4  # Réduction du seuil nécessaire
                
                # Phase 3 : Reproduction
                if (nouv_proies_mangees[i, j] >= nouv_seuil_reproduction_predateur and 
                    nouv_sante[i, j] > 1.2 and 
                    np.random.rand() < 0.4):
                    ni, nj = np.random.randint(0, size, 2)
                    if nouv_predateurs[ni, nj] == 0:
                        nouv_predateurs[ni, nj] = 2
                        nouv_proies_mangees[ni, nj] = 0  # Proies mangées par le nouveau prédateur
                        nouv_age[ni, nj] = 0
                        nouv_sante[ni, nj] = 0.8  # Santé initiale réduite (consanguinité)
                        nouv_proies_mangees[i, j] = 0  # Reset parent
                        
                # Phase 4 : Mortalité
                if (nouv_age[i, j] > duree_vie_max1 or 
                    nouv_sante[i, j] <= 0.4):
                    nouv_predateurs[i, j] = 0

    # Mise à jour globale
    proies, predateurs = nouv_proies, nouv_predateurs
    proies_mangees, age_predateurs, sante_predateurs, age_proies, seuil_reproduction_predateur= nouv_proies_mangees, nouv_age, nouv_sante, nouv_ageo, nouv_seuil_reproduction_predateur
    # Visualisation
    img.set_array(proies + predateurs)
    ax.set_title(f"Génération {frame} | Orignaux: {np.sum(proies)} | Loups: {np.sum(predateurs)}")
    # Stockage des données de population
    population_proies.append(np.sum(proies))
    population_predateurs.append(np.sum(predateurs))

    return img

# Animation
fig, ax = plt.subplots(figsize=(10, 10))
img = ax.imshow(proies + predateurs, cmap=cmap, interpolation='nearest')
ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=100)

ani.save('simulation-gif.gif', writer='pillow', fps=10, dpi=100)

plt.show()


# Création du graphe
fig2, ax1 = plt.subplots(figsize=(14, 7))

# Barres pour les prédateurs
ax1.bar(range(len(population_predateurs)), population_predateurs, color="#f65047", width=0.8, label='Loups')
ax1.set_ylabel("Population de loups", color="#f65047", fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor="#f65047")
ax1.set_ylim(0, 125)

# Courbe pour les proies
ax2 = ax1.twinx()
ax2.plot(range(len(population_proies)), population_proies, color="#1d448c", linewidth=3, 
         marker='o', markersize=8, markeredgecolor="#1d448c", label='Orignaux')
ax2.set_ylabel("Population d'orignaux", color="#1d448c", fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor="#7c94bc")
ax2.set_ylim(0, 2200)

# Titre et grille
plt.title("Évolution des populations", 
          fontsize=14, pad=20, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3)

# Légende unifiée
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', 
           bbox_to_anchor=(0.5, 1.15), ncol=2, fontsize=12)

# Ajustements finaux
plt.xlim(0, 65)
plt.tight_layout()
plt.savefig("simulation-graphe.png", dpi=100)
plt.show()
