# Jeremy IT CCNA - Day 01 : Network Devices

**Date :** 5 janvier 2026  
**Plateforme :** Udemy - Master Cisco CCNA 200-301  
**Instructeur :** Jeremy's IT Lab  
**Domaine :** Réseau - Fondamentaux  
**Durée cours :** 45 minutes  
**Durée lab :** 30 minutes  
**Statut :** ✅ Complété

---

## 🎯 Objectifs Day 01

**Théorie :**
- Comprendre les différents types d'équipements réseau
- Identifier leurs rôles et fonctions dans une infrastructure
- Comprendre les bases de l'interconnexion

**Lab Packet Tracer :**
- Prise en main interface Packet Tracer
- Ajouter équipements au workspace
- Interconnecter équipements avec câbles appropriés
- Découverte outil sélection automatique de connecteurs

---

## 📚 Notes Théoriques - Types d'Équipements Réseau

### 1. Client Devices (End Devices)

**Définition :** Équipements terminaux qui génèrent ou consomment du trafic réseau.

**Exemples :**
- **PC** (Desktop computers)
- **Laptops**
- **Smartphones / Tablets**
- **Serveurs** (Web, File, Database, Email, etc.)
- **Imprimantes réseau**
- **Caméras IP**
- **Téléphones IP**

**Caractéristiques :**
- Ont une **adresse IP** (IPv4 ou IPv6)
- Génèrent et reçoivent des données
- Ne transmettent PAS de trafic pour d'autres devices
- Connectés au réseau via **Ethernet** (câble) ou **Wi-Fi** (sans-fil)

**Rôle dans réseau :**
- **Source** : Envoie requêtes (ex: navigateur web → serveur)
- **Destination** : Reçoit réponses (ex: serveur → navigateur)

---

### 2. Switch (Commutateur réseau)

**Définition :** Équipement Layer 2 (Data Link) qui interconnecte devices dans un **même réseau local (LAN)**.

**Fonction principale :**
- **Transférer** frames Ethernet entre devices connectés
- **Apprendre** adresses MAC des devices (MAC address table)
- **Décider** vers quel port envoyer chaque frame (forwarding decision)

**Caractéristiques :**
- Nombreux ports Ethernet (8, 16, 24, 48+ ports)
- Opère sur **Layer 2** (MAC addresses)
- Crée domaines de collision séparés (full-duplex)
- Ne modifie PAS adresses IP (transparent Layer 3)

**Types :**
- **Unmanaged switch** : Configuration zéro, plug-and-play (SOHO)
- **Managed switch** : Configuration avancée (VLANs, QoS, STP, etc.) - Entreprise

**Exemple scénario :**
```
PC1 (192.168.1.10) ─┐
                    ├─ Switch ─ Server (192.168.1.100)
PC2 (192.168.1.20) ─┘
```
Switch permet PC1 et PC2 communiquer avec Server dans même LAN.

---

### 3. Router (Routeur)

**Définition :** Équipement Layer 3 (Network) qui interconnecte **différents réseaux** (LANs) et route paquets entre eux.

**Fonction principale :**
- **Router** paquets IP entre réseaux différents
- **Prendre décisions** basées sur adresses IP destination
- **Maintenir** table de routage (routing table)
- **Segmenter** réseaux (broadcast domains séparés)

**Caractéristiques :**
- Moins de ports que switch (2-4+ ports typiquement)
- Chaque interface = **réseau différent** (subnet différent)
- Opère sur **Layer 3** (IP addresses)
- Peut faire **NAT** (Network Address Translation)
- Gateway par défaut pour devices dans LAN

**Différence clé Switch vs Router :**

| Critère | Switch | Router |
|---------|--------|--------|
| **Layer OSI** | Layer 2 (Data Link) | Layer 3 (Network) |
| **Adresses** | MAC addresses | IP addresses |
| **Fonction** | Connecter devices **même** LAN | Connecter **différents** LANs/réseaux |
| **Table** | MAC address table | Routing table |
| **Broadcasts** | Forwarde broadcasts | **Bloque** broadcasts (segmente) |

**Exemple scénario :**
```
LAN 1 (192.168.1.0/24)          Router          LAN 2 (192.168.2.0/24)
PC1 ─ Switch1 ────────────────── [R] ────────────── Switch2 ─ Server
                              /     \
                          Internet  LAN 3
```

---

### 4. Firewall (Pare-feu)

**Définition :** Équipement sécurité qui **filtre** trafic réseau basé sur règles (policies) pour protéger réseau interne.

**Fonction principale :**
- **Bloquer** trafic non-autorisé (entrant/sortant)
- **Autoriser** trafic légitime selon règles
- **Inspecter** paquets (stateful inspection, deep packet inspection)
- **Loguer** connexions et tentatives accès

**Types :**
- **Firewall matériel** (appliance dédiée - Cisco ASA, Palo Alto, Fortinet)
- **Firewall logiciel** (Windows Defender Firewall, iptables Linux)
- **Next-Gen Firewall (NGFW)** : Inspection applicative, IPS, antivirus intégré

