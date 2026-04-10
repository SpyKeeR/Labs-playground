# Challenge 05 - Iptables Installation and Configuration

**Difficulté** : Level 3  
**Domaine** : iptables, Firewall, Multi-Server Security  
**Date** : 18 janvier 2026

---

## 📋 Consigne

Nous avons l'un de nos sites web opérationnel sur notre infrastructure Nautilus dans le DC Stratos. Notre équipe de sécurité a soulevé une préoccupation concernant le fait que le port Apache, c'est-à-dire le 8088, est actuellement ouvert à tous car aucun pare-feu n'est installé sur ces hôtes. Nous avons donc décidé d'ajouter une couche de sécurité pour ces hôtes et après discussions et recommandations, nous sommes arrivés aux exigences suivantes :

1. Installer iptables et toutes ses dépendances sur chaque hôte applicatif.

2. Bloquer le port entrant 8088 sur toutes les applications pour tout le monde sauf pour l'hôte LBR.

3. S'assurer que les règles persistent, même après un redémarrage du système.

---

## 🔧 Réalisation

**Note** : Configuration identique sur 3 App Servers (stapp01, stapp02, stapp03).

### App Server 1 (stapp01)

#### Étape 1 : Connexion stapp01

```bash
ssh tony@stapp01
# Password: Ir0nM@n
```

#### Étape 2 : Installation iptables-services

```bash
sudo yum install iptables-services -y
```

**Packages installés** :
- `iptables-services` : systemd service files iptables
- `iptables` : iptables command-line tool (déjà installé généralement)

**Vérification** :
```bash
rpm -qa | grep iptables
# iptables-1.4.21-35.el7.x86_64
# iptables-services-1.4.21-35.el7.x86_64
```

#### Étape 3 : Configuration rules iptables

**Rule 1 : ACCEPT LBR (172.16.238.14)** :
```bash
sudo iptables -A INPUT -s 172.16.238.14/32 -p tcp --dport 8088 -j ACCEPT
```

**Explication** :
- `-A INPUT` : Append rule to INPUT chain
- `-s 172.16.238.14/32` : Source IP 172.16.238.14 (/32 = single host)
- `-p tcp` : Protocol TCP
- `--dport 8088` : Destination port 8088
- `-j ACCEPT` : Jump target ACCEPT (allow traffic)

**Rule 2 : REJECT all others** :
```bash
sudo iptables -A INPUT -p tcp --dport 8088 -j REJECT
```

**Explication** :
- `-A INPUT` : Append rule (after ACCEPT rule)
- `-p tcp --dport 8088` : TCP port 8088 (any source)
- `-j REJECT` : Reject traffic (send ICMP error)

**Order matters** :
```
Rule 1 : ACCEPT 172.16.238.14 → Match LBR → Allow ✅
Rule 2 : REJECT all        → Match others → Block ❌
```

First match wins → LBR autorisé, autres bloqués.

#### Étape 4 : Vérifier rules

```bash
sudo iptables -L -n -v
# Output :
# Chain INPUT (policy ACCEPT)
# 1   ACCEPT   tcp  --  *  *  172.16.238.14  0.0.0.0/0  tcp dpt:8088
# 2   REJECT   tcp  --  *  *  0.0.0.0/0      0.0.0.0/0  tcp dpt:8088  reject-with icmp-port-unreachable
```

#### Étape 5 : Sauvegarder rules (persistent)

```bash
sudo service iptables save
# Output : iptables: Saving firewall rules to /etc/sysconfig/iptables
```

**Fichier généré** : `/etc/sysconfig/iptables`
```bash
cat /etc/sysconfig/iptables
# *filter
# :INPUT ACCEPT [0:0]
# -A INPUT -s 172.16.238.14/32 -p tcp -m tcp --dport 8088 -j ACCEPT
# -A INPUT -p tcp -m tcp --dport 8088 -j REJECT --reject-with icmp-port-unreachable
# COMMIT
```

#### Étape 6 : Enable iptables service (boot)

```bash
sudo systemctl enable --now iptables
```

**Vérification** :
```bash
sudo systemctl status iptables
# Active (exited) - rules loaded
```

---

### App Server 2 (stapp02)

**Répéter étapes identiques** :

```bash
ssh steve@stapp02
# Password: Am3ric@

sudo yum install iptables-services -y
sudo iptables -A INPUT -s 172.16.238.14/32 -p tcp --dport 8088 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8088 -j REJECT
sudo service iptables save
sudo systemctl enable --now iptables
```

---

### App Server 3 (stapp03)

**Répéter étapes identiques** :

```bash
ssh banner@stapp03
# Password: BigGr33n

sudo yum install iptables-services -y
sudo iptables -A INPUT -s 172.16.238.14/32 -p tcp --dport 8088 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8088 -j REJECT
sudo service iptables save
sudo systemctl enable --now iptables
```

---

## 🔗 Ressources

**iptables Documentation** :
- [iptables Manual](https://linux.die.net/man/8/iptables)
- [Netfilter Tutorial](https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html)
- [iptables Essentials](https://www.digitalocean.com/community/tutorials/iptables-essentials-common-firewall-rules-and-commands)

**Security Patterns** :
- [Firewall Best Practices](https://www.cisecurity.org/insights/white-papers/cis-controls-v8-guide-to-network-security)
- [Least Privilege Principle](https://csrc.nist.gov/glossary/term/least_privilege)