# Day 17 - VLANs (Part 2)

**Difficulté** : Intermédiaire  
**Domaine** : VLANs, Trunk, ROAS (Router on a Stick), 802.1Q  
**Date** : 19 janvier 2026  
**Source** : Jeremy's IT Lab - CCNA Course

---

## 📋 Consigne

1. Configurer les interfaces du switch connectées aux PCs comme ports access dans le VLAN correct.

2. Configurer la connexion entre SW1 et SW2 comme trunk, autorisant uniquement les VLANs nécessaires.
   Configurer un VLAN inutilisé comme native VLAN.
   **S'assurer que tous les VLANs nécessaires existent sur chaque switch**

3. Configurer la connexion entre SW2 et R1 en utilisant 'router on a stick'.
   Assigner la dernière adresse utilisable de chaque sous-réseau aux sous-interfaces de R1.

4. Tester la connectivité en effectuant des pings entre les PCs. Tous les PCs doivent pouvoir se joindre.

---

## 🔧 Réalisation

### Étape 1 : Configuration ports access SW1

```cisco
SW1(config)#int range Fa0/1,Fa0/2
SW1(config-if-range)#switchport mode access
SW1(config-if-range)#switchport access vlan 10
% Access VLAN does not exist. Creating vlan 10
SW1(config-if-range)#exit

SW1(config)#int range Fa0/3,Fa0/4
SW1(config-if-range)#switchport mode access
SW1(config-if-range)#switchport access vlan 30
% Access VLAN does not exist. Creating vlan 30
```

**Explication** :
- `int range` : Configure plusieurs interfaces simultanément
- VLAN créé automatiquement si inexistant

---

### Étape 2 : Configuration trunk SW1 ↔ SW2

**SW1** :
```cisco
SW1(config)#int G0/1
SW1(config-if)#switchport mode trunk
SW1(config-if)#switchport trunk allowed vlan 10,30
SW1(config-if)#switchport trunk native vlan 99
```

**SW2** :
```cisco
SW2(config)#int Fa0/1
SW2(config-if)#switchport mode access
SW2(config-if)#switchport access vlan 20
% Access VLAN does not exist. Creating vlan 20
SW2(config-if)#exit

SW2(config)#int range Fa0/2,Fa0/3
SW2(config-if-range)#switchport mode access
SW2(config-if-range)#switchport access vlan 10
% Access VLAN does not exist. Creating vlan 10

SW2(config)#int G0/1
SW2(config-if)#switchport mode trunk
SW2(config-if)#switchport trunk allowed vlan 10,30
SW2(config-if)#switchport trunk native vlan 99
```

**Explication trunk** :
- `switchport mode trunk` : Active mode trunk (plusieurs VLANs)
- `allowed vlan 10,30` : Autorise uniquement VLANs nécessaires (sécurité)
- `native vlan 99` : Trafic non-tagué sur VLAN 99 (bonne pratique : VLAN inutilisé)

---

### Étape 3 : Configuration trunk SW2 ↔ R1 + ROAS

**SW2 vers R1** :
```cisco
SW2(config)#int G0/2
SW2(config-if)#switchport mode trunk
SW2(config-if)#switchport trunk allowed vlan 10,20,30
SW2(config-if)#switchport trunk native vlan 99
SW2(config-if)#exit

SW2(config)#vlan 30
```

**Explication** : Création manuelle VLAN 30 (pas créé automatiquement car aucun port access)

**R1 - Router on a Stick** :
```cisco
R1(config)#int G0/0
R1(config-if)#no shut

R1(config-if)#int G0/0.10
R1(config-subif)#encapsulation dot1q 10
R1(config-subif)#ip address 10.0.0.62 255.255.255.192

R1(config)#int G0/0.20
R1(config-subif)#encapsulation dot1q 20
R1(config-subif)#ip address 10.0.0.126 255.255.255.192

R1(config)#int G0/0.30
R1(config-subif)#encapsulation dot1q 30
R1(config-subif)#ip address 10.0.0.190 255.255.255.192

R1(config)#int G0/0.99
R1(config-subif)#encapsulation dot1q 99 native
```

**Explication ROAS** :
- **Sous-interfaces** : `G0/0.10`, `G0/0.20`, etc. (logiques, pas physiques)
- `encapsulation dot1q 10` : Tag 802.1Q avec VLAN ID 10
- `no shut` sur interface physique `G0/0` active toutes sous-interfaces
- `native` : Trafic non-tagué associé au native VLAN

**Avantage** : Une seule interface physique pour tous les VLANs (scalabilité)

---

### Étape 4 : Test connectivité inter-VLAN

**Depuis n'importe quel PC** :
```
C:\> ping 10.0.0.1   (VLAN 10)
C:\> ping 10.0.0.65  (VLAN 20)
C:\> ping 10.0.0.129 (VLAN 30)
```

**Résultat** : Tous les PCs peuvent communiquer ✅

---

## 🔑 Apprentissages clés

**802.1Q Tagging** :
- **TPID** (Tag Protocol Identifier) : 0x8100 (identifie trame 802.1Q)
- **TCI** (Tag Control Information) :
  * **PCP** (Priority Code Point) : 3 bits (QoS priorité)
  * **DEI** (Drop Eligible Indicator) : 1 bit (éligibilité drop en congestion)
  * **VID** (VLAN Identifier) : 12 bits (4096 VLANs possibles)

**Native VLAN** :
- Trafic **non-tagué** sur trunk
- Par défaut VLAN 1 (bonne pratique : changer pour VLAN inutilisé)
- **Mismatch native VLAN** = problème connectivité inter-switch

**ROAS vs Multi-interface** :
- **Multi-interface** (Day 16) : 1 cable par VLAN, limite scalabilité
- **ROAS** : 1 cable trunk pour tous VLANs, économie ports

**Trunk allowed VLANs** :
- Par défaut : `all` (tous VLANs autorisés)
- Best practice : Limiter aux VLANs utilisés (sécurité + performance)

**Commandes switchport** :
- `switchport mode access` : Mode access (1 VLAN)
- `switchport mode trunk` : Mode trunk (plusieurs VLANs)
- `switchport trunk encapsulation dot1q` : Encapsulation 802.1Q (parfois requis)

---

## 🔗 Ressources

- [Cisco 802.1Q Trunking](https://www.cisco.com/c/en/us/support/docs/lan-switching/8021q/17056-741-4.html)
- [Jeremy's IT Lab - CCNA Day 17](https://www.youtube.com/watch?v=...)
