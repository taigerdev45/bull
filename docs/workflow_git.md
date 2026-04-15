## ** WORKFLOW GIT**

**Projet :** Gestion Bulletins de Notes LP ASUR  
**Repository :** `https://github.com/taigerdev45/bull.git`  
**Date :** Avril 2026

---

## ** Rappel des branches**

| Collaborateur | Branche personnelle | Rôle |
|--------------|---------------------|------|
| **Bary** | `feature_bary` | Frontend - Interface saisie notes |
| **Brady** | `feature_brady` | Frontend - Tableaux et listes |
| **Herbert** | `feature_herbert` | Frontend - Génération PDF |

**Règle d'or :** `main` est protégée. **Personne ne push directement sur main.**

---

## **ÉTAPE 1 : Cloner le projet (Une seule fois)**

### **Commandes à exécuter**

```bash
# 1. Ouvrir un terminal (Git Bash, Terminal, PowerShell)

# 2. Se placer dans le dossier où vous voulez cloner
cd Documents/Projets/    # Exemple sur Windows
# ou
cd ~/Documents/          # Exemple sur Mac/Linux

# 3. Cloner le repository
git clone https://github.com/taigerdev45/bull.git

# 4. Entrer dans le dossier du projet
cd bull

# 5. Vérifier que vous êtes sur main
git branch
# Résultat attendu : * main
```

### **Vérification initiale**

```bash
# Voir toutes les branches disponibles (locales + distantes)
git branch -a

# Résultat attendu :
# * main
#   remotes/origin/feature_bary
#   remotes/origin/feature_brady
#   remotes/origin/feature_herbert
#   remotes/origin/main
```

---

## **ÉTAPE 2 : Basculer sur votre branche personnelle**

### **Pour Bary**

```bash
# Créer une copie locale de votre branche distante
git checkout -b feature_bary origin/feature_bary

# Vérifier
git branch
# Résultat : * feature_bary
#              main
```

### **Pour Brady**

```bash
git checkout -b feature_brady origin/feature_brady
git branch
```

### **Pour Herbert**

```bash
git checkout -b feature_herbert origin/feature_herbert
git branch
```

>  **Astuce :** Une fois fait, vous resterez sur cette branche. Tout votre travail se fait ici.

---

## **ÉTAPE 3 : Workflow quotidien (Répéter à chaque session)**

### **3.1 Récupérer les dernières modifications du main**

```bash
# S'assurer d'être sur votre branche
git checkout feature_bary    # (ou feature_brady / feature_herbert)

# Récupérer les infos du serveur
git fetch origin

# Voir si main a évolué
git log --oneline main..origin/main

# Fusionner main dans votre branche (recommandé)
git merge origin/main

# OU si vous préférez rebase (historique plus propre)
git rebase origin/main
```

### **3.2 Faire vos modifications**

```bash
# Vérifier sur quelle branche vous êtes
git branch
# Doit afficher : * feature_bary (ou la vôtre)

# Créer/modifier des fichiers
# Exemple : modifier frontend/app/page.tsx
```

### **3.3 Sauvegarder vos modifications (commit)**

```bash
# Voir les fichiers modifiés
git status

# Ajouter les fichiers modifiés
git add .                    # Tous les fichiers modifiés
# OU
git add frontend/app/page.tsx  # Un fichier spécifique

# Créer un commit avec message descriptif
git commit -m "feat: ajoute composant TableEtudiants avec pagination"

# Convention de messages :
# feat:     nouvelle fonctionnalité
# fix:      correction de bug
# refactor: restructuration code
# docs:     documentation
# test:     tests
# style:    formatage (espaces, virgules)
```

### **3.4 Envoyer sur GitHub (push)**

```bash
# Envoyer vos commits sur votre branche distante
git push origin feature_bary    # Bary
# ou
git push origin feature_brady   # Brady
# ou
git push origin feature_herbert # Herbert
```

>  **Si vous tentez push sur main, vous aurez une erreur 403. C'est normal !**

---

## **ÉTAPE 4 : Demande de fusion (Pull Request / PR)**

### **Méthode 1 : Via GitHub Web (Recommandée pour débutants)**

1. **Aller sur le repository :** `https://github.com/taigerdev45/bull`

2. **Cliquer sur "Pull requests"** (onglet en haut)

3. **Cliquer sur "New pull request"** (bouton vert)

4. **Configurer la PR :**
   - **base:** `main` ← **compare:** `feature_bary` (votre branche)

5. **Remplir le formulaire :**
   ```
   Titre : [Bary] Ajoute composant TableEtudiants
   
   Description :
   - Ajoute tableau réutilisable pour listes d'étudiants
   - Pagination côté client
   - Tri par nom et matricule
   - Responsive design
   
   Tests : Vérifié sur Chrome et Firefox
   ```

6. **Cliquer "Create pull request"**

7. **Demander une review** à `taigerdev45` (chef de projet)

---

### **Méthode 2 : Via GitHub CLI (Plus rapide)**

