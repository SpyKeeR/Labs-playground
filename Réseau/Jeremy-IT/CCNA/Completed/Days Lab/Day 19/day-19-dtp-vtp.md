# Day 19 - DTP & VTP

**Difficulté** : Intermédiaire  
**Domaine** : VLAN Management, Trunk Negotiation  
**Date** : 1er février 2026  
**Source** : Jeremy's IT Lab - CCNA Course

---

## 📋 Consigne

Configuration d'un environnement multi-switch avec VTP (VLAN Trunking Protocol) et DTP (Dynamic Trunking Protocol).

1. Configurer les switchports reliant les switches en mode trunk.
   Désactiver DTP sur ces ports.
   Vérifier le mode administratif et opérationnel de chaque interface.

2. Configurer SW1 dans le domaine VTP "CCNA".
   Créer les VLANs 10, 20 et 30 sur SW1.
   Vérifier si SW2 et SW3 ont reçu les VLANs 10, 20 et 30.

3. Configurer SW2 en mode VTP transparent.
   Ajouter le VLAN 40 sur SW2.
   Vérifier si le VLAN 40 est ajouté à SW1/SW3.

4. Configurer SW3 en mode VTP client.
   Tenter de créer le VLAN 50 sur SW3.

5. Configurer tous les switchports connectés aux hôtes dans le bon VLAN.
   Les configurer manuellement en mode access.
   Vérifier si DTP est toujours activé sur ces ports.

---

## 📚 Rappels Théoriques

### VTP (VLAN Trunking Protocol)

**Modes VTP :**
- **Server** : Peut créer/modifier/supprimer VLANs, propage changements via trunks
- **Client** : Ne peut PAS créer/modifier VLANs, reçoit mises à jour VTP
- **Transparent** : Peut créer/modifier VLANs localement, transmet VTP messages mais ne synchronise pas

**Points clés :**
- Domaine VTP nécessaire pour synchronisation
- Seuls les VLANs créés en mode Server se propagent
- Mode Transparent : VLANs locaux uniquement, non propagés

### DTP (Dynamic Trunking Protocol)

**Modes DTP :**
- **Dynamic Auto** : Devient trunk si voisin Dynamic Desirable/Trunk
- **Dynamic Desirable** : Négocie activement trunk
- **Trunk** : Force mode trunk, négocie via DTP (sauf si nonegotiate)
- **Access** : Force mode access, DTP désactivé

**Désactivation DTP :**
- `switchport nonegotiate` : Désactive négociation DTP (recommandé pour sécurité)
- Ports access : DTP automatiquement off (`Trunking Negotiation: Off`)

---

## 🔧 Réalisation

### Étape 1 : Configuration Trunk + Désactivation DTP

**Sur TOUS les switches (SW1, SW2, SW3) :**

```cisco
SW1(config)#interface range GigabitEthernet0/1-2
SW1(config-if-range)#switchport mode trunk
SW1(config-if-range)#switchport nonegotiate
SW1(config-if-range)#end
```

**Répéter sur SW2 et SW3 :**
```cisco
SW2(config)#interface range GigabitEthernet0/1-2
SW2(config-if-range)#switchport mode trunk
SW2(config-if-range)#switchport nonegotiate
SW2(config-if-range)#end

SW3(config)#interface range GigabitEthernet0/1-2
SW3(config-if-range)#switchport mode trunk
SW3(config-if-range)#switchport nonegotiate
SW3(config-if-range)#end
```

**Vérification :**
```cisco
SW1#show interfaces switchport | begin Gig0/1

Name: Gig0/1
Switchport: Enabled
Administrative Mode: trunk
Operational Mode: trunk
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: dot1q
Negotiation of Trunking: Off

Name: Gig0/2
Switchport: Enabled
Administrative Mode: trunk
Operational Mode: trunk
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: dot1q
Negotiation of Trunking: Off
```

**Résultat :**
- ✅ Tous les liens inter-switch en mode trunk (Admin + Operational)
- ✅ Négociation DTP désactivée (`Negotiation of Trunking: Off`)

**Explication :**
- `switchport mode trunk` : Force le port en mode trunk permanent
- `switchport nonegotiate` : Désactive DTP (best practice sécurité)
- Sans `nonegotiate`, DTP resterait actif et enverrait des messages périodiques

---

### Étape 2 : Configuration VTP Server + Création VLANs

**Sur SW1 (VTP Server par défaut) :**

```cisco
SW1(config)#vtp domain CCNA
Changing VTP domain name from NULL to CCNA

SW1(config)#vlan 10
SW1(config-vlan)#exit
SW1(config)#vlan 20
SW1(config-vlan)#exit
SW1(config)#vlan 30
SW1(config-vlan)#exit
```