**Placement typique :**
```
Internet ─── Firewall ─── Router ─── Switch ─── LAN interne
              (DMZ)                            (Réseau protégé)
```

**Règles exemple :**
- ✅ Autoriser HTTP/HTTPS sortant (ports 80/443)
- ✅ Autoriser SSH entrant uniquement depuis IP admin (port 22)
- ❌ Bloquer tout le reste (deny all implicit)

---

### 5. Wireless Access Point (Point d'Accès Wi-Fi)

**Définition :** Équipement qui permet connexions **sans-fil** (Wi-Fi) des devices au réseau LAN câblé.

**Fonction principale :**
- **Convertir** signaux Wi-Fi ↔ Ethernet câblé
- **Diffuser** SSID (nom réseau Wi-Fi)
- **Authentifier** clients (WPA2/WPA3)
- **Étendre** couverture réseau (pas de câbles)

**Modes :**
- **Standalone AP** : Configuration individuelle (SOHO)
- **Controller-based AP (Lightweight AP)** : Managé centralement par WLC (Wireless LAN Controller) - Entreprise

**Connexion typique :**
```
Devices Wi-Fi )))  Access Point ─── Switch ─── Router ─── Internet
(Laptops, phones)    (convertit)    (LAN)
```

**Note :** AP n'est PAS un routeur (souvent confusion). AP = Layer 2 bridge Wi-Fi ↔ Ethernet.

---

## 🔧 Lab Packet Tracer - Prise en Main

### Objectif Lab

Créer topologie simple avec PC, Switch, Server et les interconnecter.

---

### Étape 1 : Interface Packet Tracer

**Zones principales :**
- **Barre outils gauche** : Catégories équipements (Routers, Switches, End Devices, etc.)
- **Zone centrale** : Workspace (canvas) pour construire topologie
- **Barre outils bas** : Outils connexion (câbles), sélection, déplacement, zoom

---

### Étape 2 : Ajouter équipements

**Actions :**
1. Cliquer **End Devices** (icône PC)
2. Sélectionner **PC-PT** (PC générique)
3. Cliquer dans workspace pour placer → **PC0** créé
4. Répéter pour ajouter **PC1**
5. Cliquer **Servers** → Ajouter **Server-PT** → **Server0**
6. Cliquer **Switches** → Sélectionner **2960-24TT** → Placer dans workspace

**Résultat :**
```
PC0    PC1    Server0

      Switch0
```

---

### Étape 3 : Interconnecter avec câbles

**Outil sélection automatique de connecteur :**
- Icône **éclair** (Lightning bolt) dans barre outils bas
- **Fonction** : Packet Tracer choisit automatiquement type câble approprié (Copper Straight-Through, Crossover, Fiber, etc.)

**Procédure standard (sans astuce) :**
1. Cliquer icône éclair
2. Cliquer sur **PC0** → Sélectionner **FastEthernet0**
3. Cliquer sur **Switch0** → Sélectionner **FastEthernet0/1**
4. Câble créé automatiquement (Copper Straight-Through)
5. **Re-cliquer** icône éclair pour prochaine connexion
6. Répéter pour PC1 et Server0

**🎯 Astuce découverte : Ctrl+Clic**

**Problème :** Après chaque connexion, outil éclair se désélectionne → besoin re-cliquer éclair à chaque fois (fastidieux si 20+ connexions).

**Solution :**
- **Ctrl+Clic** sur icône éclair au lieu de clic simple
- **Résultat** : Outil reste actif entre connexions
- Permet enchaîner connexions sans re-sélectionner outil

**Gain productivité :**
```
Sans Ctrl : Clic éclair → Connexion 1 → Clic éclair → Connexion 2 → ...
Avec Ctrl : Ctrl+Clic éclair → Connexion 1 → Connexion 2 → Connexion 3 → ...
```

---

### Étape 4 : Topologie finale

```
PC0 ────┐
        ├─── Switch0 ─── Server0
PC1 ────┘
```

**Câbles utilisés (auto-détectés) :**
- PC → Switch : **Copper Straight-Through** (câble droit)
- Switch → Server : **Copper Straight-Through**

**Ports connectés :**
- PC0 FastEthernet0 → Switch0 FastEthernet0/1
- PC1 FastEthernet0 → Switch0 FastEthernet0/2
- Server0 FastEthernet0 → Switch0 FastEthernet0/3

---

### Étape 5 : Vérification connexions

**Indicateurs visuels Packet Tracer :**
- **Triangle vert** sur connexion : Lien actif (Layer 1 OK)
- **Triangle orange** : Lien en cours négociation (attendre quelques secondes)
- **Triangle rouge** : Problème connexion (mauvais câble, port down, etc.)

**Vérifier détails connexion :**
- Passer souris sur câble → Tooltip affiche type câble + ports
- Cliquer device → Onglet **Physical** → Voir ports occupés

