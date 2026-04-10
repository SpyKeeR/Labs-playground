# Challenge 15 : Linux Postfix Troubleshooting

**Date** : 13 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Résoudre problème service Postfix qui ne démarre pas sur le serveur mail Stork DC. Les utilisateurs de l'application monitoring signalent dysfonctionnement mail server.

---

## 📋 Énoncé

Certains utilisateurs de l'application de monitoring ont signalé des problèmes avec le serveur mail de xFusionCorp Industries. Ils disposent d'un serveur mail dans le datacenter Stork où ils utilisent l'agent de transfert de mail Postfix. Le service Postfix semble échouer. Essayez d'identifier la cause racine et de la corriger.

**Serveur concerné** : `stmail01.stratos.xfusioncorp.com`

---

## 🔧 Résolution

### Étape 1 : Diagnostic initial

Vérifier statut Postfix :
```bash
sudo systemctl status postfix
```

**Output** :
- Service `inactive (dead)` ou `failed`
- Postfix pas démarré

### Étape 2 : Tentative démarrage

```bash
sudo systemctl enable --now postfix
```

**Résultat** : Service échoue au démarrage.

### Étape 3 : Analyser logs erreur

Re-vérifier statut détaillé :
```bash
sudo systemctl status postfix
```

**Erreur identifiée** (logs systemd) :
```
Jan 13 10:19:57 stmail01.stratos.xfusioncorp.com postfix[975]: fatal: parameter inet_interfaces: no local interface found for ::1
```

**Diagnostic** :
- Postfix configuré pour écouter sur `::1` (IPv6 localhost)
- Serveur n'a pas d'interface IPv6 configurée
- Postfix refuse démarrer car interface manquante

### Étape 4 : Vérifier configuration réseau

```bash
ip a
```

**Observation** : Aucune adresse IPv6 configurée (pas de `inet6` dans output).

### Étape 5 : Corriger configuration Postfix

Éditer fichier config principal :
```bash
sudo vi /etc/postfix/main.cf
```

**Rechercher directive `inet_protocols`** (mode commande VI) :
```
/inet_protocols
```

**Ligne trouvée** :
```
inet_protocols = all
```

**Correction** : Remplacer par `ipv4` uniquement :
```
inet_protocols = ipv4
```

**Explication** :
- `inet_protocols = all` : Postfix écoute IPv4 ET IPv6
- `inet_protocols = ipv4` : Postfix écoute IPv4 uniquement
- Serveur n'ayant pas IPv6, forcer IPv4 résout l'erreur

### Étape 6 : Redémarrer Postfix

```bash
sudo systemctl restart postfix
```

### Étape 7 : Validation

Vérifier statut final :
```bash
sudo systemctl status postfix
```

**Output attendu** :
- `active (running)`
- Aucune erreur logs
- Process postfix actif (PID visible)

---

## 📌 Commandes utiles

```bash
# Vérifier statut Postfix
sudo systemctl status postfix

# Démarrer + activer boot
sudo systemctl enable --now postfix

# Redémarrer Postfix
sudo systemctl restart postfix

# Recharger config (sans restart)
sudo systemctl reload postfix

# Vérifier logs Postfix
sudo tail -50 /var/log/maillog        # RHEL/CentOS
sudo tail -50 /var/log/mail.log       # Debian/Ubuntu
sudo journalctl -u postfix -n 50

# Vérifier configuration active
postconf inet_protocols
postconf -n | grep inet_protocols

# Tester configuration Postfix
postfix check

# Vérifier interfaces réseau
ip a
ip -6 a          # IPv6 uniquement

# Vérifier ports écoute
sudo ss -tuln | grep :25
sudo netstat -tuln | grep :25
```

### Configuration inet_protocols

```bash
# Fichier /etc/postfix/main.cf

# Écoute IPv4 + IPv6
inet_protocols = all

# Écoute IPv4 uniquement
inet_protocols = ipv4

# Écoute IPv6 uniquement
inet_protocols = ipv6
```

---

## 💡 Points clés

**Cause racine** :
- Postfix configuré `inet_protocols = all` (IPv4 + IPv6)
- Serveur sans configuration IPv6
- Postfix refuse démarrer si interfaces déclarées manquantes

**Solution** :
- Forcer `inet_protocols = ipv4` (IPv4 uniquement)
- Alternative : Configurer IPv6 sur serveur (plus complexe, inutile si pas besoin)

**Erreurs similaires possibles** :
- `no local interface found for ::1` → IPv6 localhost manquant
- `no local interface found for 0.0.0.0` → IPv4 mal configuré (rare)

**Debugging workflow** :
1. `systemctl status` → identifier erreur
2. Analyser logs (journalctl, /var/log/maillog)
3. Vérifier config réseau (`ip a`)
4. Adapter config Postfix (`inet_protocols`)
5. Restart + validate

---

## ⚠️ Notes production

**IPv6 en production** :
- Si IPv6 requis → configurer interfaces système (`/etc/network/interfaces` ou NetworkManager)
- Si IPv6 inutile → forcer `inet_protocols = ipv4` (évite erreurs)
- Dual-stack (IPv4+IPv6) : Vérifier `::1` localhost bien présent (`ip -6 a`)

**Postfix restart vs reload** :
- `reload` : Recharge config sans couper connexions (emails en cours continuent)
- `restart` : Redémarre complet (queue emails pas affectée, mais connexions SMTP coupées)
- Après modif `inet_protocols` : **restart requis** (reload insuffisant)

---

**Tags** : `Postfix` `inet_protocols` `IPv6` `troubleshooting` `systemd` `mail-server` `Level 2`