**Vérification sur SW2 et SW3 :**

```cisco
SW2#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/1, Fa0/2, Fa0/3, Fa0/4...
10   VLAN0010                         active    
20   VLAN0020                         active    
30   VLAN0030                         active    
1002 fddi-default                     active    
1003 token-ring-default               active    
```

```cisco
SW3#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/1, Fa0/2, Fa0/3, Fa0/4...
10   VLAN0010                         active    
20   VLAN0020                         active    
30   VLAN0030                         active    
```

**Résultat :**
- ✅ VLANs 10, 20, 30 créés sur SW1
- ✅ VLANs propagés automatiquement sur SW2 et SW3
- ✅ Synchronisation VTP fonctionnelle

**Explication :**
- `vtp domain CCNA` : Définit nom du domaine VTP (obligatoire pour sync)
- SW1 en mode Server par défaut : peut créer VLANs + propager
- SW2/SW3 en mode Server aussi par défaut : reçoivent mises à jour VTP

---

### Étape 3 : VTP Transparent Mode

**Sur SW2 :**

```cisco
SW2(config)#vtp mode transparent
Setting device to VTP TRANSPARENT mode

SW2(config)#vlan 40
SW2(config-vlan)#exit
```

**Vérification sur SW1 :**

```cisco
SW1#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/1, Fa0/2, Fa0/3
10   VLAN0010                         active    Fa0/1, Fa0/2
20   VLAN0020                         active    Fa0/3
30   VLAN0030                         active    
```
**➡️ VLAN 40 ABSENT**

**Vérification sur SW3 :**

```cisco
SW3#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    
10   VLAN0010                         active    Fa0/1
20   VLAN0020                         active    Fa0/4
30   VLAN0030                         active    Fa0/2, Fa0/3
```
**➡️ VLAN 40 ABSENT**

**Résultat :**
- ✅ VLAN 40 créé sur SW2 UNIQUEMENT
- ✅ VLAN 40 NON propagé sur SW1 et SW3
- ✅ SW2 transmet messages VTP mais ne synchronise pas

**Explication :**
- Mode Transparent : VLAN database locale indépendante
- SW2 transmet les VTP advertisements mais n'applique pas les changements
- VLANs créés en mode Transparent restent locaux

---

### Étape 4 : VTP Client Mode

**Sur SW3 :**

```cisco
SW3(config)#vtp mode client
Setting device to VTP CLIENT mode

SW3(config)#vlan 50
VTP VLAN configuration not allowed when device is in CLIENT mode.
```

**Résultat :**
- ❌ Impossible de créer VLAN 50 sur SW3
- ✅ Message d'erreur explicite : mode CLIENT interdit création VLANs

**Explication :**
- Mode Client : VLAN database en lecture seule
- Reçoit mises à jour VTP mais ne peut pas créer/modifier/supprimer VLANs
- Utilisé pour switches simples qui ne doivent pas modifier la config VLAN

---

### Étape 5 : Configuration Ports Access + Vérification DTP

**Sur SW1 :**

```cisco
SW1(config)#interface range FastEthernet0/1-2
SW1(config-if-range)#switchport mode access
SW1(config-if-range)#switchport access vlan 10
SW1(config-if-range)#exit

SW1(config)#interface FastEthernet0/3
SW1(config-if)#switchport mode access
SW1(config-if)#switchport access vlan 20
SW1(config-if)#exit
```

**Sur SW2 :**

```cisco
SW2(config)#interface range FastEthernet0/1-2
SW2(config-if-range)#switchport mode access
SW2(config-if-range)#switchport access vlan 40
SW2(config-if-range)#exit
```

**Sur SW3 :**

```cisco
SW3(config)#interface range FastEthernet0/2-3
SW3(config-if-range)#switchport mode access
SW3(config-if-range)#switchport access vlan 30
SW3(config-if-range)#exit

SW3(config)#interface FastEthernet0/1
SW3(config-if)#switchport mode access
SW3(config-if)#switchport access vlan 10
SW3(config-if)#exit

SW3(config)#interface FastEthernet0/4
SW3(config-if)#switchport mode access
SW3(config-if)#switchport access vlan 20
SW3(config-if)#exit
```

**Vérification DTP sur ports access (tous les switches) :**

```cisco
SW1#show interfaces switchport | begin Fa0/1

Name: Fa0/1
Switchport: Enabled
Administrative Mode: static access
Operational Mode: static access
Trunking Negotiation: Off

Name: Fa0/2
Switchport: Enabled
Administrative Mode: static access
Operational Mode: static access
Trunking Negotiation: Off

Name: Fa0/3
Switchport: Enabled
Administrative Mode: static access
Operational Mode: static access
Trunking Negotiation: Off
```

