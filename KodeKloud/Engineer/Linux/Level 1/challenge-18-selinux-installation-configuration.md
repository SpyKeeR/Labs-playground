# Challenge 18 : SELinux Installation and Configuration

**Date** : 7 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator I  

---

## 🎯 Objectif

Installer SELinux sur App Server 2 et le désactiver de manière permanente pour permettre des tests de sécurité avant configuration complète.

---

## 📋 Énoncé

Suite à un audit de sécurité, l'équipe sécurité de xFusionCorp Industries a décidé d'améliorer la sécurité applicative avec SELinux. Pour démarrer les tests, les exigences suivantes ont été établies pour App server 2 :

1. Installer les packages SELinux requis
2. Désactiver SELinux de manière **permanente** (réactivation ultérieure après configuration)
3. Pas de reboot nécessaire (maintenance prévue cette nuit)
4. Le statut final après reboot doit être `disabled`

**Serveur cible** : `steve@stapp02`

---

## ✅ Résolution

### 1. Connexion au serveur

```bash
ssh steve@stapp02
```

### 2. Désactiver SELinux immédiatement (mode permissive)

```bash
sudo setenforce 0
```

**Explication** : `setenforce 0` passe SELinux en mode `Permissive` immédiatement (runtime), permettant de continuer les opérations sans bloquer de processus. Ne survit pas au reboot.

### 3. Installer les packages SELinux

```bash
sudo yum install selinux-policy selinux-policy-targeted policycoreutils
```

**Packages installés** :
- `selinux-policy` : Politique de sécurité de base
- `selinux-policy-targeted` : Politique ciblée (protège services spécifiques, laisse le reste en unconfined)
- `policycoreutils` : Outils de gestion SELinux (`setenforce`, `sestatus`, `semanage`, etc.)

### 4. Désactiver SELinux de manière permanente

Éditer le fichier de configuration principal :

```bash
sudo vi /etc/selinux/config
```

Modifier la ligne `SELINUX=` :

```
SELINUX=disabled
```

**Alternative** : Le fichier `/etc/sysconfig/selinux` est un lien symbolique vers `/etc/selinux/config` (équivalent).

**Explication** : Cette modification est lue au boot. Après le reboot planifié, SELinux sera complètement désactivé.

### 5. Validation

Vérifier le statut actuel :

```bash
sestatus
```

**Sortie attendue avant reboot** :
```
SELinux status:                 enabled
Current mode:                   permissive
Mode from config file:          disabled
```

**Sortie attendue après reboot** :
```
SELinux status:                 disabled
```

---

## 🏷️ Tags

`#Linux` `#SELinux` `#Security` `#RHEL` `#KodeKloud` `#PolicyManagement`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
