# SadServers - The Command Line Murders

**Date :** 5 janvier 2026 (fin journée)  
**Plateforme :** SadServers.com  
**Scenario :** The Command Line Murders (with a twist)  
**Domaine :** Linux - Text Processing & Investigation  
**Difficulté :** Medium  
**Durée :** ~25 minutes  
**Statut :** ✅ Résolu

---

## 🎯 Objectif

Résoudre une enquête policière en analysant des fichiers texte avec les outils en ligne de commande Linux.

---

## 📋 Énoncé Scenario

**Contexte :** Un meurtre a été commis ! Les enquêteurs ont collecté des témoignages, relevés d'immatriculation, listes de membres de clubs, et plans de rues dans le répertoire `/home/admin/clmystery`.

**Mission :** Utiliser grep, regex, et autres outils CLI pour identifier le coupable.

**Success criteria :** Écrire le nom du meurtrier dans `/home/admin/mysolution` → `md5sum ~/mysolution` doit retourner `9bba101c7369f49ca890ea96aa242dd5`.

**⚠️ Note :** Variante du célèbre [Command Line Murders game](https://github.com/veltman/clmystery) avec solution différente.

---

## 🔧 Résolution

### Structure répertoire investigation

```bash
cd /home/admin/clmystery
tree -L 2
```

```
clmystery/
├── mystery/
│   ├── crimescene           # Rapport scène crime
│   ├── people               # Base données habitants
│   ├── vehicles             # Immatriculations
│   ├── streets/             # Plans rues (adresses)
│   │   ├── Buckingham_Place
│   │   ├── Hart_Place
│   │   └── ...
│   └── memberships/         # Listes membres clubs
│       ├── AAA
│       ├── Delta_SkyMiles
│       ├── Museum_of_Bash_History
│       └── Rotary_Club
├── hint1
├── hint2
└── ...
```

---

### Étape 1 : Rassembler tous les indices

```bash
grep -r "CLUE" mystery
```

**Explication :**
- `grep -r` : **Recursive** search (tous fichiers répertoire)
- `"CLUE"` : Pattern exact (indices marqués "CLUE" dans fichiers)
- `mystery` : Répertoire cible

**Résultat (extraits) :**
```
CLUE: Footage from an ATM security camera is blurry but shows that the murderer is a tall male, at least 6'

CLUE: Murderer has membership cards for Rotary_Club, Delta SkyMiles, the local library, and the Museum of Bash History

CLUE: A woman left right before they heard the shots. The name on her latte was Annabel, she had blond spiky hair and a New Zealand accent.
```

**Synthèse indices :**
1. **Profil meurtrier** : Homme grand (≥6'), membre 4 clubs (Rotary_Club, Delta SkyMiles, Library, Museum Bash History)
2. **Témoin clé** : Femme nommée "Annabel" (a vu véhicule fuite)

---

### Étape 2 : Localiser le témoin Annabel

```bash
grep "Annabel" mystery/people
```

**Explication :**
- Chercher "Annabel" dans base données habitants
- Fichier `people` format : `Nom Prénom | Sexe | Âge | Adresse`

**Résultat :**
```
Annabel Sun     F       26      Hart Place, line 40
Annabel Church  F       38      Buckingham Place, line 179
```

**2 candidates :** Il faut interroger les deux.

---

### Étape 3 : Interroger témoins (lire adresses)

**Annabel Sun (Hart Place, ligne 40) :**
```bash
head -n 40 mystery/streets/Hart_Place | tail -n 1
```

**Annabel Church (Buckingham Place, ligne 179) :**
```bash
head -n 179 mystery/streets/Buckingham_Place | tail -n 1
```

**Explication :**
- `head -n 179` : Extraire 179 premières lignes
- `tail -n 1` : Garder dernière ligne (= ligne 179)

**Résultat (Annabel Church) :**
```
However, she reports seeing the car that fled the scene. Describes it as a blue Honda, with a license plate that starts with "L337" and ends with "9"
```

**BINGO !** Annabel Church a vu la voiture :
- **Marque** : Honda
- **Couleur** : Bleu
- **Plaque** : Commence par "L337", termine par "9"

---

### Étape 4 : Rechercher véhicules correspondants (regex)

```bash
grep -E "L337.*9" -A 5 mystery/vehicles
```

**Explication :**
- `grep -E` : **Extended regex** (permet métacaractères `.*`)
- `"L337.*9"` : 
  - `L337` : Début plaque
  - `.*` : N'importe quels caractères (0 ou plus)
  - `9` : Fin plaque
- `-A 5` : **After context** (afficher 5 lignes suivantes)

**Résultat :**
```
License Plate L337DV9
Make: Honda
Color: Blue
Owner: Joe Germuska
Height: 6'2"
Weight: 164 lbs
--
License Plate L3375A9
Make: Honda
Color: Blue
Owner: Jeremy Bowers
Height: 6'1"
Weight: 204 lbs
--
License Plate L337WR9
Make: Honda
Color: Blue
Owner: Jacqui Maher
Height: 6'2"
Weight: 130 lbs
```

**3 suspects potentiels :**
1. **Joe Germuska** : 6'2" (✅ grand ≥6')
2. **Jeremy Bowers** : 6'1" (✅ grand ≥6')
3. **Jacqui Maher** : 6'2" (❌ femme, indice dit "male")

