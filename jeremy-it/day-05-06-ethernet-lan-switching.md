# Lab : Ethernet LAN Switching (Day 05-06)

**Date** : 7 janvier 2026  
**Source** : Jeremy's IT Lab - CCNA (Day 05-06)  
**Sujet** : Ethernet LAN Switching  

---

## 🎯 Objectif

Comprendre le fonctionnement des tables MAC des switches et le processus ARP dans un réseau local Ethernet.

---

## 📋 Énoncé du lab

**Topologie** :
- 2 switches (SW1, SW2) avec tables MAC vides
- 4 PCs (PC1, PC2, PC3, PC4) avec tables ARP vides

**Tâches** :

1. Si PC1 ping PC3, quels messages seront envoyés et quels périphériques les recevront ?
2. Vérifier avec le mode simulation de Packet Tracer
3. Générer du trafic pour permettre aux switches d'apprendre les adresses MAC
4. Identifier l'adresse MAC de chaque PC via commandes `show`
5. Effacer les adresses MAC dynamiques des switches

---

## ✅ Résolution

### 1. Analyse théorique du ping PC1 → PC3

**Messages attendus** :

**Phase 1 - ARP Request (PC1 ne connaît pas MAC de PC3)** :
- PC1 broadcast ARP Request : "Qui a l'IP de PC3 ?"
- **Reçu par** : Tous les périphériques du même réseau (PC2, PC3, PC4, SW1, SW2)

**Phase 2 - ARP Reply** :
- PC3 répond unicast à PC1 avec son adresse MAC
- **Reçu par** : PC1 uniquement (+ switches apprennent MAC PC3)

**Phase 3 - ICMP Echo Request/Reply (Ping)** :
- PC1 → PC3 : ICMP Echo Request (unicast)
- PC3 → PC1 : ICMP Echo Reply (unicast)
- **Reçu par** : PC1 et PC3 uniquement

### 2. Vérification en mode simulation

**Procédure** :
1. Ouvrir Packet Tracer
2. Cliquer sur **Simulation Mode** (icône chronomètre en bas à droite)
3. Exécuter ping depuis PC1 : `ping <IP_PC3>`
4. Observer étape par étape :
   - ARP Request en broadcast (propagation à tous les PCs)
   - ARP Reply en unicast (PC3 → PC1)
   - ICMP Echo Request/Reply (PC1 ↔ PC3 uniquement)

**Résultat** : Correspond à l'analyse théorique.

### 3. Apprendre les adresses MAC

Générer du trafic depuis chaque PC :

```bash
# Depuis PC1
ping <IP_PC2>
ping <IP_PC3>
ping <IP_PC4>

# Depuis PC2
ping <IP_PC1>
ping <IP_PC3>

# Répéter pour PC3 et PC4
```

**Explication** : Chaque ping génère du trafic Ethernet, permettant aux switches d'apprendre les adresses MAC sources et les interfaces associées.

### 4. Identifier les adresses MAC

Sur chaque switch :

```bash
SW1# show mac address-table dynamic
SW2# show mac address-table dynamic
```

**Sortie exemple** :
```
Mac Address Table
-------------------------------------------
Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
1       0001.C7A4.6101    DYNAMIC     Fa0/1
1       0002.1634.8A01    DYNAMIC     Fa0/2
```

**Explication** :
- **Vlan** : VLAN auquel appartient l'entrée (défaut = 1)
- **Mac Address** : Adresse MAC apprise
- **Type** : `DYNAMIC` (apprise automatiquement) vs `STATIC` (configurée manuellement)
- **Ports** : Interface physique où l'adresse a été vue

### 5. Effacer les entrées dynamiques

Sur chaque switch :

```bash
SW1# clear mac address-table dynamic
SW2# clear mac address-table dynamic
```

**Vérification** :
```bash
SW1# show mac address-table dynamic
```

**Résultat** : Table vide (switches réapprendront au prochain trafic).

---

## 📌 Commandes clés

| Commande | Usage |
|----------|-------|
| `show mac address-table dynamic` | Afficher adresses MAC apprises dynamiquement |
| `clear mac address-table dynamic` | Effacer toutes les entrées dynamiques |
| `show mac address-table` | Afficher table complète (dynamic + static) |

---

## 🏷️ Tags

`#CCNA` `#Ethernet` `#Switching` `#MACTable` `#ARP` `#PacketTracer` `#JeremyITLab`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
