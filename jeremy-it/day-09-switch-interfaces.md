# Lab : Switch Interfaces (Day 09)

**Date** : 7 janvier 2026  
**Source** : Jeremy's IT Lab - CCNA (Day 09)  
**Sujet** : Switch Interfaces Configuration  

---

## 🎯 Objectif

Configurer les interfaces d'un switch (speed, duplex, descriptions) et désactiver les ports inutilisés.

---

## 📋 Énoncé du lab

**Topologie** :
- 1 routeur (R1)
- 2 switches (SW1, SW2)
- 4 PCs (PC1, PC2, PC3, PC4)

**Tâches** :

1. Configurer le hostname de R1, SW1 et SW2
2. Configurer les adresses IP sur R1 et les PCs
3. Configurer manuellement speed et duplex sur interfaces connectées à d'autres équipements réseau (pas end hosts)
4. Configurer des descriptions sur chaque interface
5. Désactiver les interfaces non connectées

---

## ✅ Résolution

### 1. Configuration des hostnames

```bash
# Routeur
Router> enable
Router# configure terminal
Router(config)# hostname R1

# Switch 1
Switch> enable
Switch# configure terminal
Switch(config)# hostname SW1

# Switch 2
Switch> enable
Switch# configure terminal
Switch(config)# hostname SW2
```

### 2. Configuration IP

**Sur R1** :

```bash
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 172.16.255.254 255.255.0.0
R1(config-if)# no shutdown
```

**Sur PCs** : Desktop Tab → IP Configuration (adresses du réseau 172.16.0.0/16, gateway 172.16.255.254)

### 3. Configuration speed et duplex

**Sur SW1 (interfaces FastEthernet vers autres switches)** :

```bash
SW1(config)# interface FastEthernet0/1
SW1(config-if)# speed 100
SW1(config-if)# duplex full

SW1(config-if)# interface FastEthernet0/2
SW1(config-if)# speed 100
SW1(config-if)# duplex full
```

**Sur SW1 (interface GigabitEthernet vers routeur)** :

```bash
SW1(config)# interface GigabitEthernet0/1
SW1(config-if)# speed 1000
SW1(config-if)# duplex full
```

**Sur SW2** : Répéter pour interfaces interconnectées.

**Explication** :
- **Speed** : Vitesse de l'interface (10, 100, 1000 Mbps, ou `auto`)
- **Duplex** : Mode half (1 sens à la fois) ou full (2 sens simultanés), ou `auto`
- **Autonegotiation** : Si un côté en `auto` et l'autre manuel → mismatch possible (erreurs, CRC)
- **Bonnes pratiques** : Configuration manuelle sur liens switch-switch, switch-routeur (performances prévisibles)

**⚠️ Découverte** : Les PCs en mode autonegotiation ne supportent pas une configuration manuelle côté switch (mismatch duplex → erreurs). Laisser en `auto` pour interfaces vers end hosts.

### 4. Configuration des descriptions

**Sur SW1** :

```bash
SW1(config)# interface FastEthernet0/1
SW1(config-if)# description ## TO SW2 ##

SW1(config-if)# interface GigabitEthernet0/1
SW1(config-if)# description ## TO R1 G0/0 ##

SW1(config-if)# interface FastEthernet0/3
SW1(config-if)# description ## TO PC1 ##
```

**Sur SW2** : Répéter pour chaque interface connectée.

**Explication** : Les descriptions facilitent la documentation et le troubleshooting (visible dans `show interface`, `show ip interface brief`, `show run`).

### 5. Désactivation des interfaces inutilisées

**Sur SW1** :

```bash
SW1(config)# interface range FastEthernet0/3-24
SW1(config-if-range)# shutdown
```

**Explication** :
- `interface range` : Configure plusieurs interfaces simultanément
- `shutdown` : Désactive administrativement l'interface (sécurité : empêche connexion non autorisée)

**Vérification** :

```bash
SW1# show ip interface brief
```

**Résultat attendu** : Interfaces inutilisées en état `administratively down`.

---

## 📌 Commandes clés

| Commande | Usage |
|----------|-------|
| `speed {10\|100\|1000\|auto}` | Configurer vitesse interface |
| `duplex {half\|full\|auto}` | Configurer mode duplex |
| `description TEXT` | Ajouter description interface |
| `interface range RANGE` | Configurer plusieurs interfaces (ex: Fa0/1-10) |
| `shutdown` | Désactiver interface |
| `no shutdown` | Activer interface |
| `show interfaces status` | Afficher statut, speed, duplex de toutes les interfaces |

---

## 🏷️ Tags

`#CCNA` `#Switching` `#InterfaceConfiguration` `#Duplex` `#CiscoIOS` `#PacketTracer` `#JeremyITLab`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