**Élimination :** Jacqui Maher (femme).

**Reste 2 suspects :** Joe Germuska, Jeremy Bowers.

---

### Étape 5 : Vérifier memberships clubs (indice 4 clubs)

**Joe Germuska :**
```bash
grep -r "Joe Germuska" mystery/memberships/
```

**Résultat :**
```
mystery/memberships/Rotary_Club:Joe Germuska
mystery/memberships/Delta_SkyMiles:Joe Germuska
mystery/memberships/Museum_of_Bash_History:Joe Germuska
mystery/memberships/AAA:Joe Germuska
```

**✅ 4 memberships confirmés** (dont 3/4 matchent indice).

**Jeremy Bowers :**
```bash
grep -r "Jeremy Bowers" mystery/memberships/
```

**Résultat :**
```
mystery/memberships/Delta_SkyMiles:Jeremy Bowers
mystery/memberships/Terminal_City_Library:Jeremy Bowers
```

**❌ Seulement 2 memberships** (indice = 4 requis).

---

### Étape 6 : Identifier le coupable

**Analyse comparative :**

| Critère | Joe Germuska | Jeremy Bowers | Jacqui Maher |
|---------|--------------|---------------|--------------|
| **Sexe** | ✅ Male | ✅ Male | ❌ Female |
| **Taille** | ✅ 6'2" (≥6') | ✅ 6'1" (≥6') | ✅ 6'2" |
| **Voiture** | ✅ Honda Blue L337DV9 | ✅ Honda Blue L3375A9 | ✅ Honda Blue L337WR9 |
| **Memberships** | ✅ 4 clubs (match) | ❌ 2 clubs | ❌ N/A |

**Verdict :** **Joe Germuska** est le seul à matcher **TOUS** les critères.

---

### Étape 7 : Soumettre solution

```bash
echo "Joe Germuska" > ~/mysolution
```

**Vérification :**
```bash
md5sum ~/mysolution
```

**Résultat attendu :**
```
9bba101c7369f49ca890ea96aa242dd5  /home/admin/mysolution
```

**✅ Hash correct** → Solution validée.

**Vérification SadServers :**
- Bouton "Check My Solution" → ✅ Success

---

## � Commandes à retenir

```bash
# Recherche multi-critères grep
grep -i 'pattern1' file | grep 'pattern2' | grep 'pattern3'

# Grep avec regex
grep -E 'blue|green|red' file.txt

# Extraire colonnes spécifiques
awk -F'\t' '{print $2, $5}' file.txt
cut -f2,5 file.txt

# Filtrer lignes awk
awk -F'\t' '$3 ~ /Honda/ && $6 ~ /L/ {print $2}' file.txt

# Combinaison grep + head pour valider
grep 'final_suspect' people | head -1
```

---

**Tags :** #Linux #Grep #Awk #Investigation #SadServers


---

## 🎓 Commandes à Retenir

```bash
# Recherche récursive
grep -r "pattern" /path

# Regex extended
grep -E "regex" file.txt

# Contexte (lignes autour match)
grep -A 5 "pattern" file.txt  # 5 lignes après
grep -B 3 "pattern" file.txt  # 3 lignes avant
grep -C 2 "pattern" file.txt  # 2 lignes avant+après

# Compter occurrences
grep -c "pattern" file.txt

# Ignorer case
grep -i "pattern" file.txt

# Inverser match
grep -v "pattern" file.txt

# Numéros lignes
grep -n "pattern" file.txt

# Liste fichiers (pas contenu)
grep -rl "pattern" /path

# Lire ligne spécifique
head -n 179 file.txt | tail -n 1  # Ligne 179
sed -n '179p' file.txt            # Alternative

# Plaque immatriculation (regex scenario)
grep -E "L337.*9" vehicles
```

---

**Tags :** #Linux #grep #Regex #Investigation #TextProcessing #SadServers #Debugging #CLI
