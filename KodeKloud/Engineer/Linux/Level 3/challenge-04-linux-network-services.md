# Challenge 04 - Linux Network Services

**Difficulté** : Level 3  
**Domaine** : Network Troubleshooting, Port Conflicts, iptables  
**Date** : 18 janvier 2026

---

## 📋 Consigne

Notre outil de monitoring a signalé un problème dans le Datacenter Stratos. L'un de nos serveurs applicatifs rencontre un problème, car son service Apache n'est pas accessible sur le port 5001 (qui est le port Apache). Le service lui-même pourrait être arrêté, le pare-feu pourrait être en cause, ou quelque chose d'autre pourrait causer le problème.

Utilisez des outils comme telnet, netstat, etc. pour trouver et corriger le problème. Assurez-vous également qu'Apache est accessible depuis le jump host sans compromettre les paramètres de sécurité.

Une fois corrigé, vous pouvez tester avec la commande curl http://stapp01:5001 depuis le jump host.

Note : Veuillez ne pas essayer de modifier le code index.html existant, car cela entraînerait l'échec de la tâche.

---

## 🔧 Réalisation

### Étape 1 : Connexion App Server 1 et diagnostic initial

```bash
ssh tony@stapp01
# Password: Ir0nM@n
```

### Étape 2 : Vérifier status Apache

```bash
systemctl status httpd
# Output : Active (running) OU Inactive (dead)
```

**Si inactive** : Service down (simple start), **MAIS** challenge plus complexe.

### Étape 3 : Vérifier port 5001 listening

```bash
netstat -tuln | grep 5001
# Output :
# tcp   0   0 127.0.0.1:5001   0.0.0.0:*   LISTEN
```

**Analyse** :
- Port 5001 **ALREADY listening** (autre service utilise)
- `127.0.0.1:5001` : Bind localhost only (pas accessible remote)

**Identify port owner** :
```bash
sudo netstat -tulnp | grep 5001
# Output :
# tcp   0   0 127.0.0.1:5001   0.0.0.0:*   LISTEN   1234/sendmail
```

**Root cause identifiée** : **Sendmail** utilise port 5001 (conflict avec Apache).

### Étape 4 : Confirmer service port 5001 (telnet)

```bash
telnet localhost 5001
# Output :
# Trying 127.0.0.1...
# Connected to localhost.
# Escape character is '^]'.
# 220 stapp01.stratos.xfusioncorp.com ESMTP Sendmail 8.15.2/8.15.2; ...
```

**Confirmation** : Port 5001 = Sendmail SMTP (pas Apache).

**Quitter telnet** : `Ctrl+]` puis `quit`

### Étape 5 : Arrêter Sendmail (libérer port 5001)

```bash
sudo systemctl stop sendmail
```

**Vérifier port libéré** :
```bash
netstat -tuln | grep 5001
# (Aucun output = port libre ✅)
```

### Étape 6 : Reconfigurer Sendmail port SMTP standard

**Problème** : Sendmail redémarrera port 5001 au reboot (configuration persistante).

**Solution** : Modifier config Sendmail port défaut SMTP (25 ou 587).

```bash
sudo vi /etc/mail/sendmail.mc
```

**Rechercher ligne** (environ ligne 116) :
```bash
DAEMON_OPTIONS(`Port=5001,Addr=127.0.0.1, Name=MTA')dnl
```

**Modifier port 5001 → smtp** :
```bash
DAEMON_OPTIONS(`Port=smtp,Addr=127.0.0.1, Name=MTA')dnl
```

**Note** : `smtp` = alias port 25 (défaut SMTP, défini `/etc/services`).

**Sauvegarder** : `:wq`

**Rebuild Sendmail config** :
```bash
# Compile sendmail.mc → sendmail.cf
sudo make -C /etc/mail

# OU alternative
sudo m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf
```

### Étape 7 : Redémarrer Sendmail (port SMTP)

```bash
sudo systemctl start sendmail
```

**Vérifier Sendmail nouveau port** :
```bash
sudo netstat -tulnp | grep sendmail
# Output :
# tcp   0   0 127.0.0.1:25   0.0.0.0:*   LISTEN   5678/sendmail
```

✅ Sendmail écoute port 25 (standard SMTP), port 5001 libéré.

### Étape 8 : Démarrer Apache

```bash
sudo systemctl start httpd
```

**Vérifier Apache port 5001** :
```bash
sudo netstat -tulnp | grep 5001
# Output :
# tcp   0   0 0.0.0.0:5001   0.0.0.0:*   LISTEN   6789/httpd
```

✅ Apache écoute port 5001 (bind all interfaces `0.0.0.0`).

### Étape 9 : Test local Apache

```bash
curl localhost:5001
# Output : Page HTML index.html ✅
```

### Étape 10 : Test remote depuis Jump Host

```bash
# Depuis Jump Host
curl stapp01:5001
# Output : Connection refused ❌
```

**Problème** : Firewall bloque port 5001 (iptables).

### Étape 11 : Vérifier iptables rules

```bash
# Retour App Server 1
ssh tony@stapp01

sudo iptables -L -n -v
# Output :
# Chain INPUT (policy ACCEPT)
# (Pas de rule ACCEPT port 5001)
```

**iptables active MAIS** pas de rule autorisant port 5001 externe.

### Étape 12 : Ajouter rule iptables ACCEPT port 5001

```bash
sudo iptables -I INPUT 1 -p tcp --dport 5001 -j ACCEPT
```

**Explication** :
- `-I INPUT 1` : Insert rule position 1 (top, processed first)
- `-p tcp` : Protocol TCP
- `--dport 5001` : Destination port 5001
- `-j ACCEPT` : Jump target ACCEPT (allow traffic)

**Vérifier rule ajoutée** :
```bash
sudo iptables -L -n -v
# Output :
# Chain INPUT (policy ACCEPT)
# 1   ACCEPT   tcp  --  *  *  0.0.0.0/0  0.0.0.0/0  tcp dpt:5001
```

### Étape 13 : Sauvegarder rules iptables (persistent)

```bash
sudo service iptables save
# Output : iptables: Saving firewall rules to /etc/sysconfig/iptables
```

**Restart iptables** (reload rules) :
```bash
sudo systemctl restart iptables
```

### Étape 14 : Validation finale remote

```bash
# Depuis Jump Host
curl http://stapp01:5001
# Output : Page HTML index.html ✅
```

✅ Apache accessible depuis Jump Host.

## 🔗 Ressources

**Network Tools** :
- [netstat Manual](https://linux.die.net/man/8/netstat)
- [ss Command](https://man7.org/linux/man-pages/man8/ss.8.html)
- [lsof Examples](https://www.thegeekstuff.com/2012/08/lsof-command-examples/)

**Sendmail** :
- [Sendmail Documentation](https://www.sendmail.org/documentation.html)
- [sendmail.mc Configuration](https://www.sendmail.com/sm/open_source/docs/)

**iptables** :
- [iptables Tutorial](https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html)
- [Netfilter Documentation](https://www.netfilter.org/documentation/)