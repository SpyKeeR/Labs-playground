# Day 13-14-15 : Subnetting & VLSM (Variable Length Subnet Masking)

**Date** : 10 janvier 2026  
**Source** : Jeremy's IT Lab - Free CCNA 200-301  
**Type** : Cours théorique + Lab pratique  
**Difficulté** : ⭐⭐ (Niveau intermédiaire)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

**Cours (Days 13-14-15)** : Théorie subnetting (révision concepts déjà maîtrisés)

**Lab pratique** : Concevoir plan d'adressage VLSM pour réseau 192.168.5.0/24 avec besoins variés + configurer static routing pour connectivité complète.

---

## 📋 Énoncé Lab

**Réseau à subnetter** : `192.168.5.0/24`

**Topologie** :
```
[PC1] --- [R1-G0/0] --- (LAN 1: 45 hosts)
          [R1-G0/1] --- (LAN 2: 64 hosts)
          [R1-G0/2] --- [R2-G0/2] (P2P WAN: 2 hosts)
                        [R2-G0/0] --- (LAN 3: 14 hosts) --- [PC3]
                        [R2-G0/1] --- (LAN 4: 9 hosts) --- [PC4]
```

**Besoins adressage** :
- LAN 1 : 45 hosts
- LAN 2 : 64 hosts
- LAN 3 : 14 hosts
- LAN 4 : 9 hosts
- P2P WAN (R1-R2) : 2 hosts

**Contraintes** :
1. Subnet the 192.168.5.0/24 network to provide sufficient addressing for each LAN
2. Assign the **first usable address** to the PC in each LAN
3. Assign the **last usable address** to the router's interface in each LAN
4. Configure static routes on each router so that all PCs can ping eachother

---

## 🔧 Résolution

### Étape 1 : Plan d'adressage VLSM

**Méthode** : Trier réseaux par taille décroissante (plus grand → plus petit) pour optimiser allocation.

**Ordre allocation** :
1. LAN 2 : 64 hosts → /25 (126 hosts utilisables)
2. LAN 1 : 45 hosts → /26 (62 hosts utilisables)
3. LAN 3 : 14 hosts → /28 (14 hosts utilisables)
4. LAN 4 : 9 hosts → /28 (14 hosts utilisables)
5. P2P WAN : 2 hosts → /30 (2 hosts utilisables)

**Plan VLSM final** :

| LAN | Besoins | Subnet | Masque | Première IP | Dernière IP | Broadcast |
|-----|---------|--------|--------|-------------|-------------|-----------|
| LAN 2 | 64 hosts | 192.168.5.0/25 | 255.255.255.128 | 192.168.5.1 | 192.168.5.126 | 192.168.5.127 |
| LAN 1 | 45 hosts | 192.168.5.128/26 | 255.255.255.192 | 192.168.5.129 | 192.168.5.190 | 192.168.5.191 |
| LAN 3 | 14 hosts | 192.168.5.192/28 | 255.255.255.240 | 192.168.5.193 | 192.168.5.206 | 192.168.5.207 |
| LAN 4 | 9 hosts | 192.168.5.208/28 | 255.255.255.240 | 192.168.5.209 | 192.168.5.222 | 192.168.5.223 |
| P2P WAN | 2 hosts | 192.168.5.224/30 | 255.255.255.252 | 192.168.5.225 | 192.168.5.226 | 192.168.5.227 |

**IP restantes** : 192.168.5.228 - 192.168.5.255 (28 addresses libres pour croissance future)

### Étape 2 : Configuration adresses IP

**LAN 2 (192.168.5.0/25)** :
```
PC2 : 192.168.5.1 (première utilisable)
R1 G0/1 : 192.168.5.126 (dernière utilisable)
Masque : 255.255.255.128
```

**LAN 1 (192.168.5.128/26)** :
```
PC1 : 192.168.5.129 (première utilisable)
R1 G0/0 : 192.168.5.190 (dernière utilisable)
Masque : 255.255.255.192
```

**LAN 3 (192.168.5.192/28)** :
```
PC3 : 192.168.5.193 (première utilisable)
R2 G0/0 : 192.168.5.206 (dernière utilisable)
Masque : 255.255.255.240
```

**LAN 4 (192.168.5.208/28)** :
```
PC4 : 192.168.5.209 (première utilisable)
R2 G0/1 : 192.168.5.222 (dernière utilisable)
Masque : 255.255.255.240
```

**P2P WAN (192.168.5.224/30)** :
```
R1 G0/2 : 192.168.5.225
R2 G0/2 : 192.168.5.226
Masque : 255.255.255.252
```

### Étape 3 : Configuration static routes

**Objectif** : Permettre tous PCs se pinguer mutuellement.

**Router R1** :
```
R1(config)#ip route 192.168.5.192 255.255.255.240 192.168.5.226
R1(config)#ip route 192.168.5.208 255.255.255.240 192.168.5.226
```

**Explication R1** :
- Route vers LAN 3 (192.168.5.192/28) via next-hop R2 (192.168.5.226)
- Route vers LAN 4 (192.168.5.208/28) via next-hop R2 (192.168.5.226)