**Résultat :**
- ✅ Tous les ports access configurés dans les bons VLANs
- ✅ DTP automatiquement désactivé sur ports access (`Trunking Negotiation: Off`)
- ✅ Pas besoin de `switchport nonegotiate` sur ports access

**Explication :**
- `switchport mode access` désactive DTP automatiquement
- Port access = 1 seul VLAN, pas de négociation trunk nécessaire
- Best practice : toujours forcer mode (access ou trunk), jamais laisser dynamic

---

## 📊 Schéma Final

```
         [SW1 - VTP Server]
         VLANs: 10, 20, 30
              /         \
        Trunk (noneg)  Trunk (noneg)
            /               \
   [SW2 - Transparent]    [SW3 - Client]
   VLANs: 10,20,30,40     VLANs: 10,20,30
   (40 local uniquement)  (lecture seule)
   
   Fa0/1-2: VLAN 40       Fa0/1: VLAN 10
                          Fa0/2-3: VLAN 30
SW1:                      Fa0/4: VLAN 20
  Fa0/1-2: VLAN 10
  Fa0/3: VLAN 20
```

---

## 💡 Apprentissages Clés

### VTP Best Practices

1. **Utiliser mode Transparent pour la plupart des switches**
   - Évite synchronisations accidentelles
   - Maintien control local de la VLAN database

2. **Mode Client : uniquement pour switches très simples**
   - Pas de création VLAN locale
   - Dépend entièrement du Server VTP

3. **Attention au VTP Version Number**
   - Switch avec revision number plus élevée écrase les autres
   - Risque : brancher ancien switch peut supprimer tous les VLANs !

### DTP Best Practices

1. **Toujours désactiver DTP sur ports trunk** (`switchport nonegotiate`)
   - Réduit trafic réseau inutile
   - Améliore sécurité (empêche VLAN hopping attacks)

2. **Forcer mode access/trunk explicitement**
   - Jamais laisser en Dynamic Auto/Desirable
   - Configuration claire et prévisible

3. **DTP désactivé automatiquement sur ports access**
   - `Trunking Negotiation: Off` automatique avec `switchport mode access`
   - Pas besoin de `nonegotiate` supplémentaire

### Vérifications Importantes

**Commandes de diagnostic :**
- `show vtp status` : Mode VTP, domain, revision number
- `show interfaces switchport` : Mode admin/operational, DTP status
- `show vlan` : Liste VLANs + ports assignés
- `show interfaces trunk` : Trunks actifs + VLANs allowed

**Points de vigilance :**
- VTP domain DOIT correspondre pour synchronisation
- Mode Transparent : VLANs créés localement ne se propagent PAS
- Mode Client : VLAN database read-only

---

## ⚠️ Pièges & Erreurs Courantes

1. **Oublier `switchport nonegotiate` sur trunks**
   - DTP reste actif (messages périodiques)
   - Risque sécurité VLAN hopping

2. **Créer VLAN sur switch Transparent et s'attendre à propagation**
   - Mode Transparent = VLAN database locale uniquement

3. **Tenter créer VLAN sur switch Client**
   - Erreur `VTP VLAN configuration not allowed when device is in CLIENT mode`

4. **Brancher switch avec revision number élevée**
   - Peut effacer toute la VLAN database du réseau !
   - Solution : reset revision number avant connexion

---

## 🎯 Commandes Résumé

```cisco
# Configuration Trunk + DTP Off
interface range GigabitEthernet0/1-2
switchport mode trunk
switchport nonegotiate

# VTP Configuration
vtp domain CCNA              # Définir domaine
vtp mode {server|client|transparent}

# Création VLANs
vlan 10
vlan 20

# Configuration Ports Access
interface FastEthernet0/1
switchport mode access
switchport access vlan 10

# Vérifications
show vtp status
show interfaces switchport
show vlan
show interfaces trunk
```

---

## ⏱️ Temps de Réalisation

- **Lecture cours** : 35 min
- **Lab configuration** : 10 min
- **Write-up** : 15 min
- **Total** : ~60 min

---

## 🔗 Ressources

- [Jeremy's IT Lab - Day 19 Lecture (35:40)](https://www.udemy.com/course/complete-networking-fundamentals-course-ccna-start/)
- [Cisco VTP Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/16-12/configuration_guide/vlan/b_1612_vlan_9300_cg/configuring_vtp.html)
- [DTP Security Best Practices](https://www.cisco.com/c/en/us/support/docs/lan-switching/8021q/17056-741-4.html)

---

**Tags :** `#CCNA` `#VTP` `#DTP` `#VLANs` `#Trunking` `#Switching` `#Lab`
