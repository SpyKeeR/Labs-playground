# Jeremy IT CCNA - Day 03 : The OSI Model and TCP/IP Suite

**Date :** 6 janvier 2026  
**Durée :** ~30 minutes  
**Série :** Jeremy IT CCNA (Day 03/53)  
**Ressources :** [Jeremy's IT Lab - Free CCNA Course](https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ)

---

## 🎯 Objectif

Comprendre les **modèles en couches** (OSI et TCP/IP), les organisations de standardisation (IETF, IEEE), l'histoire des protocoles réseau, et le rôle/interaction des couches dans l'encapsulation des données.

---

## 📋 Cours : Layered Models

### Qu'est-ce qu'un modèle réseau ?

**Définition :** Framework conceptuel décrivant comment les données circulent entre applications sur différents équipements réseau.

**Pourquoi des couches ?**
- **Modularité** : Chaque couche responsabilité spécifique (simplification développement)
- **Interopérabilité** : Équipements vendors différents communiquent (respect standards)
- **Troubleshooting** : Isoler problème par couche (Layer 1 câble ? Layer 3 routing ?)
- **Évolution** : Remplacer technologie 1 couche sans toucher autres

**Analogie :** Service postal = couches (rédaction lettre → mise enveloppe → tri postal → transport → distribution).

---

### Modèle vs Standard

**Modèle (Model)** : Cadre conceptuel théorique (guideline, pas implémentation).

**Standard** : Spécification technique précise (RFC, IEEE 802.x) implémentable.

**Exemples :**
- **Modèle OSI** : Théorique ISO (jamais implémenté complètement)
- **Standard TCP/IP** : Implémentation réelle Internet (RFCs IETF)
- **Standard IEEE 802.3** : Spécification Ethernet (câblage, CSMA/CD)

---

### Organisations de standardisation

#### IETF (Internet Engineering Task Force)

- **Rôle** : Développement standards Internet (TCP, IP, HTTP, DNS)
- **Documents** : **RFCs** (Request for Comments)
  * RFC 791 : Internet Protocol (IP)
  * RFC 793 : Transmission Control Protocol (TCP)
  * RFC 2616 : HTTP/1.1
- **Processus** : Open community (propositions publiques, peer review)

**Site :** [https://www.ietf.org](https://www.ietf.org)

---

#### IEEE (Institute of Electrical and Electronics Engineers)

- **Rôle** : Standards réseaux locaux (LAN, WLAN, MAN)
- **Standards :**
  * **802.3** : Ethernet (câblage, CSMA/CD, speeds)
  * **802.11** : WiFi (a/b/g/n/ac/ax)
  * **802.1Q** : VLAN Tagging
  * **802.1X** : Network Access Control (authentification)

**Site :** [https://www.ieee.org](https://www.ieee.org)

---

#### ISO (International Organization for Standardization)

- **Rôle** : Standards internationaux multi-industries
- **Contribution réseaux** : Modèle OSI (1984)
- **Autres standards** : ISO 9001 (qualité), ISO 27001 (sécurité info)

---

### Histoire TCP/IP vs OSI

#### Chronologie

**1969** : ARPANET (ancêtre Internet, US DoD)  
**1974** : TCP/IP développé (Vint Cerf, Bob Kahn)  
**1983** : ARPANET migration vers TCP/IP (**"Flag Day"**)  
**1984** : Modèle OSI publié ISO (concurrent théorique)  
**1990s** : TCP/IP s'impose (Internet explosion commerciale)  

**Résultat :** OSI reste modèle pédagogique (7 couches claires), TCP/IP réalité implémentation (4-5 couches).

---

#### Pourquoi OSI a échoué ?

**Raisons techniques :**
- Développement lent (comités bureaucratiques vs agile IETF)
- Complexité implémentation (overhead protocoles)
- TCP/IP déjà déployé massivement (ARPANET, universités)

**Raisons commerciales :**
- Vendors investis dans TCP/IP (Cisco, Sun, Berkeley UNIX)
- Internet gratuit vs standards ISO payants

**Legacy :** OSI utilisé **vocabulaire** (Layer 2 switching, Layer 3 routing), TCP/IP utilisé **implémentation**.

---

## 📊 Modèle OSI (7 couches)

### Vue d'ensemble

**OSI** = Open Systems Interconnection

| Couche | Nom | Rôle | PDU | Exemples |
|--------|-----|------|-----|----------|
| **7** | Application | Interface utilisateur, services réseau | Data | HTTP, DNS, SMTP |
| **6** | Presentation | Encodage, encryption, compression | Data | SSL/TLS, JPEG, ASCII |
| **5** | Session | Gestion sessions (ouverture/fermeture) | Data | NetBIOS, RPC |
| **4** | Transport | Segmentation, fiabilité (TCP) ou vitesse (UDP) | Segment | TCP, UDP |
| **3** | Network | Routage inter-réseaux (adressage logique IP) | Packet | IP, ICMP, OSPF |
| **2** | Data Link | Trame (adressage physique MAC), accès média | Frame | Ethernet, WiFi 802.11 |
| **1** | Physical | Transmission bits (câbles, signaux électriques) | Bit | RJ45, Fiber, Radio |

**PDU** = Protocol Data Unit (nom données à chaque couche).

---

### Mnémoniques

**Descendant (7→1) :** "**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing"  
**Montant (1→7) :** "**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way"

---

### Détail couches (OSI)

#### Layer 7 : Application

**Rôle :** Interface entre logiciel utilisateur et réseau.

**Protocoles :**
- **HTTP/HTTPS** : Web browsing (port 80/443)
- **DNS** : Résolution noms domaine (port 53)
- **SMTP/POP3/IMAP** : Email (ports 25, 110, 143)
- **FTP** : Transfert fichiers (port 21)
- **SSH** : Remote shell sécurisé (port 22)

**Exemple :** User tape `www.google.com` → DNS résout IP → HTTP GET request.

---

#### Layer 6 : Presentation

**Rôle :** Formatage données (encoding, encryption, compression).

**Fonctions :**
- **Encryption** : SSL/TLS (HTTPS), PGP (email)
- **Encoding** : ASCII, Unicode, EBCDIC
- **Compression** : JPEG (images), MP3 (audio), ZIP

**Exemple :** HTTPS chiffre données HTTP avant envoi (SSL/TLS handshake Layer 6).

---

#### Layer 5 : Session

**Rôle :** Gestion sessions (établissement, maintien, terminaison).

**Fonctions :**
- **Session ID** : Identifier conversation (cookies HTTP)
- **Synchronization** : Checkpoints reprise après interruption
- **Dialog control** : Half-duplex vs Full-duplex

**Protocoles :**
- **NetBIOS** : Windows file sharing
- **RPC** : Remote Procedure Call
- **PPTP** : VPN tunnels

**Exemple :** Connexion SSH = session Layer 5 (persiste durant multiple commandes).

---

#### Layer 4 : Transport

**Rôle :** Segmentation données, fiabilité (TCP) ou vitesse (UDP).

**TCP (Transmission Control Protocol) :**
- **Connection-oriented** : 3-way handshake (SYN, SYN-ACK, ACK)
- **Fiabilité** : Acknowledgements, retransmissions, ordering
- **Flow control** : Windowing (éviter saturation récepteur)
- **Usage** : HTTP, SSH, FTP (données critiques)

**UDP (User Datagram Protocol) :**
- **Connectionless** : Pas handshake (envoi direct)
- **Pas fiabilité** : Pas ACK, pas retransmission
- **Faible latence** : Overhead minimal
- **Usage** : DNS, VoIP, streaming vidéo (tolérance perte paquets)

**Ports :** Multiplex applications (source port, destination port 0-65535).

---

#### Layer 3 : Network

**Rôle :** Routage inter-réseaux (adressage logique IP).

**Protocoles :**
- **IP (Internet Protocol)** : Adressage IPv4/IPv6
- **ICMP** : Messages erreur (ping, traceroute)
- **Routing protocols** : OSPF, EIGRP, BGP

**Fonctions :**
- **Logical addressing** : Adresses IP (192.168.1.10, 2001:db8::1)
- **Path determination** : Choix meilleur chemin (routing table)
- **Packet forwarding** : Router décision next-hop

**PDU :** Packet (IP header + data).

---

#### Layer 2 : Data Link

**Rôle :** Communication directe équipements même réseau (adressage physique MAC).

**Sous-couches :**
- **LLC** (Logical Link Control) : Interfaçage Layer 3
- **MAC** (Media Access Control) : Accès média (CSMA/CD Ethernet)

**Fonctions :**
- **Physical addressing** : Adresses MAC (00:1A:2B:3C:4D:5E)
- **Frame encapsulation** : Ajouter header/trailer (Ethernet frame)
- **Error detection** : FCS (Frame Check Sequence) CRC

**Équipements :** Switch (commutation frames entre ports MAC).

**PDU :** Frame (Ethernet header + IP packet + FCS trailer).

---

#### Layer 1 : Physical

**Rôle :** Transmission bits (signaux électriques, optiques, radio).

**Caractéristiques :**
- **Câbles** : UTP, Fiber, Coaxial
- **Connecteurs** : RJ45, LC, BNC
- **Signaux** : Voltage (copper), Lumière (fiber), Radio (WiFi)
- **Standards** : IEEE 802.3 (Ethernet), 802.11 (WiFi)

**Équipements :** Hub (répéteur signaux), Transceivers.

**PDU :** Bit (0 et 1).

---

## 📊 Modèle TCP/IP (4-5 couches)

### Vue d'ensemble

**TCP/IP Suite** = Implémentation réelle Internet (vs OSI théorique).

| Couche TCP/IP | Équivalent OSI | Rôle | Protocoles |
|---------------|----------------|------|------------|
| **Application** | 7-6-5 (App/Pres/Session) | Services utilisateur | HTTP, DNS, SMTP, FTP |
| **Transport** | 4 (Transport) | Segmentation, fiabilité | TCP, UDP |
| **Internet** | 3 (Network) | Routage IP | IP, ICMP, ARP |
| **Network Access** | 2-1 (Data Link/Physical) | Accès média physique | Ethernet, WiFi |

**Variante 5 couches :** Séparer Network Access → Data Link + Physical (alignement OSI).

---

### Correspondance OSI ↔ TCP/IP

**Simplifications TCP/IP :**
- **Couches 5-6-7 OSI** → 1 couche Application (implémentation apps gère présentation/session)
- **Couches 1-2 OSI** → 1 couche Network Access (abstraction matériel)

**Raison :** Pragmatisme (TCP/IP conçu implementation-first, OSI design-first).

---

## 🔄 Encapsulation et Décapsulation

### Processus Encapsulation (envoi)

**Scénario :** PC1 envoie email (SMTP) vers PC2.

**Étapes descendantes (Layer 7 → 1) :**

```
Layer 7 (Application) :
  User compose email "Hello World"
  SMTP ajoute commandes (MAIL FROM, RCPT TO, DATA)
  → Data

Layer 6 (Presentation) :
  Encode ASCII
  Encrypt TLS (si SMTPS port 465)
  → Data (encoded/encrypted)

Layer 5 (Session) :
  Établit session SMTP (session ID)
  → Data

Layer 4 (Transport) :
  Segment data (si > MTU)
  Ajoute TCP header (source port 49152, dest port 25)
  → Segment (TCP header + data)

Layer 3 (Network) :
  Ajoute IP header (source IP 192.168.1.10, dest IP 203.0.113.5)
  → Packet (IP header + TCP segment)

Layer 2 (Data Link) :
  Ajoute Ethernet header (source MAC, dest MAC gateway)
  Ajoute FCS trailer (CRC error detection)
  → Frame (Ethernet header + IP packet + FCS)

Layer 1 (Physical) :
  Convertir frame en bits
  Transmettre signaux électriques (UTP) ou lumière (fiber)
  → Bits (01010101...)
```

---

### Processus Décapsulation (réception)

**Étapes montantes (Layer 1 → 7) :**

```
Layer 1 (Physical) :
  Recevoir signaux
  Convertir bits → frame
  
Layer 2 (Data Link) :
  Vérifier FCS (si erreur CRC → drop frame)
  Retirer Ethernet header/trailer
  Vérifier dest MAC (si pas match → drop)
  → Packet

Layer 3 (Network) :
  Retirer IP header
  Vérifier dest IP (si pas match → forward ou drop)
  → Segment

Layer 4 (Transport) :
  Retirer TCP header
  Vérifier dest port 25 (SMTP service listening)
  Réassembler segments (si fragmentés)
  Envoyer ACK (TCP reliability)
  → Data

Layer 5 (Session) :
  Maintenir session SMTP
  
Layer 6 (Presentation) :
  Decrypt TLS
  Decode ASCII
  
Layer 7 (Application) :
  SMTP daemon traite email
  Stocker mailbox utilisateur
  → "Hello World" affiché application email
```

---

### Noms PDU (récapitulatif)

| Couche | PDU | Contenu |
|--------|-----|---------|
| Application/Transport | **Data** | Payload applicatif |
| Transport | **Segment** (TCP) ou **Datagram** (UDP) | TCP/UDP header + data |
| Network | **Packet** | IP header + segment |
| Data Link | **Frame** | Ethernet header + packet + FCS |
| Physical | **Bit** | Signaux 0/1 |

**Mnémonique :** "**D**on't **S**ome **P**eople **F**orget **B**irthdays"

---

## 🧪 Lab : Simulation Mode Packet Tracer

### Énoncé

Observer encapsulation/décapsulation en mode **Simulation** Packet Tracer lors d'un ping ICMP entre 2 PCs.

**Topologie :**
```
PC1 (192.168.1.10) ---- Switch ---- PC2 (192.168.1.20)
```

---

### Résolution

**1. Configurer IPs**

PC1 :
```
IP : 192.168.1.10
Mask : 255.255.255.0
Gateway : (laisser vide, même réseau)
```

PC2 :
```
IP : 192.168.1.20
Mask : 255.255.255.0
```

---

**2. Activer mode Simulation**

Interface Packet Tracer :
- Coin inférieur droit : Cliquer **"Simulation"** (vs Realtime)
- Panneau **Event List** apparaît (vide initialement)

---

**3. Envoyer ping**

Depuis PC1 :
```
PC> ping 192.168.1.20
```

**Observation :** Packet Tracer **pause** et affiche enveloppe ICMP.

---

**4. Observer encapsulation (PC1 → PC2)**

Cliquer enveloppe ICMP → Panneau **PDU Information** :

**Outbound PDU Details (Layer 7 → 1) :**

```
Layer 4 (ICMP - considéré Layer 3 mais affiché ici) :
  Type : Echo Request (ping)
  Code : 0
  Identifier : 0x0001
  Sequence : 1

Layer 3 (IP) :
  Source IP : 192.168.1.10
  Dest IP : 192.168.1.20
  Protocol : ICMP (1)
  TTL : 128

Layer 2 (Ethernet) :
  Source MAC : 0001.4251.A3C2 (PC1)
  Dest MAC : 0060.5C8D.12F4 (PC2)
  Type : 0x0800 (IPv4)

Layer 1 (Physical) :
  Port : FastEthernet0
  Signal : Bits transmis
```

---

**5. Observer décapsulation (PC2 réception)**

Cliquer **"Capture/Forward"** plusieurs fois → Enveloppe atteint PC2.

Cliquer enveloppe sur PC2 → **Inbound PDU Details (Layer 1 → 7) :**

```
Layer 1 : Recevoir bits port FastEthernet0
Layer 2 : Retirer Ethernet header, vérifier dest MAC OK
Layer 3 : Retirer IP header, vérifier dest IP 192.168.1.20 OK
Layer 4 : Traiter ICMP Echo Request
Layer 7 : Application ping génère Echo Reply
```

---

**6. Observer réponse (PC2 → PC1)**

PC2 génère **ICMP Echo Reply** (encapsulation inverse) :

```
Layer 4 : ICMP Echo Reply (Type 0)
Layer 3 : IP header (source 192.168.1.20, dest 192.168.1.10)
Layer 2 : Ethernet header (source MAC PC2, dest MAC PC1)
Layer 1 : Bits transmis
```

**Event List** montre timeline complète :
```
1. PC1 → Switch : ICMP Request (Layer 2 frame)
2. Switch → PC2 : Forward frame (switching MAC table)
3. PC2 receive : Décapsulation
4. PC2 → Switch : ICMP Reply
5. Switch → PC1 : Forward reply
6. PC1 receive : Décapsulation reply
```

---

### Vérification

**Commande PC1 :**
```
PC> ping 192.168.1.20

Pinging 192.168.1.20 with 32 bytes of data:

Reply from 192.168.1.20: bytes=32 time<1ms TTL=128
Reply from 192.168.1.20: bytes=32 time<1ms TTL=128
Reply from 192.168.1.20: bytes=32 time<1ms TTL=128
Reply from 192.168.1.20: bytes=32 time<1ms TTL=128

Ping statistics for 192.168.1.20:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

**Succès :** 4 replies → Encapsulation/décapsulation fonctionnelles.

---

## 💡 Apprentissages clés

### Modèle en couches = abstraction

**Avantage développeur :** Programmer app Layer 7 (HTTP) **sans connaître** Layer 1 (fiber vs copper).

**Exemple :** Développeur web écrit `fetch('https://api.example.com')` → Navigateur gère HTTPS (L7), TCP (L4), IP (L3), Ethernet (L2), signaux (L1) automatiquement.

---

### OSI pédagogique, TCP/IP pratique

**Usage professionnel :**
- **Troubleshooting** : "Problème Layer 2" (VLAN, STP) vs "Problème Layer 3" (routing, ACL)
- **Certifications** : CCNA utilise vocabulaire OSI (même si TCP/IP implémenté)
- **Documentation** : RFCs utilisent terminologie OSI (bien que standards TCP/IP)

**Exemple troubleshooting :**
```
Ping échoue PC1 → PC2 ?
1. Layer 1 : Câble branché ? LED port verte ?
2. Layer 2 : MAC address table switch contient MAC PC2 ?
3. Layer 3 : Routing table contient route vers 192.168.1.0/24 ?
4. Layer 4 : Firewall bloque ICMP ?
```

---

### Encapsulation = headers empilés

**Analogie courrier postal :**
- **Lettre** = Data (Layer 7)
- **Enveloppe** = TCP header (Layer 4, adresse port)
- **Colis postal** = IP header (Layer 3, adresse IP)
- **Camion postal** = Ethernet frame (Layer 2, adresse MAC)
- **Route physique** = Fiber optic (Layer 1)

Chaque couche **ajoute header** (encapsulation descendante), **retire header** (décapsulation montante).

---

### Adjacent-layer vs Same-layer interaction

**Adjacent-layer (vertical) :**
- Communication entre couches **même équipement**
- Exemple : Layer 7 HTTP passe data à Layer 4 TCP

**Same-layer (horizontal) :**
- Communication entre couches **équipements distants**
- Exemple : TCP source (PC1 Layer 4) dialogue avec TCP destination (PC2 Layer 4) via headers

**Diagramme :**
```
PC1 Layer 7 ─────────────────── PC2 Layer 7  (same-layer)
    ↓ (adjacent)                    ↑
PC1 Layer 4 ─────────────────── PC2 Layer 4  (same-layer)
    ↓                               ↑
PC1 Layer 1 ── câble physique ── PC2 Layer 1  (same-layer)
```

---

### Protocoles vs Couches

**1 protocole ≠ 1 couche :**
- **ARP** : Layer 2 (MAC) mais utilise IP (Layer 3 info) → **"Layer 2.5"**
- **ICMP** : Layer 3 (IP) mais pas routage (diagnostic) → Network layer mais pas routing
- **DNS** : Layer 7 mais utilise UDP (Layer 4 port 53)

**Conclusion :** Modèles = guidelines, réalité = protocoles chevauchent couches.

---

## 🏢 Application professionnelle

### Troubleshooting méthodique (approche couches)

**Scénario :** User "Je n'accède pas au site web interne http://intranet.company.local".

**Approche bottom-up (Layer 1 → 7) :**

```
Layer 1 (Physical) :
  - Câble Ethernet branché PC ? LED verte ?
  - Port switch actif ? (show interface status)
  → OK : Passer Layer 2

Layer 2 (Data Link) :
  - PC obtient adresse MAC gateway ? (arp -a)
  - VLAN correct ? (show vlan brief sur switch)
  → OK : Passer Layer 3

Layer 3 (Network) :
  - PC a IP valide ? (ipconfig, ip a)
  - Gateway pingable ? (ping 192.168.1.1)
  - DNS résout intranet.company.local ? (nslookup)
  → OK : Passer Layer 4

Layer 4 (Transport) :
  - Port 80 ouvert serveur ? (telnet intranet.company.local 80)
  - Firewall bloque TCP 80 ? (show access-list)
  → OK : Passer Layer 7

Layer 7 (Application) :
  - Service HTTP running ? (systemctl status httpd)
  - VirtualHost configuré ? (apachectl -S)
  - Logs erreurs ? (tail /var/log/httpd/error_log)
```

**Résultat :** DNS ne résout pas (Layer 3) → Vérifier /etc/resolv.conf ou serveur DNS.

---

### Design réseau entreprise (séparation couches)

**Architecture 3-tier datacenter :**

```
Layer 3 (Core) :
  - Routers Cisco ASR 9000
  - Routing OSPF inter-VLANs
  - BGP externe (ISPs)

Layer 2 (Distribution) :
  - Switches L3 Cisco Catalyst 9500
  - VLANs (VLAN 10 Admin, VLAN 20 Devs, VLAN 30 Users)
  - HSRP (High availability gateway)

Layer 1 (Access) :
  - Switches L2 Cisco Catalyst 9200
  - PoE (IP phones, WiFi APs)
  - 48 ports 1G + 4 uplinks 10G fiber
```

**Avantage modularité :** Changer Access switches (Layer 1-2) sans toucher Core routing (Layer 3).

---

### Sécurité par couche (Defense in Depth)

**Principe :** Protections à **chaque couche** (si 1 échoue, autres bloquent).

```
Layer 7 : WAF (Web Application Firewall) - Bloquer injections SQL
Layer 4 : Firewall règles ports (autoriser 80/443, bloquer reste)
Layer 3 : ACL (Access Control Lists) - Bloquer IPs malveillantes
Layer 2 : Port security - Limiter MAC addresses par port switch
Layer 1 : Physique - Datacenter accès biométrique
```

**Exemple attaque :**
1. Attaquant tente SQL injection (Layer 7) → **WAF bloque**
2. Si WAF contourné, firewall voit port 3306 MySQL non autorisé → **Firewall bloque**
3. Si firewall contourné, ACL voit IP source blacklist → **ACL bloque**

**Résultat :** 3 barrières indépendantes (defense in depth).

---

## ❌ Difficultés rencontrées

### Aucune (rappel concepts)

**Feedback :** Cours Jeremy IT clair, mode simulation Packet Tracer visualise encapsulation excellemment.

**Note :** Notions OSI/TCP/IP déjà abordées formations précédentes (BTS SIO, TSSR) → Juste **piqûre de rappel**.

---

## 🔗 Ressources

- **Jeremy's IT Lab Day 03** : [OSI Model & TCP/IP Suite](https://www.youtube.com/watch?v=t-ai8JzhHuY&list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ&index=3)
- **IETF RFCs** : [https://www.rfc-editor.org](https://www.rfc-editor.org)
- **IEEE Standards** : [https://standards.ieee.org](https://standards.ieee.org)
- **Cisco Learning Network** : [OSI Model Deep Dive](https://learningnetwork.cisco.com)

---

## 📝 Commandes à retenir

### Packet Tracer - Mode Simulation

```
1. Basculer Realtime → Simulation (coin inférieur droit)
2. Envoyer traffic (ping, HTTP request)
3. Cliquer enveloppe → PDU Information
4. Observer Outbound/Inbound PDU Details (couches)
5. Capture/Forward (step-by-step) ou Auto Capture (play button)
```

### Troubleshooting approche couches

```
Layer 1 : show interfaces status, show controllers
Layer 2 : show mac address-table, show vlan brief
Layer 3 : show ip route, show ip interface brief
Layer 4 : show access-list, netstat -an
Layer 7 : show processes, debug http
```

---

**Note :** Fondations solides OSI/TCP/IP essentielles pour Days suivants (switching, routing, ACLs).

**Prochaine étape :** Day 04 - Introduction to the CLI (Cisco IOS commands).
