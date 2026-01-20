# Jeremy IT CCNA - Day 04 : Introduction to the CLI

**Date :** 6 janvier 2026  
**Durée :** ~40 minutes  
**Série :** Jeremy IT CCNA (Day 04/53)  
**Ressources :** [Jeremy's IT Lab - Free CCNA Course](https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ)

---

## 🎯 Objectif

Maîtriser les bases du **Cisco IOS CLI** (Command Line Interface) : modes EXEC (user/privileged), configuration globale, commandes essentielles (hostname, passwords, encryption), et sauvegarder configurations running/startup.

---

## 📋 Cours : Cisco IOS CLI Basics

### Accès console (terminal physique)

#### Rollover Cable (Console Cable)

**Connecteurs :**
- **Côté équipement** : RJ45 (port console router/switch, couleur bleue généralement)
- **Côté PC** : DB9 (ancien port série) ou USB (adaptateur moderne)

**Pinout étoile (rollover) :**

```
RJ45 Pin 1 ──────── Pin 8 RJ45
RJ45 Pin 2 ──────── Pin 7 RJ45
RJ45 Pin 3 ──────── Pin 6 RJ45
RJ45 Pin 4 ──────── Pin 5 RJ45
RJ45 Pin 5 ──────── Pin 4 RJ45
RJ45 Pin 6 ──────── Pin 3 RJ45
RJ45 Pin 7 ──────── Pin 2 RJ45
RJ45 Pin 8 ──────── Pin 1 RJ45
```

**Mémorisation :** Pin 1 → Pin 8, Pin 2 → Pin 7 (inversion miroir complète).

**Différence vs câbles réseau :**
- **Straight-Through** : 1→1, 2→2 (réseau standard)
- **Crossover** : 1→3, 2→6 (équipements identiques)
- **Rollover** : 1→8, 2→7 (console uniquement)

---

#### Logiciel terminal (Packet Tracer)

**Accès CLI Packet Tracer :**
1. Cliquer équipement (router/switch)
2. Onglet **CLI** (vs Physical/Config)
3. Terminal s'ouvre (équivalent PuTTY/Tera Term réel)

**Logiciels réels :**
- **PuTTY** (Windows/Linux)
- **Tera Term** (Windows)
- **SecureCRT** (commercial)
- **screen/minicom** (Linux)

**Configuration port série :**
```
Baud rate : 9600
Data bits : 8
Parity : None
Stop bits : 1
Flow control : None
```

---

### Modes CLI Cisco IOS

#### 1. User EXEC Mode

**Prompt :** `Router>`

**Caractéristiques :**
- Mode par défaut après connexion
- **Lecture seule** (commandes show limitées)
- Pas accès configuration
- Sécurité basique (empêcher utilisateurs non-admin modifier config)

**Commandes disponibles :**
```cisco
Router> show version           # Version IOS (très limitée)
Router> show ip interface brief  # Interfaces (mais pas détails)
Router> ping 8.8.8.8           # Tests connectivité
Router> traceroute 1.1.1.1     # Tracer route
Router> enable                 # Passer Privileged EXEC
```

---

#### 2. Privileged EXEC Mode

**Prompt :** `Router#`

**Caractéristiques :**
- Accès via `enable` depuis User EXEC
- **Toutes commandes show** (show running-config, show startup-config)
- Commandes debug, copy, erase
- **Pas modification config** (lecture avancée seulement)

**Commandes typiques :**
```cisco
Router# show running-config    # Config RAM (actuelle)
Router# show startup-config    # Config NVRAM (boot)
Router# show ip route          # Table routage
Router# show interfaces        # Détails interfaces
Router# debug ip icmp          # Debugging ICMP
Router# configure terminal     # Passer Global Configuration
Router# copy running-config startup-config  # Sauvegarder
Router# reload                 # Redémarrer
```

**Retour User EXEC :**
```cisco
Router# disable
Router>
```

---

#### 3. Global Configuration Mode

**Prompt :** `Router(config)#`

**Accès :**
```cisco
Router# configure terminal
Router(config)#
```

**Raccourci :** `conf t`

**Caractéristiques :**
- **Modification configuration** (hostname, passwords, interfaces)
- Changes affectent **running-config** (RAM, temporaire)
- Sous-modes : interface, line, router

**Commandes typiques :**
```cisco
Router(config)# hostname R1           # Changer nom
Router(config)# enable password CCNA  # Mot de passe enable (non chiffré)
Router(config)# enable secret Cisco   # Mot de passe enable (chiffré MD5)
Router(config)# service password-encryption  # Chiffrer tous passwords
Router(config)# no ip domain-lookup   # Désactiver DNS lookup (éviter délais typos)
Router(config)# interface GigabitEthernet0/0/0  # Entrer mode interface
Router(config)# line console 0        # Configurer port console
```

**Retour Privileged EXEC :**
```cisco
Router(config)# exit
Router#
```

**Raccourci direct :** `Ctrl+Z` ou `end` (depuis n'importe quel sous-mode → Privileged EXEC).

---

#### 4. Interface Configuration Mode

**Prompt :** `Router(config-if)#`

**Accès :**
```cisco
Router(config)# interface GigabitEthernet0/0/0
Router(config-if)#
```

**Raccourci :** `int gi0/0/0`

**Commandes typiques :**
```cisco
Router(config-if)# ip address 192.168.1.1 255.255.255.0  # Assigner IP
Router(config-if)# no shutdown       # Activer interface (admin up)
Router(config-if)# description WAN Link to ISP  # Documentation
Router(config-if)# speed 100         # Forcer 100 Mbps
Router(config-if)# duplex full       # Forcer full-duplex
```

**Retour Global Config :**
```cisco
Router(config-if)# exit
Router(config)#
```

---

### Configurations Running vs Startup

#### Running-Config (RAM)

**Localisation :** RAM (volatile, perdue au reboot)

**Visualiser :**
```cisco
Router# show running-config
```

**Caractéristiques :**
- Configuration **active** (appliquée immédiatement)
- Modifications `configure terminal` → running-config
- **Non persistante** après reload (sauf si sauvegardée)

---

#### Startup-Config (NVRAM)

**Localisation :** NVRAM (Non-Volatile RAM, persistante)

**Visualiser :**
```cisco
Router# show startup-config
```

**Caractéristiques :**
- Configuration **boot** (chargée au démarrage)
- **Persistante** après reload/power off
- Nécessite sauvegarde manuelle (running → startup)

---

#### Sauvegarder configuration

**Méthode 1 (recommandée) :**
```cisco
Router# copy running-config startup-config
Destination filename [startup-config]? [Enter]
Building configuration...
[OK]
```

**Méthode 2 (raccourci) :**
```cisco
Router# write memory
```

**Méthode 3 (très court) :**
```cisco
Router# wr
```

**Important :** Sans sauvegarde, **reload = perte config** (retour startup-config ancienne ou vide).

---

### Passwords Cisco IOS

#### 1. Enable Password (obsolète)

**Configuration :**
```cisco
Router(config)# enable password CCNA
```

**Caractéristiques :**
- Protège accès Privileged EXEC (`enable` command)
- **Stocké en clair** (visible `show running-config`)
- **Obsolète** (remplacé par `enable secret`)

**Visualisation running-config :**
```
enable password CCNA
```

---

#### 2. Enable Secret (recommandé)

**Configuration :**
```cisco
Router(config)# enable secret Cisco
```

**Caractéristiques :**
- Protège accès Privileged EXEC
- **Chiffré MD5** (hash irréversible)
- **Type 5 encryption** (visible running-config)
- **Priorité** : Si `enable password` ET `enable secret` configurés → **secret utilisé**

**Visualisation running-config :**
```
enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
```

**Type 5** = MD5 hashing (vs Type 7 = réversible).

---

#### 3. Service Password-Encryption

**Problème :** Autres passwords (console, VTY, enable password) stockés **clair** par défaut.

**Solution :**
```cisco
Router(config)# service password-encryption
```

**Effet :**
- Chiffre **tous passwords futurs** (line console, vty, enable password)
- Chiffre **passwords existants** non chiffrés
- **Type 7 encryption** (Vigenère cipher, **faible**, réversible)

**Visualisation avant :**
```
line console 0
 password cisco123
```

**Visualisation après :**
```
line console 0
 password 7 094F471A1A0A
```

**Note :** Type 7 **facilement décryptable** (outils en ligne) → Utiliser `enable secret` (Type 5) pour vraie sécurité.

---

#### Comparaison types encryption

| Type | Méthode | Réversible | Usage | Sécurité |
|------|---------|------------|-------|----------|
| **Type 0** | Plaintext | Oui (visible) | Défaut (aucune config) | ❌ Nulle |
| **Type 7** | Vigenère cipher | Oui (facilement) | `service password-encryption` | 🟡 Faible |
| **Type 5** | MD5 hash | Non (hash) | `enable secret` | 🟢 Correcte |
| **Type 8** | PBKDF2 SHA-256 | Non (hash) | `enable algorithm-type sha256 secret` | 🟢 Forte |
| **Type 9** | Scrypt | Non (hash) | `enable algorithm-type scrypt secret` | 🟢 Très forte |

**Best practice :** `enable secret` (Type 5 minimum) + `service password-encryption` (masquer Type 7).

---

#### Priorité passwords enable

**Scénario :** Les 2 configurés simultanément.

```cisco
Router(config)# enable password CCNA
Router(config)# enable secret Cisco
```

**Question :** Quel password utilisé lors `enable` ?

**Réponse :** **`enable secret`** (priorité absolue).

**Raison :** Sécurité (MD5 hash > plaintext).

**Test :**
```cisco
Router> enable
Password: [taper "Cisco"]  ← Secret MD5
Router#
```

Si taper "CCNA" (enable password) → **Access denied**.

---

## 🧪 Lab : Basic Router/Switch Configuration

### Énoncé

Configurer router R1 et switch SW1 :

1. Changer hostnames (R1, SW1)
2. Configurer enable password **non chiffré** "CCNA"
3. Tester password User → Privileged EXEC
4. Visualiser password running-config (doit être clair)
5. Activer encryption tous passwords
6. Visualiser running-config (passwords chiffrés Type 7)
7. Configurer enable secret **chiffré** "Cisco"
8. Tester quel password requis (secret > password)
9. Vérifier types encryption running-config
10. Sauvegarder running → startup

---

### Résolution

#### Router R1

**Step 1 : Changer hostname**

```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R1
R1(config)#
```

**Observation :** Prompt change immédiatement `Router(config)#` → `R1(config)#`.

---

**Step 2 : Enable password non chiffré**

```cisco
R1(config)# enable password CCNA
```

---

**Step 3 : Tester password**

```cisco
R1(config)# exit
R1# disable
R1> enable
Password: [taper "CCNA"]
R1#
```

**Succès :** Accès Privileged EXEC.

---

**Step 4 : Visualiser password clair**

```cisco
R1# show running-config
!
enable password CCNA
!
```

**Problème :** Password visible **plaintext** (Type 0).

---

**Step 5 : Activer encryption**

```cisco
R1# configure terminal
R1(config)# service password-encryption
```

---

**Step 6 : Vérifier encryption Type 7**

```cisco
R1# show running-config
!
enable password 7 0822455D0A16
!
service password-encryption
!
```

**Type 7** = Vigenère cipher (faible mais masque texte).

---

**Step 7 : Configurer enable secret**

```cisco
R1(config)# enable secret Cisco
```

---

**Step 8 : Tester priorité passwords**

```cisco
R1(config)# exit
R1# disable
R1> enable
Password: [taper "CCNA"]  ← Enable password
Access denied

R1> enable
Password: [taper "Cisco"]  ← Enable secret
R1#
```

**Résultat :** `enable secret` **prioritaire** (CCNA ignoré).

---

**Step 9 : Vérifier types encryption**

```cisco
R1# show running-config
!
enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
enable password 7 0822455D0A16
!
service password-encryption
!
```

**Type 5** = MD5 hash (enable secret)  
**Type 7** = Vigenère (enable password)

**Question lab :** "What encryption type number is used for the encrypted 'enable password'?"  
**Réponse :** **7** (Type 7 Vigenère)

**Question lab :** "What encryption type number is used for the encrypted 'enable secret'?"  
**Réponse :** **5** (Type 5 MD5)

---

**Step 10 : Sauvegarder config**

```cisco
R1# copy running-config startup-config
Destination filename [startup-config]? [Enter]
Building configuration...
[OK]
```

**Vérification :**
```cisco
R1# show startup-config
!
hostname R1
!
enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
enable password 7 0822455D0A16
!
```

**Succès :** Config persistante (survit reload).

---

#### Switch SW1

**Répéter étapes identiques :**

```cisco
Switch> enable
Switch# configure terminal
Switch(config)# hostname SW1
SW1(config)# enable password CCNA
SW1(config)# service password-encryption
SW1(config)# enable secret Cisco
SW1(config)# exit
SW1# copy running-config startup-config
```

**Vérification finale :**
```cisco
SW1# show running-config
!
hostname SW1
!
enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
enable password 7 0822455D0A16
!
```

---

## 💡 Apprentissages clés

### Rollover cable pinout (découverte)

**Avant lab :** Connaissais existence console cable, mais **jamais mémorisé pinout**.

**Après cours Jeremy :** **Pin 1→8, 2→7, 3→6, 4→5** (inversion étoile complète).

**Utilité réelle :** Rare (câbles achetés pré-faits), mais utile troubleshooting (tester continuité multimètre).

---

### Enable password vs secret (clarification)

**Avant lab :** Savais `enable secret` meilleur, mais **pas priorité exacte**.

**Découverte :** Si **les 2 configurés**, secret **toujours prioritaire** (password ignoré).

**Best practice :**
1. Configurer **uniquement** `enable secret` (éviter confusion)
2. Si `enable password` existe (legacy), le supprimer :
   ```cisco
   Router(config)# no enable password
   ```

---

### Service password-encryption = Type 7 (faible)

**Erreur fréquente :** Penser `service password-encryption` = sécurité forte.

**Réalité :** Type 7 = **masquage basique** (shoulder surfing), pas vraie encryption.

**Décryptage facile :**
- Outils en ligne (type "cisco type 7 decrypt")
- Scripts Python (cisco_decrypt.py)

**Usage légitime :** Empêcher lecture accidentelle (screenshots, partage configs).

**Vraie sécurité :** `enable secret` Type 5 (MD5) ou Type 8/9 (SHA-256/Scrypt).

---

### Running vs Startup (piège débutants)

**Scénario classique :**
1. Technicien configure router (`hostname R1`, `enable secret`, IPs interfaces)
2. Teste connectivité (ping OK)
3. Part sans `copy run start`
4. Reboot nocturne (maintenance, panne électrique)
5. **Config perdue** → hostname redevient "Router", IPs disparaissent

**Réflexe professionnel :** `wr` après **chaque session config** (automatisme musculaire).

---

### Modes CLI (hiérarchie)

**Visualisation :**

```
User EXEC (Router>)
    ↓ enable
Privileged EXEC (Router#)
    ↓ configure terminal
Global Configuration (Router(config)#)
    ↓ interface gi0/0/0
Interface Configuration (Router(config-if)#)
    ↓ exit → Global
    ↓ exit → Privileged
    ↓ disable → User
```

**Raccourcis navigation :**
- `Ctrl+Z` : N'importe quel mode → Privileged EXEC (immédiat)
- `end` : Identique Ctrl+Z (commande)
- `exit` : Remonter 1 niveau (config-if → config → privileged → user → déconnexion)

---

### Tab completion (productivité)

**Fonctionnalité :** IOS complète commandes partielles.

**Exemples :**
```cisco
Router# sh ru[Tab]  → show running-config
Router# conf t[Tab] → configure terminal
Router(config)# int gi0/0/0[Tab] → interface GigabitEthernet0/0/0
```

**Avantage :** Rapidité + éviter typos (IOS complète uniquement commandes valides).

---

### Question mark (aide contextuelle)

**Usage 1 : Liste commandes disponibles**
```cisco
Router> ?
  enable    Turn on privileged commands
  exit      Exit from the EXEC
  ping      Send echo messages
  show      Show running system information
  ...
```

**Usage 2 : Complétion partielle**
```cisco
Router# show ?
  arp          ARP table
  interfaces   Interface status
  ip           IP information
  running-config  Current operating configuration
  ...
```

**Usage 3 : Syntaxe commande**
```cisco
Router# show ip ?
  interface  IP interface status
  route      IP routing table
  ...
```

**Productivité :** `?` après chaque mot = découvrir options (pas besoin mémoriser tout).

---

## 🏢 Application professionnelle

### Première configuration router entreprise

**Scénario :** Déploiement router Cisco ISR 4331 siège entreprise.

**Checklist initiale :**

```cisco
Router> enable
Router# configure terminal

# 1. Hostname (identifier équipement)
Router(config)# hostname HQ-ROUTER-01

# 2. Enable secret (accès admin)
HQ-ROUTER-01(config)# enable secret P@ssw0rd_SecureAdmin2026

# 3. Console password (accès physique)
HQ-ROUTER-01(config)# line console 0
HQ-ROUTER-01(config-line)# password C0ns0le_P@ss123
HQ-ROUTER-01(config-line)# login
HQ-ROUTER-01(config-line)# exit

# 4. VTY password (accès SSH/Telnet distant)
HQ-ROUTER-01(config)# line vty 0 15
HQ-ROUTER-01(config-line)# password VTY_S3cur3!
HQ-ROUTER-01(config-line)# login
HQ-ROUTER-01(config-line)# exit

# 5. Encryption passwords
HQ-ROUTER-01(config)# service password-encryption

# 6. Désactiver DNS lookup (éviter délais typos)
HQ-ROUTER-01(config)# no ip domain-lookup

# 7. Banner MOTD (avertissement légal)
HQ-ROUTER-01(config)# banner motd #
*****************************************************************
* UNAUTHORIZED ACCESS PROHIBITED                                *
* This system is for authorized users only.                     *
* Activity is monitored and recorded. Violators prosecuted.     *
*****************************************************************
#

# 8. Sauvegarder
HQ-ROUTER-01(config)# exit
HQ-ROUTER-01# copy running-config startup-config
```

**Temps :** 5 minutes (checklist standard).

---

### Troubleshooting accès perdu (password recovery)

**Scénario :** Admin oublie `enable secret`, accès Privileged EXEC impossible.

**Procédure password recovery (Cisco) :**

1. **Reboot + ROMMON** (appuyer Ctrl+Break durant boot)
2. **Changer config-register** :
   ```
   rommon 1> confreg 0x2142  # Ignorer startup-config
   rommon 2> reset
   ```
3. **Router boot sans config** (factory default)
4. **Copier startup → running** :
   ```cisco
   Router# copy startup-config running-config
   ```
5. **Changer password** :
   ```cisco
   Router# configure terminal
   Router(config)# hostname R1
   R1(config)# enable secret NewPassword123
   ```
6. **Restaurer config-register** :
   ```cisco
   R1(config)# config-register 0x2102  # Boot normal
   R1(config)# exit
   R1# copy running-config startup-config
   R1# reload
   ```

**Sécurité physique :** Password recovery nécessite accès console → **Datacenter locked**.

---

### Template configuration (automatisation)

**Problème :** Configurer 50 routers identiquement (succursales).

**Solution :** Script template + TFTP.

**Template base (`router-template.cfg`) :**
```cisco
service password-encryption
no ip domain-lookup
!
enable secret GlobalAdminPass2026
!
line console 0
 password ConsolePass123
 login
 logging synchronous
!
line vty 0 15
 password VtyPass456
 login
 transport input ssh
!
banner motd #Unauthorized access prohibited#
```

**Déploiement :**
```cisco
# Depuis TFTP server (10.0.0.100)
Router# copy tftp://10.0.0.100/router-template.cfg running-config

# Personnaliser hostname
Router(config)# hostname BRANCH-RTR-PARIS-01

# Sauvegarder
Router# wr
```

**Gain :** 50 routers en 30 minutes (vs 4 heures manuellement).

---

## ❌ Difficultés rencontrées

### Aucune (notions déjà acquises)

**Feedback :** Lab plutôt facile, notions déjà abordées formations précédentes (TSSR, BTS SIO).

**Nouveauté mineure :** Rollover cable pinout détails (1→8, 2→7) jamais mémorisé avant.

**Utilité lab :** Rafraîchissement sympa commandes basiques (`enable secret` vs `password`, types encryption 5 vs 7).

---

## 🔗 Ressources

- **Jeremy's IT Lab Day 04** : [Intro to CLI](https://www.youtube.com/watch?v=CKIT16OChSg&list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ&index=4)
- **Cisco IOS Command Reference** : [CLI Fundamentals](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/command/fundamentals-cr-book.html)
- **Password Recovery Procedures** : [Cisco Support](https://www.cisco.com/c/en/us/support/docs/routers/2800-series-integrated-services-routers/112058-c2900-password-recovery-00.html)

---

## 📝 Commandes à retenir

### Navigation modes

```cisco
Router> enable                  # User → Privileged EXEC
Router# configure terminal      # Privileged → Global Config
Router(config)# interface gi0/0/0  # Global → Interface Config
Router(config-if)# exit         # Remonter 1 niveau
Router(config)# end             # → Privileged EXEC (depuis n'importe où)
# Ctrl+Z                        # Idem end (raccourci clavier)
Router# disable                 # Privileged → User EXEC
```

### Configuration basique

```cisco
# Hostname
Router(config)# hostname R1

# Enable secret (MD5, recommandé)
R1(config)# enable secret Cisco

# Enable password (Type 7 faible, obsolète)
R1(config)# enable password CCNA

# Encryption passwords (Type 7)
R1(config)# service password-encryption

# Désactiver DNS lookup
R1(config)# no ip domain-lookup
```

### Sauvegarder config

```cisco
# Méthode complète
Router# copy running-config startup-config

# Raccourcis
Router# write memory
Router# wr
```

### Visualiser configs

```cisco
Router# show running-config    # RAM (actuelle)
Router# show startup-config    # NVRAM (boot)
Router# show version           # IOS version, uptime, hardware
```

---

**Note :** Bases CLI solides essentielles Days suivants (interface config, VLANs, routing).

**Prochaine étape :** Day 05 - Ethernet LAN Switching (MAC address table, flooding, forwarding).
