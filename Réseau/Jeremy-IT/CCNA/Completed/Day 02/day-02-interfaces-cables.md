# Jeremy IT CCNA - Day 02 : Interfaces and Cables

**Date :** 6 janvier 2026  
**Durée :** ~30 minutes  
**Série :** Jeremy IT CCNA (Day 02/53)  
**Ressources :** [Jeremy's IT Lab - Free CCNA Course](https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ)

---

## 🎯 Objectif

Comprendre les standards IEEE 802.3 pour Ethernet, les types de câbles réseau (copper vs fiber), la nomenclature des connexions (BASE-T, LX, SX), et apprendre à sélectionner le câble approprié selon les critères distance/débit/environnement.

---

## 📋 Cours : Interfaces and Cables

### Standards IEEE 802.3 (Ethernet)

**IEEE** = Institute of Electrical and Electronics Engineers  
**802.3** = Famille standards Ethernet (câbles, connecteurs, vitesses)

#### Nomenclature standards

**Format :** `<VITESSE>BASE-<TYPE>`

- **VITESSE** : 10, 100, 1000 (Mbps) ou 10G, 40G, 100G (Gbps)
- **BASE** : Baseband (signal unique, vs Broadband multi-signaux)
- **TYPE** : T (Twisted Pair copper), LX/SX (fiber optic)

**Exemples :**

| Standard | Vitesse | Type câble | Distance max | Connecteur |
|----------|---------|------------|--------------|------------|
| **10BASE-T** | 10 Mbps | UTP Cat3 | 100m | RJ45 |
| **100BASE-TX** | 100 Mbps | UTP Cat5 | 100m | RJ45 |
| **1000BASE-T** | 1 Gbps | UTP Cat5e/6 | 100m | RJ45 |
| **10GBASE-T** | 10 Gbps | UTP Cat6a/7 | 100m | RJ45 |
| **1000BASE-LX** | 1 Gbps | Fiber monomode | 5 km | LC/SC |
| **1000BASE-SX** | 1 Gbps | Fiber multimode | 550m | LC/SC |
| **10GBASE-SR** | 10 Gbps | Fiber multimode | 400m | LC |
| **10GBASE-LR** | 10 Gbps | Fiber monomode | 10 km | LC |

---

### Câbles cuivre (Copper) - Twisted Pair

#### Catégories UTP/STP

**UTP** = Unshielded Twisted Pair (non blindé)  
**STP** = Shielded Twisted Pair (blindé, résistant interférences EMI)

| Catégorie | Bande passante | Vitesse max | Usage typique |
|-----------|----------------|-------------|---------------|
| **Cat 3** | 16 MHz | 10 Mbps | 10BASE-T (obsolète) |
| **Cat 5** | 100 MHz | 100 Mbps | 100BASE-TX |
| **Cat 5e** | 100 MHz | 1 Gbps | 1000BASE-T (standard actuel) |
| **Cat 6** | 250 MHz | 10 Gbps (55m) | 1G/10GBASE-T |
| **Cat 6a** | 500 MHz | 10 Gbps (100m) | 10GBASE-T |
| **Cat 7** | 600 MHz | 10 Gbps (100m) | Datacenters |

**Note :** La **bande passante** (MHz) détermine la vitesse maximale supportée.

---

#### Types câbles cuivre

**1. Straight-Through (Droit)**

- **Usage** : Connecter équipements **différents** types
- **Pinout** : 1→1, 2→2, ..., 8→8 (identique chaque extrémité)
- **Exemples** :
  * PC → Switch
  * Router → Switch
  * Switch → Firewall

**2. Crossover (Croisé)**

- **Usage** : Connecter équipements **même** type
- **Pinout** : Permutation paires Tx/Rx (1-2 ↔ 3-6)
- **Exemples** :
  * PC → PC (direct)
  * Switch → Switch (sans uplink)
  * Router → Router

**Note moderne :** Auto-MDI/MDIX détecte automatiquement → câble droit suffit presque toujours.

**3. Rollover (Console)**

- **Usage** : Connexion console (configuration CLI)
- **Pinout étoile** : 1→8, 2→7, 3→6, 4→5 (inversion complète)
- **Exemple** : Laptop (port série/USB) → Switch/Router (port console RJ45)

---

### Câbles fibre optique (Fiber Optic)

#### Principe

- Transmission par **lumière** (LED ou laser) dans fibre verre/plastique
- **Avantages** : Immunité EMI, longues distances, hauts débits
- **Inconvénients** : Coût élevé, fragilité mécanique, expertise installation

---

#### Types fibre

**1. Multimode (MMF)**

- **Diamètre cœur** : 50-62.5 µm (large)
- **Source lumière** : LED (infrarouge)
- **Distance** : 550m max (dispersion modale)
- **Coût** : Faible (LED bon marché)
- **Standards** : 1000BASE-SX, 10GBASE-SR
- **Couleur gaine** : Orange (OM1/OM2) ou Aqua (OM3/OM4)

**2. Monomode (SMF - Single Mode Fiber)**

- **Diamètre cœur** : 8-10 µm (très fin)
- **Source lumière** : Laser (cohérent)
- **Distance** : 5-40 km (pas dispersion)
- **Coût** : Élevé (laser précis)
- **Standards** : 1000BASE-LX, 10GBASE-LR/ER
- **Couleur gaine** : Jaune

---

#### Connecteurs fibre

| Connecteur | Type | Usage |
|------------|------|-------|
| **LC** | Petit (1.25mm) | Standard moderne (SFP, SFP+) |
| **SC** | Moyen (2.5mm) | Legacy, patch panels |
| **ST** | Bayonet | Ancien (obsolète) |
| **MPO/MTP** | Multi-fibres | 40G/100G QSFP |

**Duplex** : 2 fibres (Tx + Rx) dans 1 connecteur.

---

### SFP/SFP+ Transceivers

**SFP** = Small Form-factor Pluggable (module amovible)

- **Avantage** : Port switch universel (changer transceiver selon besoin)
- **Types** :
  * SFP : 1 Gbps (1000BASE-T, LX, SX)
  * SFP+ : 10 Gbps (10GBASE-SR, LR)
  * QSFP+ : 40 Gbps
  * QSFP28 : 100 Gbps

**Exemples modules :**
- **1000BASE-T SFP** : RJ45 copper (100m)
- **1000BASE-SX SFP** : Fiber multimode LC (550m)
- **10GBASE-LR SFP+** : Fiber monomode LC (10km)

---

## 🧪 Lab : Cable Type Selection

### Énoncé

Connecter différents équipements en sélectionnant le câble approprié selon :
1. Type équipements (même/différent)
2. Distance
3. Vitesse requise

**Topologie :**
- PC1 ↔ Switch1
- Switch1 ↔ Router1
- Router1 ↔ Router2 (WAN 10km)
- PC2 ↔ PC3 (direct)

---

### Résolution

**1. PC1 → Switch1**

- **Types équipements** : Différents (endpoint → switch)
- **Distance** : 5m (local)
- **Câble** : **Straight-Through UTP Cat5e** (RJ45)
- **Standard** : 1000BASE-T (1 Gbps, 100m max OK)

---

**2. Switch1 → Router1**

- **Types équipements** : Différents (switch → router)
- **Distance** : 10m
- **Câble** : **Straight-Through UTP Cat5e**
- **Standard** : 1000BASE-T

---

**3. Router1 → Router2 (WAN)**

- **Types équipements** : Identiques (router → router)
- **Distance** : **10 km** (longue distance)
- **Problème** : UTP limité 100m, crossover impossible
- **Solution** : **Fiber monomode (SMF)** avec transceivers SFP+
- **Câble** : **10GBASE-LR** (laser, LC connector)
  * Vitesse : 10 Gbps
  * Distance : 10 km max
  * Connecteurs : LC duplex

**Installation :**
```
Router1 : Installer SFP+ 10GBASE-LR dans port GigabitEthernet
Router2 : Installer SFP+ 10GBASE-LR dans port GigabitEthernet
Câble : Fiber monomode LC-LC (jaune)
```

---

**4. PC2 → PC3 (direct)**

- **Types équipements** : Identiques (PC → PC)
- **Distance** : 2m
- **Câble classique** : Crossover UTP Cat5e (permutation Tx/Rx)
- **Alternative moderne** : Straight-Through (si cartes réseau Auto-MDIX)

**Note :** Packet Tracer peut imposer crossover (simulation anciens équipements).

---

### Vérification

**1. Vérifier status interfaces**

Dans Packet Tracer :
- Cliquer équipement → Physical
- Observer LED ports : **Vert** = UP, **Rouge** = DOWN, **Éteint** = disconnected

**2. Tester connectivité**

```bash
# Depuis PC1
ping <IP_Router1>

# Depuis Router1
ping <IP_Router2>
```

Si timeout → vérifier :
- Type câble (straight vs crossover vs fiber)
- Transceivers installés (fiber)
- Interfaces activées (`no shutdown`)

---

## 💡 Apprentissages clés

### Standards IEEE 802.3

**Mnémonique nomenclature :**
- **BASE-T** = **T**wisted pair (cuivre RJ45)
- **BASE-LX** = **L**ong wavelength (laser monomode, longue distance)
- **BASE-SX** = **S**hort wavelength (LED multimode, courte distance)

**Règle distance copper :** 100m max (tous standards UTP).

---

### Sélection câble (décision tree)

```
Distance > 100m ?
├─ OUI → Fiber optic
│   └─ Distance > 550m ?
│       ├─ OUI → Monomode (LX/LR)
│       └─ NON → Multimode (SX/SR)
│
└─ NON → Copper UTP
    └─ Types équipements identiques ?
        ├─ OUI → Crossover (ou Auto-MDIX)
        └─ NON → Straight-Through
```

---

### Bande passante vs vitesse

**Erreur fréquente :** Confondre bande passante (MHz) et débit (Mbps/Gbps).

- **Bande passante** : Fréquences supportées (qualité câble)
- **Vitesse** : Débit données (dépend bande passante + encodage)

**Exemple :**
- Cat5e : 100 MHz → supporte 1 Gbps (encodage 4 paires)
- Cat6a : 500 MHz → supporte 10 Gbps (meilleur SNR)

---

### Fiber : Multimode vs Monomode

**Quand choisir multimode :**
- Distance < 550m (datacenter, campus)
- Budget limité (LED bon marché)
- Débit 1G/10G suffisant

**Quand choisir monomode :**
- Distance > 550m (MAN, WAN, buildings distants)
- Besoin 10G+ sur longues distances
- Infrastructure critique (pas dispersion modale)

---

### Auto-MDI/MDIX (Modern Ethernet)

**Fonctionnement :** Cartes réseau détectent automatiquement pinout et inversent Tx/Rx si besoin.

**Impact :** Crossover cables **obsolètes** dans réseaux modernes (gigabit+).

**Exception :** Packet Tracer simule anciens équipements → peut exiger crossover.

---

### Transceivers SFP modulaires

**Avantages :**
- **Flexibilité** : 1 port switch → multiple usages (copper/fiber/distance)
- **Hot-swappable** : Changement sans éteindre switch
- **Scalabilité** : Migration 1G → 10G sans changer switch

**Exemple évolution datacenter :**
1. Déploiement initial : SFP 1000BASE-T (copper)
2. Migration fiber : Remplacer par SFP 1000BASE-SX
3. Upgrade 10G : Remplacer par SFP+ 10GBASE-SR (même port)

---

## 🏢 Application professionnelle

### Datacenter (rows servers)

**Scénario :** Connecter 200 serveurs dans 10 racks.

**Câblage :**
- **TOR switches** (Top of Rack) : 1 par rack
- **Serveurs → TOR** : Straight-Through Cat6a (10GBASE-T, 5m)
- **TOR → Core switches** : Fiber multimode 10GBASE-SR (OM3, 100m)
- **Core switches clustering** : Fiber monomode 40GBASE-LR4 (QSFP+, 2km inter-datacenter)

**Justification distances :**
- Intra-rack : < 10m → copper économique
- Rack-to-Core : < 300m → multimode (coût modéré)
- Inter-datacenter : > 2km → monomode (seule option)

---

### Campus universitaire (3 bâtiments)

**Topologie :**
- Building A (Admin) ↔ Building B (Sciences) : 500m
- Building B ↔ Building C (Sports) : 1.2 km

**Câblage :**
- **A ↔ B** : Fiber multimode 1000BASE-SX (OM2, 550m max OK)
- **B ↔ C** : Fiber monomode 1000BASE-LX (SMF, 5km max OK)
- **Distribution interne** : UTP Cat6 (100m bureaux → switch étage)

**Budget :**
- Multimode A-B : 2€/m → 1000€
- Monomode B-C : 5€/m → 6000€
- UTP interne : 0.50€/m → 500€

---

### Industrial site (usine)

**Contraintes :**
- Interférences EMI (moteurs 380V, variateurs fréquence)
- Humidité, poussières
- Températures -10°C/+50°C

**Solutions câblage :**
- **STP Cat6a** (Shielded) : Résistance EMI (paires blindées individuellement + tresse globale)
- **Fiber multimode** : Immunité totale EMI (zones critiques autour machines)
- **IP67 connectors** : Étanchéité poussière/eau

**Exemple :**
```
Automate Siemens → Switch industriel : STP Cat6a (10m, blindage 360°)
Switch zone production → Salle serveurs : Fiber OM3 (200m, immunité EMI)
```

---

### Home office (télétravail)

**Besoin :** Connexion stable PC → Box Internet.

**Distance typique :** 20m (bureau étage, box RDC).

**Options :**
1. **WiFi** : Simple mais latence variable (visio, gaming problématique)
2. **Powerline (CPL)** : Utilise réseau électrique (débit erratique)
3. **UTP Cat5e** : Câblage mural propre (**recommandé**)

**Installation Cat5e :**
- Passage gaine technique ou plinthes
- Connecteurs RJ45 sertis (outil nécessaire)
- Test continuité (cable tester)

**Gain :** Latency 1ms (vs 20-50ms WiFi), débit stable 1 Gbps.

---

## ❌ Difficultés rencontrées

### Compréhension initiale

**Problème :** Nomenclature BASE-T/LX/SX abstraite sans contexte.

**Solution :** Cours Jeremy détaille historique + cas usage → mémorisation facilitée.

**Exemple mnémonique :**
- **T** = Twisted (torsadé) → visualiser paires cuivre entrelacées
- **LX** = Long (laser traverse 10km) → faisceau laser focalisé
- **SX** = Short (LED diffuse rapidement) → lumière dispersion modale

---

### Différenciation multimode/monomode

**Confusion initiale :** Pourquoi 2 types fibre ?

**Clarification :**
- **Multimode** : Diamètre large → rayons lumineux multiples angles (**dispersion modale** limite distance)
- **Monomode** : Diamètre très fin → 1 seul rayon (chemin unique, pas dispersion → longues distances)

**Analogie :** Multimode = autoroute 6 voies (voitures vitesses différentes arrivent décalées), Monomode = rail unique TGV (train arrive précisément).

---

### Lab : Oubli no shutdown

**Erreur :** Connexion fiber Router1-Router2 DOWN malgré câble/transceivers corrects.

**Cause :** Interfaces fiber désactivées par défaut (économie énergie).

**Fix :**
```cisco
Router1(config)# interface GigabitEthernet0/0/0
Router1(config-if)# no shutdown
```

**Vérification :**
```cisco
Router1# show ip interface brief
GigabitEthernet0/0/0   10.1.1.1   YES manual up   up
```

Status `up/up` = Layer 1 (physical) + Layer 2 (data link) opérationnels.

---

## 🔗 Ressources

- **Jeremy's IT Lab Day 02** : [Interfaces and Cables](https://www.youtube.com/watch?v=ieTH5lVhNaY&list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ&index=2)
- **IEEE 802.3 Standards** : [IEEE Ethernet Working Group](https://www.ieee802.org/3/)
- **Fiber Optic Association** : [Fiber Types Guide](https://www.thefoa.org/tech/ref/basic/fiber.html)
- **Cable tester tools** : Fluke Networks, Klein Tools
- **SFP Compatibility** : Cisco/HP/Ubiquiti compatibility matrices

---

## 📝 Commandes à retenir

### Packet Tracer

```cisco
# Vérifier interfaces disponibles
Router# show ip interface brief

# Activer interface
Router(config)# interface GigabitEthernet0/0/0
Router(config-if)# no shutdown

# Vérifier transceiver installé
Switch# show interfaces GigabitEthernet1/0/1 transceiver
```

### Sélection câble (mental checklist)

```
1. Distance ? (< 100m = copper, > 100m = fiber)
2. Types équipements ? (différents = straight, identiques = crossover/fiber)
3. Vitesse ? (1G = Cat5e, 10G = Cat6a ou fiber)
4. Environnement ? (EMI = STP ou fiber)
```

---

**Note :** Lab très simple mais rafraîchissement utile sur standards IEEE. Bases solides pour Day 03+ (TCP/IP, switching, routing).

**Prochaine étape :** Day 03 - OSI Model et encapsulation.
