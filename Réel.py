import matplotlib.pyplot as plt

# Données brutes sous forme de listes

annees = list(range(1980, 2020))

loups = [50, 30, 14, 23, 24, 22, 20, 16, 12, 11, 15, 12, 12, 13, 15, 16,
22, 24, 14, 25, 29, 19, 17, 19, 29, 30, 30, 21, 23, 24, 19, 16,
9, 8, 9, 3, 2, 2, 2, 14]

orignaux = [664, 650, 700, 900, 811, 1062, 1025, 1380, 1653, 1397, 1216,
1313, 1600, 1880, 1800, 2400, 1200, 500, 700, 750, 850, 900,
1000, 900, 750, 540, 385, 450, 650, 530, 510, 515, 750, 975,
1050, 1250, 1300, 1600, 1500, 2060]

# Création du graphe
fig, ax1 = plt.subplots(figsize=(14, 7))

# Barres pour les loups
ax1.bar(annees, loups, color="#f65047", width=0.8, label='Loups')
ax1.set_ylabel("Population de loups", color="#f65047", fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor="#f65047")
ax1.set_ylim(0, 60)

# Courbe pour les orignaux
ax2 = ax1.twinx()
ax2.plot(annees, orignaux, color="#1d448c", linewidth=3,
marker='o', markersize=8, markeredgecolor="#1d448c", label='Orignaux')
ax2.set_ylabel("Population d'orignaux", color="#1d448c", fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor="#1d448c")
ax2.set_ylim(0, 2500)

# Titre et grille
plt.title("Évolution des populations à l'Île Royale (1980–2019)",
fontsize=14, pad=20, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3)

# Légende unifiée
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center',
bbox_to_anchor=(0.5, 1.15), ncol=2, fontsize=12)

# Ajustements finaux
plt.xlim(1979, 2020)
plt.tight_layout()
plt.savefig("réel-graphe.png", dpi=100)
plt.show()