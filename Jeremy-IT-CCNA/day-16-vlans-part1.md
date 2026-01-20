# Day 16 - VLANs (Part 1)

**Difficulté** : Intermédiaire  
**Domaine** : VLANs, Switching, Subnetting  
**Date** : 19 janvier 2026  
**Source** : Jeremy's IT Lab - CCNA Course

---

## 📋 Consigne

1. Configurer l'adresse IP/masque de sous-réseau correct sur chaque PC.
   Définir l'adresse de passerelle comme la DERNIÈRE adresse utilisable du sous-réseau.

2. Effectuer trois connexions entre R1 et SW1.
   Configurer une interface sur R1 pour chaque VLAN.
   S'assurer que les adresses IP correspondent à l'adresse de passerelle configurée sur les PCs.

3. Configurer les interfaces de SW1 dans les VLANs appropriés.
   Ne pas oublier les interfaces qui se connectent à R1 !
   Nommer les VLANs (Engineering, HR, Sales)

4. Effectuer un ping entre les PCs pour vérifier la connectivité.
   Envoyer un ping de diffusion depuis un PC (ping vers l'adresse broadcast du sous-réseau),
   et observer quels périphériques reçoivent la diffusion (utiliser le 'Simulation Mode' de Packet Tracer)

---

## 🔧 Réalisation

### Plan d'adressage

**VLAN 10 - Engineering** :
- Network : `10.0.0.0/26`
- Mask : `255.255.255.192`
- PC1 : `10.0.0.1`
- PC2 : `10.0.0.2`
- Gateway : `10.0.0.62` (R1 G0/0)

**VLAN 20 - HR** :
- Network : `10.0.0.64/26`
- Mask : `255.255.255.192`
- PC3 : `10.0.0.65`
- PC4 : `10.0.0.66`
- Gateway : `10.0.0.126` (R1 G0/1)

**VLAN 30 - Sales** :
- Network : `10.0.0.128/26`
- Mask : `255.255.255.192`
- PC5 : `10.0.0.129`
- PC6 : `10.0.0.130`
- Gateway : `10.0.0.190` (R1 G0/2)

---

### Étape 1 : Configuration adresses IP PCs

**Configuration manuelle sur chaque PC** :
- Adresse IP, masque, gateway selon plan d'adressage
- Gateway = Dernière adresse utilisable (/26 = 62 hôtes utilisables)

---

### Étape 2 : Connexions physiques SW1 ↔ R1

**Câblage Copper Straight-Through** :
```
SW1 Gig0/1 ↔ R1 Gig0/0  (VLAN 10)
SW1 Gig1/1 ↔ R1 Gig0/1  (VLAN 20)
SW1 Gig2/1 ↔ R1 Gig0/2  (VLAN 30)
```

**Configuration interfaces R1** :
```cisco
R1(config)#int Gig0/0
R1(config-if)#ip address 10.0.0.62 255.255.255.192
R1(config-if)#no shut

R1(config-if)#int Gig0/1
R1(config-if)#ip address 10.0.0.126 255.255.255.192
R1(config-if)#no shut

R1(config-if)#int Gig0/2
R1(config-if)#ip address 10.0.0.190 255.255.255.192
R1(config-if)#no shut
```

**Explication** :
- `no shut` : Active interface (désactivée par défaut)
- Une interface physique R1 par VLAN (architecture séparée)

---

### Étape 3 : Configuration VLANs sur SW1

**Création VLANs** :
```cisco
SW1(config)#vlan 10
SW1(config-vlan)#name Engineering
SW1(config-vlan)#vlan 20
SW1(config-vlan)#name HR
SW1(config-vlan)#vlan 30
SW1(config-vlan)#name Sales
SW1(config-vlan)#exit
```

**Assignation ports access** :
```cisco
SW1(config)#int Fa3/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 10
SW1(config-if)#exit

SW1(config)#int Fa4/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 10

SW1(config)#int Fa5/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 20

SW1(config)#int Fa6/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 20

SW1(config)#int Fa7/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 30

SW1(config)#int Fa8/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 30
```

**Assignation ports vers routeur** :
```cisco
SW1(config)#int G0/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 10

SW1(config)#int G1/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 20

SW1(config)#int G2/1
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 30
```

**Explication** :
- `switchport mode access` : Port en mode access (un seul VLAN)
- Ports vers R1 également en mode access (un VLAN par interface)

**Vérification** :
```cisco
SW1(config)#do show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa9/1
10   Engineering                      active    Gig0/1, Fa3/1, Fa4/1
20   HR                               active    Gig1/1, Fa5/1, Fa6/1
30   Sales                            active    Gig2/1, Fa7/1, Fa8/1
```

---

### Étape 4 : Test connectivité et broadcast

**Test ping broadcast depuis PC1** :
```
C:\> ping 10.0.0.63
```

**Explication** : `10.0.0.63` = Adresse broadcast VLAN 10 (10.0.0.0/26)

**Observation Simulation Mode** :
- Paquets ARP envoyés **uniquement dans VLAN 10**
- PC1 et PC2 reçoivent broadcast
- PC3, PC4, PC5, PC6 (autres VLANs) ne reçoivent rien

**Vérification isolation VLANs** : Broadcasts confinés à leur VLAN ✅

---

## 🔑 Apprentissages clés

**Architecture multi-interface par VLAN** :
- Méthode basique : 1 interface physique R1 par VLAN
- Limitation : Scalabilité (nombre interfaces limité)
- Alternative : ROAS (Router on a Stick) - Day 17

**Broadcast confinement** :
- VLANs = Domaines de broadcast séparés
- Switch forward broadcast uniquement dans VLAN origine
- Sécurité + Performance (réduction trafic inutile)

**Modes switchport** :
- **Access** : Port connecté end-device (PC, serveur, imprimante)
- **Trunk** : Port inter-switch (plusieurs VLANs) - Day 17

**VLANs par défaut Cisco** :
- VLAN 1 : Default (tous ports par défaut)
- VLANs 1002-1005 : Token Ring, FDDI (technologies obsolètes, créés automatiquement)

---

## 🔗 Ressources

- [Cisco VLAN Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/16-12/configuration_guide/vlan/b_1612_vlan_9300_cg.html)
- [Jeremy's IT Lab - CCNA Day 16](https://www.youtube.com/watch?v=...)
