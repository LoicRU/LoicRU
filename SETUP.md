# 🧰 Setup — profil GitHub `LoicRU`

Tout ce qu'il y a à faire, dans l'ordre. Compte ~10 minutes.

---

## 1. Créer le repo spécial

GitHub affiche le README d'un repo qui porte **exactement ton pseudo** sur ta page de profil.

- Nouveau repo → nom : **`LoicRU`** (identique au pseudo, sinon ça ne marche pas)
- **Public** ✅
- Coche « Add a README file »

> Si le repo existe déjà, saute cette étape.

---

## 2. Déposer les fichiers

Arborescence finale du repo :

```
LoicRU/
├── README.md
├── build_header.py                 # régénère le header animé
├── assets/
│   ├── terminal.svg                # header animé (fait main, 0 dépendance)
│   ├── divider.svg                 # séparateur animé
│   └── footer.svg                  # bandeau de fin animé
└── .github/
    └── workflows/
        ├── snake.yml               # 🐍 serpent qui mange les contributions
        ├── 3d-contrib.yml          # 🧊 calendrier 3D isométrique
        └── metrics.yml             # 📊 optionnel (nécessite un token)
```

Le plus simple :

```bash
git clone https://github.com/LoicRU/LoicRU.git
cd LoicRU
# copie le contenu du dossier livré ici
git add .
git commit -m "feat: new profile README — terminal edition"
git push
```

---

## 3. Lancer les workflows une première fois

Deux images du README sont **générées par GitHub Actions** : avant le premier run, elles apparaissent cassées. C'est normal.

1. Onglet **Actions** du repo → autorise les workflows si GitHub le demande
2. `🐍 Snake — contribution graph` → **Run workflow**
3. `🧊 3D contribution calendar` → **Run workflow**

Ensuite ça tourne tout seul (snake toutes les 12 h, 3D chaque nuit).

**Vérifie aussi** : Settings → Actions → General → Workflow permissions → **Read and write permissions** ✅
(sans ça, les workflows ne peuvent pas pousser leurs images)

---

## 4. Optionnel — Metrics (`metrics.yml`)

La carte la plus riche (calendrier isométrique, achievements, habitudes de commit). Elle demande un token personnel :

1. GitHub → Settings → Developer settings → **Personal access tokens (classic)**
2. Génère un token avec le scope **`public_repo`** uniquement
3. Repo `LoicRU` → Settings → Secrets and variables → Actions → **New repository secret**
   - Nom : `METRICS_TOKEN`
   - Valeur : le token
4. Actions → `📊 Metrics` → Run workflow
5. Décommente le bloc ② dans le README (tout en bas, dans le commentaire HTML)

---

## 5. À personnaliser avant de pousser

| Où | Quoi |
| :-- | :-- |
| Badge `Contact` | Ton mail est en clair (`jpppp852@gmail.com`). Remplace-le par un mail public dédié, ou supprime le badge. |
| Section `man loic` | Ajoute l'URL de ton portfolio quand il est en ligne. |
| Bloc `~/now.log` | À rafraîchir tous les 2–3 mois, c'est la section qui vieillit le plus vite. |
| `~/.stack --deep` | Les barres de confiance sont mon estimation d'après tes projets — ajuste-les. |

---

## 6. Modifier le header animé

Tout le header vient d'un seul script. Édite la liste `LINES` dans `build_header.py` :

```python
LINES = [
    ([("$ ", GREEN, ""), ("whoami", TXT, "")], 0.40, 0.75),
    #   ^ segments (texte, couleur, classe)    ^ début  ^ durée de frappe
]
```

puis :

```bash
python3 build_header.py     # réécrit assets/terminal.svg
```

Aucune dépendance, juste Python 3. L'animation est en CSS pur embarqué dans le SVG (pas de JS — GitHub le bloquerait).

---

## 7. Dépannage

**Une image de stats ne s'affiche pas / affiche « Maximum retries exceeded »**
`github-readme-stats` est une instance publique saturée. Solution propre : déployer ton propre clone sur Vercel (5 min, gratuit) et remplacer `github-readme-stats.vercel.app` par ton domaine dans le README.
→ https://github.com/anuraghazra/github-readme-stats#deploy-on-your-own

**Une image mise à jour reste l'ancienne**
GitHub met les images en cache derrière son proxy (camo). Force le rafraîchissement en ajoutant `?v=2` à la fin de l'URL.

**Le SVG animé ne bouge pas**
Vérifie que tu regardes bien le repo `LoicRU/LoicRU` sur github.com (certains lecteurs Markdown tiers n'animent pas les SVG). Sur GitHub, ça tourne.

**Le serpent n'apparaît pas**
La branche `output` doit exister — elle est créée par le premier run du workflow. Vérifie aussi les Workflow permissions (étape 3).

---

## 8. Pour aller plus loin

| Module | Effort | Effet |
| :-- | :-- | :-- |
| **WakaTime** | 10 min | Temps de code réel par langage, mis à jour tout seul. Très crédible sur un CV. |
| **Spotify now-playing** | 20 min | Ce que tu écoutes en direct dans le README (fork *novatorem* + Vercel). |
| **Instance perso de github-readme-stats** | 5 min | Fiabilité + `count_private=true` qui compte vraiment tes repos privés. |
| **Épingler les repos** | 1 min | Le README ne remplace pas les *pinned repositories* : épingle Mosalea (si repo public) et `investment-bot-render`. |
| **Ajouter une bio + un lien** | 1 min | La bio GitHub s'affiche à gauche du README, elle compte autant. |