**Router R2** :
```
R2(config)#ip route 192.168.5.128 255.255.255.192 192.168.5.225
R2(config)#ip route 192.168.5.0 255.255.255.128 192.168.5.225
```

**Explication R2** :
- Route vers LAN 1 (192.168.5.128/26) via next-hop R1 (192.168.5.225)
- Route vers LAN 2 (192.168.5.0/25) via next-hop R1 (192.168.5.225)

### Étape 4 : Workflow VLSM (méthode générale)

1. **Lister besoins** : Réseaux + nombre hosts
2. **Calculer masques** : Hosts requis → masque approprié (/25, /26, /28, /30)
3. **Trier décroissant** : Plus grand réseau → plus petit (éviter fragmentation)
4. **Allouer séquentiellement** : Première adresse réseau disponible
5. **Assigner IPs** : Première utilisable (PC), dernière utilisable (routeur)
6. **Configurer routes** : Static routes pour interconnecter réseaux

---

## ✅ Validation

**Tests connectivité** :
```
PC1> ping 192.168.5.1       # PC1 → PC2 (via R1)
PC1> ping 192.168.5.193     # PC1 → PC3 (via R1 → R2)
PC1> ping 192.168.5.209     # PC1 → PC4 (via R1 → R2)

PC3> ping 192.168.5.129     # PC3 → PC1 (via R2 → R1)
PC3> ping 192.168.5.1       # PC3 → PC2 (via R2 → R1)
PC3> ping 192.168.5.209     # PC3 → PC4 (via R2)
```

**Vérifications routeurs** :
```
R1#show ip route
# Doit afficher :
# C    192.168.5.0/25 is directly connected, GigabitEthernet0/1
# C    192.168.5.128/26 is directly connected, GigabitEthernet0/0
# C    192.168.5.224/30 is directly connected, GigabitEthernet0/2
# S    192.168.5.192/28 [1/0] via 192.168.5.226
# S    192.168.5.208/28 [1/0] via 192.168.5.226

R2#show ip route
# Doit afficher :
# S    192.168.5.0/25 [1/0] via 192.168.5.225
# S    192.168.5.128/26 [1/0] via 192.168.5.225
# C    192.168.5.192/28 is directly connected, GigabitEthernet0/0
# C    192.168.5.208/28 is directly connected, GigabitEthernet0/1
# C    192.168.5.224/30 is directly connected, GigabitEthernet0/2
```

---

## 📌 Commandes utiles

### Calcul masques subnets

```bash
# Hosts requis → Masque
# 2^n - 2 >= hosts requis (n = bits host)

# 64 hosts → 2^7 - 2 = 126 ≥ 64 → /25 (32-7=25)
# 45 hosts → 2^6 - 2 = 62 ≥ 45 → /26
# 14 hosts → 2^4 - 2 = 14 ≥ 14 → /28
# 9 hosts → 2^4 - 2 = 14 ≥ 9 → /28
# 2 hosts → 2^2 - 2 = 2 ≥ 2 → /30
```

### Configuration routeurs

```bash
# Assigner IP interface
Router(config)#interface g0/0
Router(config-if)#ip address 192.168.5.190 255.255.255.192
Router(config-if)#no shutdown

# Ajouter static route
Router(config)#ip route <réseau> <masque> <next-hop>

# Vérifier routes
Router#show ip route
Router#show ip route static

# Vérifier interfaces
Router#show ip interface brief

# Tester connectivité
Router#ping 192.168.5.193
```

### Calcul subnets (méthode rapide)

```bash
# Masque /25 = 255.255.255.128
# Block size = 256 - 128 = 128
# Subnets : 0, 128 (2 subnets)

# Masque /26 = 255.255.255.192
# Block size = 256 - 192 = 64
# Subnets : 0, 64, 128, 192 (4 subnets)

# Masque /28 = 255.255.255.240
# Block size = 256 - 240 = 16
# Subnets : 0, 16, 32, ..., 240 (16 subnets)

# Masque /30 = 255.255.255.252
# Block size = 256 - 252 = 4
# Subnets : 0, 4, 8, 12, ..., 252 (64 subnets)
```

---

## 💡 Points clés

**VLSM avantages** :
- Optimise utilisation adresses IP (pas de gaspillage)
- Flexibilité besoins variés (14 hosts et 64 hosts même réseau parent)
- Scalabilité (IP libres pour croissance future)

**Erreurs évitées** :
- Allouer dans désordre → fragmentation espace adressage
- Oublier trier décroissant → bloquer allocation réseaux plus grands
- Utiliser broadcast/network comme IP host → erreur config

**Optimisation** :
- P2P links toujours /30 (2 hosts exactement)
- LANs : masque juste suffisant (pas /24 pour 9 hosts)
- Conserver IP contiguës pour agrégation routes future

---

**Tags** : `VLSM` `subnetting` `static-routing` `CCNA` `IPv4` `network-design` `Jeremy-IT-Lab`
