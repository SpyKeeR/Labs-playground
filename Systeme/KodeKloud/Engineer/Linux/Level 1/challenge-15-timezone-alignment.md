# KodeKloud Engineer - Challenge 15 : Timezone Alignment

**Date :** 6 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - System Configuration & Time Management  
**Difficulté :** Easy  
**Durée :** ~15 minutes  
**Statut :** ✅ Résolu

---

## 🎯 Objectif

Synchroniser les paramètres de timezone sur tous les serveurs pour correspondre au fuseau horaire local du datacenter.

---

## 📋 Énoncé

**Contexte :** Lors du daily standup, il a été noté que les paramètres de timezone des Nautilus Application Servers dans le Stratos Datacenter sont incohérents avec le timezone local du datacenter.

**Timezone local datacenter :** `America/Argentina/Mendoza`

**Mission :** Synchroniser les paramètres timezone de **tous les App servers** pour correspondre à `America/Argentina/Mendoza`.

**Serveurs cibles :**
- App Server 1 : `tony@stapp01`
- App Server 2 : `steve@stapp02`
- App Server 3 : `banner@stapp03`

---

## 🔧 Résolution

### App Server 1 (stapp01)

#### Étape 1 : Connexion
```bash
ssh tony@stapp01
```

#### Étape 2 : Vérifier timezone actuelle
```bash
timedatectl status
```

**Output (exemple avant modification) :**
```
               Local time: Tue 2026-01-06 10:45:32 UTC
           Universal time: Tue 2026-01-06 10:45:32 UTC
                 RTC time: Tue 2026-01-06 10:45:32
                Time zone: Etc/UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

**Analyse :**
- **Time zone actuelle** : `Etc/UTC`
- **Offset** : +0000 (UTC = GMT+0)
- **Target** : `America/Argentina/Mendoza` (GMT-3)

---

#### Étape 3 : Définir nouveau timezone
```bash
sudo timedatectl set-timezone America/Argentina/Mendoza
```

**⚠️ Note :** Aucun output = succès (commande silencieuse si OK).

---

#### Étape 4 : Vérifier changement appliqué
```bash
timedatectl status
```

**Output (après modification) :**
```
               Local time: Tue 2026-01-06 07:45:32 -03
           Universal time: Tue 2026-01-06 10:45:32 UTC
                 RTC time: Tue 2026-01-06 10:45:32
                Time zone: America/Argentina/Mendoza (-03, -0300)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

**Vérification :**
- ✅ **Time zone** : `America/Argentina/Mendoza`
- ✅ **Offset** : -03 (GMT-3)
- ✅ **Local time** : Ajusté automatiquement (UTC 10:45 → Local 07:45)

---

### App Server 2 (stapp02)

```bash
ssh steve@stapp02
timedatectl status
# (noter timezone actuelle)

sudo timedatectl set-timezone America/Argentina/Mendoza

timedatectl status
# Time zone: America/Argentina/Mendoza (-03, -0300)
```

---

### App Server 3 (stapp03)

```bash
ssh banner@stapp03
timedatectl status
# (noter timezone actuelle)

sudo timedatectl set-timezone America/Argentina/Mendoza

timedatectl status
# Time zone: America/Argentina/Mendoza (-03, -0300)
```

---

## 🎓 Commandes à Retenir

```bash
# Voir status complet (timezone, NTP, RTC)
timedatectl status
# (ou simplement : timedatectl)

# Changer timezone
sudo timedatectl set-timezone America/Argentina/Mendoza
sudo timedatectl set-timezone Europe/Paris
sudo timedatectl set-timezone UTC

# Lister timezones disponibles
timedatectl list-timezones

# Filtrer par région
timedatectl list-timezones | grep America
timedatectl list-timezones | grep Europe

# Définir heure manuellement
sudo timedatectl set-time "2026-01-06 15:30:00"

# Activer/Désactiver NTP
sudo timedatectl set-ntp true
sudo timedatectl set-ntp false

# Hardware clock
sudo hwclock --show            # Lire RTC
sudo hwclock --systohc         # Sync system → RTC
sudo hwclock --hctosys         # Sync RTC → system

# Vérifier fichier timezone
ls -l /etc/localtime
readlink /etc/localtime

# Alternative manuelle (sans timedatectl)
sudo ln -sf /usr/share/zoneinfo/TIMEZONE /etc/localtime
```

---

**Tags :** #Linux #Timezone #timedatectl #NTP #SystemAdministration #Time #KodeKloud
