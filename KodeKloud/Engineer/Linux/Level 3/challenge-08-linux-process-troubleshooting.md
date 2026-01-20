# Challenge 08 - Linux Process Troubleshooting

**Difficulté** : Level 3  
**Domaine** : Apache, Process Management, Port Conflicts  
**Date** : 18 janvier 2026

---

## 📋 Consigne

L'équipe de support production de xFusionCorp Industries a déployé des outils de monitoring pour surveiller tous les services et applications des systèmes. L'un des systèmes de monitoring a signalé une indisponibilité du service Apache sur l'un des serveurs d'applications dans le Stratos DC.

Identifier le serveur défaillant et corriger le problème. S'assurer que le service Apache est démarré et opérationnel sur tous les serveurs d'applications. Ils n'ont peut-être pas encore hébergé de code sur ces serveurs, donc pas besoin de s'inquiéter si Apache ne sert aucune page. Il faut simplement s'assurer que le service fonctionne. De plus, s'assurer qu'Apache s'exécute sur le port 5003 sur tous les serveurs d'applications.

---

## 🔧 Réalisation

### Étape 1 : Connexion App Server 1 (diagnostic)

```bash
ssh tony@stapp01
# Password: Ir0nM@n (user tony)
```

### Étape 2 : Diagnostic réseau - Identifier processus sur port 5003

```bash
sudo ss -tulnp
```

**Output** :
```
Netid State   Recv-Q Send-Q Local Address:Port   Peer Address:Port  Process
tcp   LISTEN  0      100    0.0.0.0:5003         0.0.0.0:*          users:(("sendmail",pid=2345,fd=4))
tcp   LISTEN  0      128    0.0.0.0:22           0.0.0.0:*          users:(("sshd",pid=1234,fd=3))
tcp   LISTEN  0      100    127.0.0.1:25         0.0.0.0:*          users:(("sendmail",pid=2345,fd=5))
```

**Analyse** :
- **Port 5003** : Occupé par **sendmail** (PID 2345) ❌
- **Conflit** : Apache ne peut pas démarrer car port déjà utilisé

**Options ss** :
- `-t` : Sockets TCP
- `-u` : Sockets UDP
- `-l` : Sockets en écoute (LISTEN)
- `-n` : Numérique (pas de résolution DNS)
- `-p` : Processus associés

### Étape 3 : Arrêt Sendmail (libération port)

```bash
sudo systemctl stop sendmail
```

**Vérification** :
```bash
sudo ss -tulnp | grep :5003
# (vide) → Port 5003 libéré ✅
```

### Étape 4 : Reconfiguration Sendmail (port SMTP standard)

```bash
sudo vi /etc/mail/sendmail.mc
```

**Rechercher ligne** (utiliser `/5003` dans vi) :
```m4
DAEMON_OPTIONS(`Port=5003,Addr=127.0.0.1, Name=MTA')dnl
```

**Modifier** :
```m4
DAEMON_OPTIONS(`Port=smtp,Addr=127.0.0.1, Name=MTA')dnl
```

**Changement** :
- `Port=5003` → `Port=smtp` (résolu en port 25 via `/etc/services`)

**Sauvegarder** : `:wq`

### Étape 5 : Compilation configuration Sendmail

```bash
sudo make -C /etc/mail
```

**Explication** :
- Sendmail utilise fichiers `.mc` (source macros m4) compilés en `.cf` (configuration native)
- **Commande équivalente** : `m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf`

**Output** :
```
/usr/bin/m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf
chmod 644 /etc/mail/sendmail.cf
```

### Étape 6 : Redémarrage Sendmail

```bash
sudo systemctl start sendmail
```

**Vérification nouveau port** :
```bash
sudo ss -tulnp | grep sendmail
# tcp LISTEN 0 100 127.0.0.1:25  0.0.0.0:* users:(("sendmail",pid=3456,fd=4))
```

**Confirmation** :
- Sendmail écoute maintenant sur **port 25** (SMTP standard) ✅
- Port 5003 disponible pour Apache ✅

### Étape 7 : Démarrage Apache

```bash
sudo systemctl start httpd
```

**Vérification service** :
```bash
sudo systemctl status httpd
# Active (running)
```

**Vérification port** :
```bash
sudo ss -tulnp | grep :5003
# tcp LISTEN 0 128 0.0.0.0:5003 0.0.0.0:* users:(("httpd",pid=3678,fd=4))
```

**Confirmation** :
- Apache écoute sur **port 5003** ✅

### Étape 8 : Validation multi-serveurs

**Test stapp01** :
```bash
curl stapp01:5003
# Output : Page HTML Apache (HTTP 200 OK)
```

**Test stapp02** :
```bash
curl stapp02:5003
# Output : Page HTML Apache (HTTP 200 OK)
```

**Test stapp03** :
```bash
curl stapp03:5003
# Output : Page HTML Apache (HTTP 200 OK)
```

**Résultat** : ✅ Apache opérationnel sur les 3 serveurs sur port 5003

---

## 📊 Résumé problème

**Symptôme** :
- Apache refuse de démarrer sur stapp01

**Cause racine** :
- Sendmail configuré pour écouter sur port 5003 (au lieu de 25)
- Sendmail démarre avant Apache (ordre systemd)
- Apache ne peut pas bind port 5003 (déjà occupé)

**Solution** :
1. Arrêter Sendmail
2. Reconfigurer Sendmail : `Port=5003` → `Port=smtp` (25)
3. Compiler configuration `.mc` → `.cf`
4. Redémarrer Sendmail sur port 25
5. Démarrer Apache sur port 5003 libéré

**Architecture finale** :
```
stapp01, stapp02, stapp03
├── Sendmail : Port 25 (SMTP standard)
└── Apache   : Port 5003 (personnalisé)
```

---

## 🔗 Ressources

**Documentation ss** :
- [ss man page](https://man7.org/linux/man-pages/man8/ss.8.html)
- [iproute2 Documentation](https://wiki.linuxfoundation.org/networking/iproute2)

**Sendmail Configuration** :
- [Sendmail Documentation](https://www.proofpoint.com/us/products/email-protection/open-source-email-solution)
- [m4 Macro Processor](https://www.gnu.org/software/m4/manual/)

**systemd Service Management** :
- [systemd.service](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [systemctl Documentation](https://www.freedesktop.org/software/systemd/man/systemctl.html)
