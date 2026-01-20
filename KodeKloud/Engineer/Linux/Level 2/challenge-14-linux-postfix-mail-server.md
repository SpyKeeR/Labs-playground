# Challenge 14 : Linux Postfix Mail Server

**Date** : 10 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐⭐ (Niveau 2 - Complexe)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Configurer un serveur mail complet sur Stork DC :
- Installer et configurer **Postfix** (MTA - Mail Transfer Agent)
- Installer et configurer **Dovecot** (MDA - IMAP/POP3)
- Créer compte email `siva@stratos.xfusioncorp.com`
- Configurer SMTP-Auth entre Postfix et Dovecot

---

## 📋 Énoncé

xFusionCorp Industries a prévu de mettre en place un serveur de messagerie commun dans le Stork DC. Après plusieurs réunions et recommandations, ils ont décidé d'utiliser postfix comme agent de transfert de courrier et dovecot comme serveur IMAP/POP3. Nous aimerions que vous effectuiez les étapes suivantes :

1. Installer et configurer **postfix** sur le serveur de messagerie Stork DC.
2. Créer un compte email `siva@stratos.xfusioncorp.com` identifié par `8FmzjvFU6S`.
3. Définir son répertoire de messagerie à `/home/siva/Maildir`.
4. Installer et configurer **dovecot** sur le même serveur.

**Serveur concerné** :
- `stmail01` (user `groot`)

---

## 🔧 Résolution

### Approche

1. Se connecter sur le serveur mail
2. Installer Postfix
3. Configurer `/etc/postfix/main.cf` (hostname, domain, interfaces, Maildir, SMTP-Auth)
4. Installer Dovecot
5. Configurer Dovecot (protocols, auth, mail location, Postfix SASL)
6. Créer utilisateur `siva` avec mot de passe
7. Démarrer les services

### Commandes exécutées

```bash
ssh groot@stmail01
sudo -i

# ========== INSTALLATION POSTFIX ==========
yum install postfix -y

# ========== CONFIGURATION POSTFIX ==========
vi /etc/postfix/main.cf
```

**Modifications `/etc/postfix/main.cf`** :

```bash
# line 95 : uncomment and specify hostname
myhostname = mail.srv.world

# line 102 : uncomment and specify domain name
mydomain = srv.world

# line 118 : uncomment
myorigin = $mydomain

# line 135 : change
inet_interfaces = all

# line 138 : change it if use only IPv4
inet_protocols = ipv4

# line 183 : add
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain

# line 283 : uncomment and specify your local network
mynetworks = 127.0.0.0/8, 10.0.0.0/24

# line 438 : uncomment (use Maildir)
home_mailbox = Maildir/

# line 593 : add
# hide the kind or version of SMTP software
smtpd_banner = $myhostname ESMTP

# add follows to last line
# disable SMTP VRFY command
disable_vrfy_command = yes

# require HELO command to sender hosts
smtpd_helo_required = yes

# limit an email size
# example below means 10M bytes limit
message_size_limit = 10240000

# SMTP-Auth settings
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
smtpd_sasl_local_domain = $myhostname
smtpd_recipient_restrictions = 
  permit_mynetworks,
  permit_sasl_authenticated,
  reject_unauth_destination
```

```bash
# Démarrer Postfix
systemctl enable --now postfix

# ========== INSTALLATION DOVECOT ==========
yum install dovecot -y

# ========== CONFIGURATION DOVECOT ==========
vi /etc/dovecot/dovecot.conf
```

**Modifications `/etc/dovecot/dovecot.conf`** :
```bash
# line 30 : uncomment (if not use IPv6, remove [::])
listen = *, ::
```

```bash
vi /etc/dovecot/conf.d/10-auth.conf
```

**Modifications `/etc/dovecot/conf.d/10-auth.conf`** :
```bash
# line 10 : uncomment and change (allow plain text auth)
disable_plaintext_auth = no

# line 100 : add
auth_mechanisms = plain login
```

```bash
vi /etc/dovecot/conf.d/10-mail.conf
```

**Modifications `/etc/dovecot/conf.d/10-mail.conf`** :
```bash
# line 30 : uncomment and add
mail_location = maildir:~/Maildir
```

```bash
vi /etc/dovecot/conf.d/10-master.conf
```

