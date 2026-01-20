# Challenge 06 : Linux Find Command

**Date** : 9 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Trouver tous les fichiers `.css` dans arborescence et les copier avec structure répertoires vers emplacement sécurisé.

---

## 📋 Énoncé

Audit sécurité a identifié du contenu malicieux dans code website. Équipe a trouvé potentiellement plus de fichiers infectés. Avant nettoyage, trouver tous fichiers similaires et les copier vers emplacement sûr pour investigation.

**Tâches** :

**a.** Sur App Server 1, dans `/var/www/html/media`, trouver tous les fichiers (pas répertoires) avec extension `.css`

**b.** Copier tous ces fichiers avec structure répertoires parents vers `/media`

**c.** Ne pas copier l'intégralité du contenu `/var/www/html/media`

**Serveur cible** : `tony@stapp01`

---

## ✅ Résolution

### 1. Se connecter au serveur

```bash
ssh tony@stapp01
```

### 2. Naviguer vers répertoire source

```bash
cd /var/www/html/media
```

### 3. Trouver et copier fichiers .css avec structure

```bash
sudo find . -name "*.css" | sudo xargs cp -a --parents -t /media
```

**Explication décomposée** :

**find . -name "*.css"** :
- `find .` : Chercher depuis répertoire courant
- `-name "*.css"` : Fichiers avec extension .css
- Sortie : Liste chemins relatifs (ex: `./css/style.css`, `./themes/dark/main.css`)

**| sudo xargs cp -a --parents -t /media** :
- `xargs` : Convertit entrée standard en arguments commande
- `cp -a` : Archive mode (preserve metadata, permissions, timestamps)
- `--parents` : Créer structure répertoires parents
- `-t /media` : Target directory (destination)

**Exemple fonctionnement** :
```
find . -name "*.css"
→ ./css/style.css
→ ./themes/dark/main.css

xargs cp -a --parents -t /media
→ cp -a --parents ./css/style.css /media
→ cp -a --parents ./themes/dark/main.css /media

Résultat /media :
/media/css/style.css
/media/themes/dark/main.css
```

### 4. Validation

Vérifier fichiers copiés avec structure :

```bash
find /media -type f
```

**Sortie attendue** :
```
/media/css/style.css
/media/themes/dark/main.css
/media/...
```

**Vérifier structure répertoires préservée** :
```bash
ls -R /media
```

---

## 💡 Notes

- **find -name** : Recherche fichiers par motif (wildcards `*`, `?`)
- **xargs** : Batch processing (évite "Argument list too long")
- **cp --parents** : Préserve arborescence répertoires source
- **-t destination** : Spécifie target avant sources (requis avec xargs)

---

## 🏷️ Tags

`#Linux` `#find` `#xargs` `#cp` `#FileManagement` `#Security` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
