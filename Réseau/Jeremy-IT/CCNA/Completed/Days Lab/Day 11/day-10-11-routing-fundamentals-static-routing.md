# Day 11 : Routing Fundamentals & Static Routing

**Date** : 8 janvier 2026  
**Plateforme** : Jeremy's IT Lab - CCNA 200-301  
**Cours Udemy** : Master Cisco CCNA 200-301  

---

## 🎯 Objectifs

- Comprendre fonctionnement routing IP (Layer 3)
- Maîtriser configuration routes statiques Cisco IOS
- Troubleshooter problèmes routing (next-hop, interfaces)

---

## 📋 Cours : Routing Fundamentals

**Rappels routing Layer 3 :**
- Routeurs forward packets entre réseaux différents (Layer 3)
- Table de routage : chemins vers destinations
- Décision basée sur adresse IP destination

**Déjà acquis** : Concepts de base routing connus.

---

## 📋 Cours : Static Routing

**Commande Cisco IOS** : `ip route`

**Syntaxe** :
```
ip route <DESTINATION_NETWORK> <SUBNET_MASK> <NEXT_HOP_IP | EXIT_INTERFACE>
```

**Exemple next-hop IP** :
```
ip route 192.168.3.0 255.255.255.0 192.168.12.2
```
- `192.168.3.0` : Réseau destination
- `255.255.255.0` : Masque réseau
- `192.168.12.2` : Adresse IP next-hop (routeur suivant)

**Exemple exit interface** :
```
ip route 192.168.3.0 255.255.255.0 GigabitEthernet0/1
```
- `GigabitEthernet0/1` : Interface sortie (moins recommandé)

**Rappels importants** :
- Préférer next-hop IP (plus fiable, supporte multi-access networks)
- Exit interface : uniquement réseaux point-to-point
- Vérifier table routing : `show ip route`

---

## 🛠️ Lab 1 : Configuring Static Routes

### Topologie

```
PC1 (192.168.1.1) --- [R1] --- [R2] --- [R3] --- PC2 (192.168.3.1)
     192.168.1.0/24    |       |        |      192.168.3.0/24
                  192.168.12.0/24  192.168.13.0/24
```

**Réseaux** :
- LAN PC1 : `192.168.1.0/24` (gateway R1 .254)
- Interconnexion R1-R2 : `192.168.12.0/24`
- Interconnexion R2-R3 : `192.168.13.0/24`
- LAN PC2 : `192.168.3.0/24` (gateway R3 .254)

### Consigne

1. Configurer PCs et routeurs (hostnames, IP addresses)
2. Configurer gateway sur PCs
3. Configurer routes statiques pour permettre PC1 ping PC2

### Résolution

#### Configuration PCs

**PC1** (Desktop Tab → IP Configuration) :
- IP : `192.168.1.1`
- Mask : `255.255.255.0`
- Gateway : `192.168.1.254`

**PC2** (Desktop Tab → IP Configuration) :
- IP : `192.168.3.1`
- Mask : `255.255.255.0`
- Gateway : `192.168.3.254`

#### Configuration R1

```
hostname R1

interface GigabitEthernet0/0
 ip address 192.168.12.1 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 192.168.1.254 255.255.255.0
 no shutdown

ip route 192.168.13.0 255.255.255.0 192.168.12.2
ip route 192.168.3.0 255.255.255.0 192.168.12.2
```

**Explication routes** :
- Route vers `192.168.13.0` (interconnexion R2-R3) via `192.168.12.2` (R2)
- Route vers `192.168.3.0` (LAN PC2) via `192.168.12.2` (R2)

#### Configuration R2

```
hostname R2

interface GigabitEthernet0/0
 ip address 192.168.12.2 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 192.168.13.2 255.255.255.0
 no shutdown

ip route 192.168.1.0 255.255.255.0 192.168.12.1
ip route 192.168.3.0 255.255.255.0 192.168.13.3
```

**Explication routes** :
- Route vers `192.168.1.0` (LAN PC1) via `192.168.12.1` (R1)
- Route vers `192.168.3.0` (LAN PC2) via `192.168.13.3` (R3)

#### Configuration R3

```
hostname R3

interface GigabitEthernet0/0
 ip address 192.168.13.3 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 192.168.3.254 255.255.255.0
 no shutdown

ip route 192.168.12.0 255.255.255.0 192.168.13.2
ip route 192.168.1.0 255.255.255.0 192.168.13.2
```

**Explication routes** :
- Route vers `192.168.12.0` (interconnexion R1-R2) via `192.168.13.2` (R2)
- Route vers `192.168.1.0` (LAN PC1) via `192.168.13.2` (R2)

#### Validation

```
PC1> ping 192.168.3.1
```

**Résultat** : Success (ICMP Echo Reply)

---

## 🛠️ Lab 2 : Troubleshooting Static Routes

### Consigne

PC1 et PC2 ne peuvent pas se pinguer. **Une erreur de configuration par routeur**. Trouver et corriger.

### Diagnostic

#### R1 : show ip route

```
R1# show ip route
...
S    192.168.3.0/24 [1/0] via 192.168.12.3
...
```

**Problème** : Next-hop IP incorrect (`192.168.12.3` n'existe pas, devrait être `192.168.12.2`)

**Correction** :
```
R1(config)# no ip route 192.168.3.0 255.255.255.0 192.168.12.3
R1(config)# ip route 192.168.3.0 255.255.255.0 192.168.12.2
```

#### R2 : show ip route

```
R2# show ip route
...
S    192.168.3.0/24 is directly connected, GigabitEthernet0/0
...
```

**Problème** : Exit interface incorrecte (`G0/0` vers R1, devrait être next-hop IP `192.168.13.3`)

**Correction** :
```
R2(config)# no ip route 192.168.3.0 255.255.255.0 GigabitEthernet0/0
R2(config)# ip route 192.168.3.0 255.255.255.0 192.168.13.3
```

#### R3 : show ip interface brief

```
R3# show ip interface brief
Interface              IP-Address      Status                Protocol
GigabitEthernet0/0     192.168.13.2    up                    up
GigabitEthernet0/1     192.168.3.254   up                    up
```

**Problème** : IP G0/0 incorrecte (`192.168.13.2` = IP de R2, devrait être `192.168.13.3`)

**Correction** :
```
R3(config)# interface GigabitEthernet0/0
R3(config-if)# ip address 192.168.13.3 255.255.255.0
```

#### Validation

```
PC1> ping 192.168.3.1
```

**Résultat** : Success

---

## 💡 Notes

- **show ip route** : Commande essentielle diagnostic routing
- **Next-hop IP vs Exit interface** : Next-hop préféré (évite ambiguïté multi-access)
- **Erreurs courantes** : Typo IP next-hop, mauvaise interface, IP dupliquée

---

## 🏷️ Tags

`#CCNA` `#Routing` `#StaticRoutes` `#Cisco` `#IOS` `#PacketTracer` `#Troubleshooting` `#JeremyIT`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