**Modifications `/etc/dovecot/conf.d/10-master.conf`** :
```bash
# line 107-109 : uncomment and add like follows
  # Postfix smtp-auth
  unix_listener /var/spool/postfix/private/auth {
    mode = 0666
    user = postfix
    group = postfix
  }
```

```bash
vi /etc/dovecot/conf.d/10-ssl.conf
```

**Modifications `/etc/dovecot/conf.d/10-ssl.conf`** :
```bash
# line 8 : change (not require SSL)
ssl = yes
```

```bash
# Démarrer Dovecot
systemctl enable --now dovecot

# ========== CRÉATION UTILISATEUR MAIL ==========
useradd -m siva
passwd siva
# Password: 8FmzjvFU6S
```

### Explications

**Architecture mail server** :
- **Postfix (MTA)** : Envoi/réception emails via SMTP (port 25)
- **Dovecot (MDA)** : Accès boîtes mail via IMAP (143) / POP3 (110)
- **SMTP-Auth** : Postfix délègue authentification à Dovecot via socket UNIX

**Directives Postfix clés** :
- `myhostname` : FQDN serveur mail
- `mydomain` : Domaine emails
- `myorigin` : Domaine expéditeur par défaut
- `inet_interfaces` : Interfaces écoute SMTP (`all` = toutes)
- `mydestination` : Domaines acceptés en livraison locale
- `mynetworks` : Réseaux autorisés relay sans auth
- `home_mailbox` : Format stockage (`Maildir/` = un fichier par email)

**Directives Dovecot clés** :
- `disable_plaintext_auth = no` : Autorise auth plain text (à sécuriser avec TLS en prod)
- `auth_mechanisms = plain login` : Méthodes authentification
- `mail_location = maildir:~/Maildir` : Emplacement mailboxes
- `unix_listener /var/spool/postfix/private/auth` : Socket SASL pour Postfix

---

## ✅ Validation

```bash
# Vérifier services actifs
systemctl status postfix
systemctl status dovecot

# Tester SMTP (port 25)
telnet localhost 25
# EHLO test
# QUIT

# Tester IMAP (port 143)
telnet localhost 143
# a1 LOGIN siva 8FmzjvFU6S
# a2 LIST "" "*"
# a3 LOGOUT

# Envoyer email test
mail -s "Test" siva@stratos.xfusioncorp.com <<< "Test email"

# Vérifier logs
tail -f /var/log/maillog
```

---

## 📌 Commandes utiles

```bash
# ========== POSTFIX ==========
# Vérifier configuration (non-default settings)
postconf -n

# Lister toutes directives
postconf

# Tester directive spécifique
postconf myhostname

# Vérifier queue emails
postqueue -p
mailq

# Supprimer email queue
postsuper -d <queue_id>

# Supprimer tous emails queue
postsuper -d ALL

# Recharger configuration
systemctl reload postfix

# Logs Postfix
tail -f /var/log/maillog

# ========== DOVECOT ==========
# Vérifier configuration
doveconf -n

# Lister utilisateurs
doveadm user '*'

# Tester authentification user
doveadm auth test siva 8FmzjvFU6S

# Logs Dovecot
tail -f /var/log/dovecot.log

# ========== TESTS MAIL ==========
# Envoyer email
mail -s "Subject" recipient@domain.com <<< "Body"

# Lire emails user
su - siva
mail

# Tester SMTP telnet
telnet localhost 25

# Tester IMAP telnet
telnet localhost 143

# Tester SMTP-Auth
telnet localhost 25
EHLO test
AUTH PLAIN
```

---

## ⚠️ Notes importantes

**Sécurité production** :
- Activer TLS/SSL (`smtpd_use_tls = yes`)
- Certificats valides (`smtpd_tls_cert_file`, `smtpd_tls_key_file`)
- Désactiver plain text auth sans TLS
- Configurer SPF/DKIM/DMARC
- Firewall : ouvrir ports 25, 587 (submission), 143, 993 (IMAPS)

**Format Maildir vs mbox** :
- `Maildir/` : Un fichier par email (recommandé, concurrent-safe)
- `mbox` : Tous emails dans un seul fichier (legacy, risque corruption)

**Relay ouvert** :
- Vérifier `mydestination` et `relay_domains` bien configurés
- `smtpd_recipient_restrictions` doit rejeter relay non autorisé

---

**Tags** : `postfix` `dovecot` `MTA` `MDA` `SMTP` `IMAP` `mail server` `SMTP-Auth` `Maildir` `Level 2`
