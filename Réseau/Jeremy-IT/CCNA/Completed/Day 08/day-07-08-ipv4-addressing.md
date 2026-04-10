# Lab : IPv4 Addressing (Day 07-08)

**Date** : 7 janvier 2026  
**Source** : Jeremy's IT Lab - CCNA (Day 07-08)  
**Sujet** : IPv4 Addressing  

---

## 🎯 Objectif

Configurer les adresses IPv4 sur un routeur et des PCs, vérifier la connectivité réseau.

---

## 📋 Énoncé du lab

**Topologie** :
- 1 routeur (R1)
- 3 switches (SW1, SW2, SW3)
- 3 PCs (PC1, PC2, PC3)

**Tâches** :

1. Configurer le hostname de R1
2. Afficher la liste des interfaces de R1, leurs adresses IP et statuts
3. Configurer les adresses IP sur les interfaces de R1 et les activer (avec descriptions)
4. Vérifier à nouveau les interfaces de R1
5. Sauvegarder la configuration
6. Configurer les adresses IP des PCs
7. Tester la connectivité (pings PC1 → PC2, PC1 → PC3)

---

## ✅ Résolution

### 1. Configuration du hostname

```bash
R1> enable
R1# configure terminal
R1(config)# hostname R1
```

### 2. Vérifier les interfaces (état initial)

```bash
R1# show ip interface brief
```

**Sortie attendue** : Interfaces down/down (pas d'IP configurée).

### 3. Configuration des interfaces

**Interface GigabitEthernet 0/0 (vers SW1)** :

```bash
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 15.255.255.254 255.0.0.0
R1(config-if)# description ## R1 TO SW1 ##
R1(config-if)# no shutdown
```

**Interface GigabitEthernet 0/1 (vers SW2)** :

```bash
R1(config-if)# interface GigabitEthernet0/1
R1(config-if)# ip address 182.98.255.254 255.255.0.0
R1(config-if)# description ## R1 TO SW2 ##
R1(config-if)# no shutdown
```

**Interface GigabitEthernet 0/2 (vers SW3)** :

```bash
R1(config-if)# interface GigabitEthernet0/2
R1(config-if)# ip address 201.191.20.254 255.255.255.0
R1(config-if)# description ## R1 TO SW3 ##
R1(config-if)# no shutdown
```

**Explication** :
- `ip address` : Configure l'adresse IP et le masque de sous-réseau
- `description` : Ajoute une description (documentation)
- `no shutdown` : Active l'interface (état `up/up` si câblé correctement)

### 4. Vérification des interfaces

```bash
R1# show ip interface brief
```

**Sortie attendue** : Interfaces up/up avec adresses IP configurées.

### 5. Sauvegarder la configuration

```bash
R1# show running-config
R1# copy running-config startup-config
```

**Explication** :
- `show running-config` : Affiche la configuration active (RAM)
- `copy run start` : Copie la running-config vers startup-config (NVRAM, persistante au reboot)

### 6. Configuration des PCs

**Méthode** : Desktop Tab → IP Configuration

**PC1** (connecté à SW1) :
- IP Address : `15.0.0.1`
- Subnet Mask : `255.0.0.0`
- Default Gateway : `15.255.255.254` (IP de R1 G0/0)

**PC2** (connecté à SW2) :
- IP Address : `182.98.0.1`
- Subnet Mask : `255.255.0.0`
- Default Gateway : `182.98.255.254` (IP de R1 G0/1)

**PC3** (connecté à SW3) :
- IP Address : `201.191.20.1`
- Subnet Mask : `255.255.255.0`
- Default Gateway : `201.191.20.254` (IP de R1 G0/2)

### 7. Test de connectivité

**Depuis PC1** :

```bash
ping 182.98.0.1    # PC2
ping 201.191.20.1  # PC3
```

**Résultat attendu** : Réponses reçues (TTL, time).

**Explication** : Le routeur R1 route les paquets entre les 3 réseaux distincts (15.0.0.0/8, 182.98.0.0/16, 201.191.20.0/24).

---

## 📌 Commandes clés

| Commande | Usage |
|----------|-------|
| `show ip interface brief` | Afficher résumé interfaces (IP, statut) |
| `interface INTERFACE` | Entrer en mode configuration d'interface |
| `ip address IP MASK` | Configurer adresse IPv4 |
| `description TEXT` | Ajouter description interface |
| `no shutdown` | Activer interface |
| `show running-config` | Afficher configuration active (RAM) |
| `copy run start` | Sauvegarder configuration (NVRAM) |

---

## 🏷️ Tags

`#CCNA` `#IPv4` `#Routing` `#CiscoIOS` `#PacketTracer` `#JeremyITLab`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
