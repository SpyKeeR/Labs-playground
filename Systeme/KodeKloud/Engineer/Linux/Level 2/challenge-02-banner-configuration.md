# Challenge 02 : Banner Configuration

**Date** : 7 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Configurer un message MOTD (Message of the Day) sur tous les serveurs applicatifs et de base de données pour maintenir la conformité de sécurité.

---

## 📋 Énoncé

Lors de la réunion mensuelle de conformité, il a été constaté que plusieurs serveurs du Stratos DC n'ont pas de bannière valide. L'équipe sécurité a fourni des templates approuvés à appliquer sur les serveurs pour maintenir la conformité. Ces bannières seront affichées à l'utilisateur lors d'une connexion réussie.

**Tâche** : Mettre à jour le message of the day sur tous les serveurs applicatifs et de base de données pour Nautilus.

**Template** : Utiliser le template approuvé situé à `/home/thor/nautilus_banner` sur le jump host.

**Serveurs cibles** : 
- App servers : `tony@stapp01`, `steve@stapp02`, `banner@stapp03`
- DB server : `peter@stdb01`

---

## ✅ Résolution

### 1. Transférer le template vers tous les serveurs

Depuis le jump host, copier le fichier banner vers chaque serveur (dans `/tmp` pour éviter problèmes permissions) :

```bash
scp /home/thor/nautilus_banner tony@stapp01:/tmp
scp /home/thor/nautilus_banner steve@stapp02:/tmp
scp /home/thor/nautilus_banner banner@stapp03:/tmp
scp /home/thor/nautilus_banner peter@stdb01:/tmp
```

**Explication** :
- `scp` : Secure Copy Protocol (transfert fichier via SSH)
- Source : `/home/thor/nautilus_banner` (fichier local)
- Destination : `user@host:/tmp` (répertoire temporaire sur serveur distant)
- `/tmp` utilisé car accessible en écriture sans sudo

### 2. Installer le banner sur chaque serveur

**App Server 1** :
```bash
ssh tony@stapp01
sudo mv /tmp/nautilus_banner /etc/motd
exit
```

**App Server 2** :
```bash
ssh steve@stapp02
sudo mv /tmp/nautilus_banner /etc/motd
exit
```

**App Server 3** :
```bash
ssh banner@stapp03
sudo mv /tmp/nautilus_banner /etc/motd
exit
```

**DB Server** :
```bash
ssh peter@stdb01
sudo mv /tmp/nautilus_banner /etc/motd
exit
```

**Explication** :
- `sudo mv /tmp/nautilus_banner /etc/motd` : Déplace fichier vers `/etc/motd` avec permissions root
- `/etc/motd` : Message of the Day, affiché après login SSH réussi
- `mv` écrase l'ancien MOTD si existant

### 3. Validation

Se reconnecter à un serveur pour vérifier l'affichage du banner :

```bash
ssh tony@stapp01
# Banner s'affiche après authentification
```

---

## 🏷️ Tags

`#Linux` `#MOTD` `#SSH` `#Security` `#SystemAdmin` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