---

## 💡 Apprentissages Clés

### 1. Prise en main Packet Tracer efficace

**Raccourcis utiles :**
- **Ctrl+Clic** sur outil connexion : Garder outil actif
- **Delete** : Supprimer device/câble sélectionné
- **Ctrl+Z** : Undo
- **Zoom** : Molette souris ou boutons zoom bas-droite

**Organisation workspace :**
- Grouper devices par fonction (clients gauche, servers droite, infrastructure centre)
- Aligner équipements (grille automatique activable)
- Nommer devices explicitement (double-clic → Display Name)

---

### 2. Types câbles réseau (preview)

**Copper Straight-Through (droit) :**
- Usage : **Different device types** (PC ↔ Switch, Switch ↔ Router)
- Pinout : 1-1, 2-2, 3-3, etc. (fils "droits")

**Copper Crossover (croisé) :**
- Usage : **Same device types** (PC ↔ PC, Switch ↔ Switch, Router ↔ Router)
- Pinout : 1-3, 2-6, 3-1, 6-2 (TX/RX croisés)

**Fiber Optic :**
- Usage : Longues distances, haute bande passante
- Types : Single-Mode (long), Multi-Mode (court)

**Auto-MDI/MDIX moderne :**
- Switches/NICs modernes détectent automatiquement et adaptent
- Crossover souvent inutile (mais bon à connaître pour CCNA)

---

### 3. Nomenclature ports Cisco

**Format :** `Type Module/Slot/Port`

**Exemples :**
- **FastEthernet0/1** : FastEthernet, module 0, port 1
- **GigabitEthernet0/0/1** : Gigabit, chassis 0, module 0, port 1
- **Serial0/1/0** : Serial (WAN), module 0, slot 1, port 0

**Types interfaces :**
- **FastEthernet (Fa)** : 100 Mbps
- **GigabitEthernet (Gi)** : 1000 Mbps (1 Gbps)
- **TenGigabitEthernet** : 10 Gbps
- **Serial** : Connexions WAN (leased lines)

---

### 4. Méthodologie construction topologie

**Étapes recommandées :**
1. **Planifier** : Dessiner schéma sur papier avant (optionnel mais utile)
2. **Ajouter infrastructure** : Routers, Switches (backbone)
3. **Ajouter end devices** : PCs, Servers
4. **Câbler** : Interconnecter (Ctrl+Clic astuce!)
5. **Labelliser** : Renommer devices (PC-Sales, SW-Floor2, etc.)
6. **Configurer** : IP addresses, services (prochains labs)
7. **Tester** : Ping, traceroute, simulation mode

---

## 📊 Application Professionnelle

### Architecture réelle petite entreprise

```
                    Internet
                       |
                   Firewall
                       |
                    Router
                    /    \
                   /      \
          Switch Floor1  Switch Floor2
             / | \          / | \
          PC PC PC       PC PC Server
```

**Équipements utilisés :**
- **Firewall** : Protection périmètre (Fortinet, Palo Alto)
- **Router** : Connexion Internet + routing inter-VLANs
- **Switches** : Distribution accès utilisateurs par étage
- **PCs** : Postes employés
- **Server** : File server, AD, databases

**Évolution grandes entreprises :**
- **Core Layer** : Routers/Switches haute capacité (backbone)
- **Distribution Layer** : Agrégation access switches, routing inter-VLANs
- **Access Layer** : Switches connectant end devices

---

## 🔗 Ressources

**Cisco Packet Tracer :**
- [Téléchargement gratuit](https://www.netacad.com/courses/packet-tracer) (via Cisco NetAcad)
- [Tutoriels officiels](https://www.netacad.com/courses/packet-tracer)

**Documentation CCNA :**
- [Cisco CCNA 200-301 Exam Topics](https://learningnetwork.cisco.com/s/ccna-exam-topics)
- Jeremy IT Lab cours complet : Master Cisco CCNA 200-301 (Udemy)

**Labs supplémentaires :**
- Dossier local : `f:\Formation\AutoFormation\Ressources\Jeremy IT - Lab\Days Lab\Day 01\`

---

## 🎓 Points à Retenir

**Équipements clés :**
- **Switch** : Interconnecte devices **même LAN** (Layer 2, MAC addresses)
- **Router** : Interconnecte **différents LANs** (Layer 3, IP addresses)
- **Firewall** : Filtre trafic sécurité
- **Access Point** : Connexions Wi-Fi → LAN câblé

**Packet Tracer :**
- Outil éclair : Auto-sélection câble approprié
- **Ctrl+Clic** éclair : Garder outil actif (gain temps++)
- Triangle vert = Connexion OK

**Prochaine étape (Day 02) :**
- Interfaces et câbles (détails types câbles)
- Configuration basique IP addresses
- Tests connectivité (ping)

---

**Tags :** #CCNA #Networking #PacketTracer #JeremyITLab #NetworkDevices #Fundamentals