```bash
# Installer gh si pas déjà fait : https://cli.github.com/

# Se connecter (une seule fois)
gh auth login

# Créer la Pull Request depuis votre branche
gh pr create --base main --head feature_bary \
  --title "[Bary] Ajoute composant TableEtudiants" \
  --body "Description détaillée des changements..."

# Voir le statut de vos PR
gh pr list --author @me

# Ouvrir la PR dans le navigateur
gh pr view --web
```

---

### **Méthode 3 : Via VS Code (Si vous utilisez VS Code)**

1. **Ouvrir l'onglet Source Control** (Ctrl+Shift+G)
2. **Stage changes** → **Commit** → **Push**
3. **Cliquer sur "Create Pull Request"** (bouton qui apparaît après push)
4. **Remplir le formulaire** dans VS Code
5. **Submit**

---

## **ÉTAPE 5 : Après la Pull Request**

### **Ce qui se passe**

| Étape | Acteur | Action |
|-------|--------|--------|
| 1 | Vous | Créez la PR |
| 2 | Chef de projet | Review le code |
| 3 | Chef de projet | Approuve ou demande des changements |
| 4 | Vous | Corrigez si demandé (nouveau commit + push) |
| 5 | Chef de projet | Merge dans `main` |

### **Si des changements sont demandés**

```bash
# Sur votre branche locale
git checkout feature_bary

# Faire les corrections
# Modifier les fichiers...

# Commit des corrections
git add .
git commit -m "fix: corrige pagination selon review"

# Push (la PR se met à jour automatiquement)
git push origin feature_bary
```

>  **La Pull Request se met à jour automatiquement** quand vous push sur la même branche.

---

## ** Commandes de référence rapide**

### **Carte de visite (à garder sous la main)**

```bash
# === DÉBUT DE SESSION ===
git checkout feature_bary          # Votre branche
git fetch origin                   # Voir les nouveautés
git merge origin/main              # Mettre à jour avec main

# === TRAVAIL ===
git status                         # Voir état
git add .                          # Préparer fichiers
git commit -m "feat: description"  # Sauvegarder
git push origin feature_bary       # Envoyer

# === FIN DE SESSION ===
git log --oneline -3               # Voir derniers commits
git status                         # Vérifier tout est pushé

# === URGENCE : Annuler des modifications ===
git checkout -- .                  # Annuler tous changements non commités
git reset HEAD~1                   # Annuler dernier commit (garde modifications)
git reset --hard HEAD~1            # Annuler dernier commit (perd modifications)
```

---

## ** Erreurs courantes et solutions**

### **Erreur 1 : "fatal: not a git repository"**

```bash
# Problème : Vous n'êtes pas dans le dossier bull
cd chemin/vers/bull
# ou recloner si dossier perdu
git clone https://github.com/taigerdev45/bull.git
```

### **Erreur 2 : "error: pathspec 'feature_bary' did not match"**

```bash
# Problème : La branche n'existe pas localement
git fetch origin
git checkout -b feature_bary origin/feature_bary
```

### **Erreur 3 : "failed to push some refs"**

```bash
# Problème : Des modifications sur le serveur que vous n'avez pas
git pull origin feature_bary   # Récupérer d'abord
# Résoudre conflits si nécessaire
git push origin feature_bary   # Puis push
```

### **Erreur 4 : "403 Forbidden" sur push main**

```bash
#  C'est NORMAL ! Main est protégée.
# Solution : Push sur votre branche feature
git push origin feature_bary   # ✓ Correct
```

### **Erreur 5 : Conflits de fusion (merge conflict)**

```bash
# Signe : Git indique "CONFLICT" lors du pull/merge

# 1. Ouvrir les fichiers en conflit (marqués <<<<<<< HEAD)
# 2. Choisir quelle version garder
# 3. Supprimer les marqueurs <<<<<<< ======= >>>>>>>
# 4. Sauvegarder le fichier

git add .                      # Marquer comme résolu
git commit -m "fix: résout conflits de fusion"
git push origin feature_bary
```

---

## ** Résumé visuel du workflow**

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   CLONER UNE    │────▶│  TRAVAILLER SUR  │────▶│   PUSH SUR VOTRE │
│    FOIS SEULE   │     │   VOTRE BRANCHE   │     │    BRANCHE       │
│                 │     │  (feature_xxx)    │     │   (feature_xxx)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  CHEF PROJET    │◄────│  PULL REQUEST   │◄────│  GITHUB / gh    │
│  MERGE DANS     │     │  (Demande fusion) │     │  pr create      │
│     MAIN        │     │                   │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│   TOUT LE MONDE │
│  PULL ORIGIN/   │
│  MAIN POUR      │
│  METTRE À JOUR  │
└─────────────────┘
```

---

## ** Support**

**En cas de problème :**

1. **Vérifier votre branche :** `git branch`
2. **Vérifier le statut :** `git status`
3. **Contacter le chef de projet :** taigerdev45@email.com

**Liens utiles :**
- Repository : `https://github.com/taigerdev45/bull`
- Pull Requests : `https://github.com/taigerdev45/bull/pulls`
- Issues : `https://github.com/taigerdev45/bull/issues`
