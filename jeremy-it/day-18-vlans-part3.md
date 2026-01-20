# Day 18 - VLANs (Part 3)

**Difficulté** : Avancé  
**Domaine** : Switch Layer 3, SVIs, Inter-VLAN Routing  
**Date** : 19 janvier 2026  
**Source** : Jeremy's IT Lab - CCNA Course

---

## 📋 Consigne

Tous les périphériques sont préconfigurés depuis la fin du lab Day 17 (SW2 a été remplacé par un switch multicouche) :
- Les hôtes sont dans les VLANs corrects
- SW1-SW2 sont connectés via trunk
- R1-SW2 sont connectés via ROAS

1. Remplacer la configuration ROAS sur R1-SW2 par une connexion Layer 3 point-à-point.
   Utiliser les adresses IP données dans le diagramme réseau.
   Configurer une route par défaut sur SW2, avec l'interface G0/0 de R1 comme next hop.

2. Configurer des SVIs sur SW2, un pour chaque VLAN.
   Assigner la dernière adresse IP utilisable de chaque sous-réseau au SVI approprié.

3. Tester la connectivité inter-VLAN en effectuant des pings entre VLANs.

4. Tester la connectivité Internet en effectuant un ping vers 1.1.1.1
   (Les routes ont déjà été configurées sur R1 et le routeur Internet)

---

## 🔧 Réalisation

### Étape 1 : Suppression configuration ROAS sur R1

```cisco
R1(config)#no int G0/0.10
R1(config)#no int G0/0.20
R1(config)#no int G0/0.30

R1(config)#default int G0/0
Building configuration...
Interface GigabitEthernet0/0 set to default configuration

R1(config)#int G0/0
R1(config-if)#ip address 10.0.0.194 255.255.255.252
R1(config-if)#no shut
```

**Explication** :
- `no int G0/0.X` : Supprime sous-interfaces ROAS
- `default int G0/0` : Réinitialise interface (efface toute config)
- Adresse IP `/30` (point-to-point, 2 hôtes utilisables)

---

### Étape 2 : Configuration Layer 3 sur SW2

**Suppression config trunk + Activation routing** :
```cisco
SW2(config)#default int G1/0/2
Building configuration...
Interface GigabitEthernet1/0/2 set to default configuration

SW2(config)#ip routing
```

**Explication** :
- `default int` : Réinitialise interface (mode switchport par défaut)
- `ip routing` : **Active fonction routage** sur switch L3 (clé!)

**Configuration interface routed** :
```cisco
SW2(config)#int G1/0/2
SW2(config-if)#no switchport
SW2(config-if)#ip address 10.0.0.193 255.255.255.252
```

**Explication** :
- `no switchport` : **Transforme port L2 en port L3** (interface routed)
- Permet assignation IP directement (comme routeur)

---

### Étape 3 : Configuration route par défaut SW2

```cisco
SW2(config)#ip route 0.0.0.0 0.0.0.0 10.0.0.194
```

**Explication** : Route par défaut vers R1 (passerelle Internet)

---

### Étape 4 : Configuration SVIs (Switch Virtual Interfaces)

```cisco
SW2(config)#int vlan 10
%LINK-5-CHANGED: Interface Vlan10, changed state to up
SW2(config-if)#ip address 10.0.0.62 255.255.255.192
SW2(config-if)#no shut
SW2(config-if)#exit

SW2(config)#int vlan 20
%LINK-5-CHANGED: Interface Vlan20, changed state to up
SW2(config-if)#ip address 10.0.0.126 255.255.255.192
SW2(config-if)#no shut
SW2(config-if)#exit

SW2(config)#int vlan 30
%LINK-5-CHANGED: Interface Vlan30, changed state to up
SW2(config-if)#ip address 10.0.0.190 255.255.255.192
SW2(config-if)#no shut
```

**Explication SVIs** :
- **Interface virtuelle** : Pas physique, représente VLAN Layer 3
- Permet switch L3 de router entre VLANs **en interne** (pas besoin routeur externe)
- `no shut` : Active SVI (down par défaut)
- SVI UP si : VLAN existe + au moins 1 port actif dans VLAN

---

### Étape 5 : Test connectivité

**Depuis PC1 (VLAN 10)** :
```
C:\> ping 10.0.0.62   (Gateway VLAN 10 - SVI)
C:\> ping 10.0.0.65   (PC3 VLAN 20)
C:\> ping 1.1.1.1     (Internet via R1)
```

**Résultat** : Tous les pings réussissent ✅

---

## 🔑 Apprentissages clés

**Switch Layer 3 vs Layer 2** :
- **L2** : Switching uniquement (forward based on MAC)
- **L3** : Switching + Routing (forward based on MAC + IP)
- Catalyst 3560, 3750, 9300 = L3 capable

**Inter-VLAN routing évolution** :
1. **Routeur externe multi-interface** (Day 16) : Câble par VLAN, pas scalable
2. **ROAS** (Day 17) : Un câble trunk, routage externe, latence
3. **Switch L3 + SVIs** (Day 18) : Routage interne, performances optimales

**SVI (Switch Virtual Interface)** :
- Interface logique représentant VLAN en Layer 3
- Agit comme **gateway par défaut** pour hosts du VLAN
- Requiert VLAN existant + port actif pour être UP

**Commande `ip routing`** :
- **Absente** : Switch L3 = Switch L2 (routing désactivé)
- **Présente** : Switch peut router paquets entre VLANs/réseaux
- Essentielle pour SVIs fonctionnels

**Interface routed vs switchport** :
- **Switchport** (défaut) : Port L2, mode access/trunk
- **Routed** (`no switchport`) : Port L3, adresse IP directe
- Utilisé pour connexion point-to-point L3 (switch-routeur, switch-switch)

**Wireshark - Trame 802.1Q** :
- **Trame non-taguée** : Ethernet Type directement après MAC dest/source
- **Trame taguée** : 4 octets tag 802.1Q inséré (TPID 0x8100 + TCI)
- Tag ajouté par switch sortie trunk, retiré entrée trunk

---

## 📊 Comparaison architectures Inter-VLAN

| Architecture | Câbles | Latence | Scalabilité | Complexité |
|--------------|--------|---------|-------------|------------|
| **Multi-interface** | N câbles (N=VLANs) | Basse | Faible (limite ports) | Faible |
| **ROAS** | 1 trunk | Moyenne (aller-retour) | Moyenne | Moyenne |
| **Switch L3 + SVI** | 1 L3 link | Très basse (interne) | Haute | Haute |

---

## 🔗 Ressources

- [Cisco Switch Virtual Interface](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/16-12/configuration_guide/int_hw/b_1612_int_hw_9300_cg/configuring_switch_virtual_interfaces.html)
- [Layer 3 Switch Configuration](https://www.cisco.com/c/en/us/support/docs/smb/switches/cisco-350-series-managed-switches/smb5760-configure-layer-3-switching-on-a-switch-through-the-command-i.html)
- [Jeremy's IT Lab - CCNA Day 18](https://www.youtube.com/watch?v=...)
