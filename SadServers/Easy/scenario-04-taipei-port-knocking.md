# Scenario 04 : "Taipei" - Come a-knocking

**Date** : 7 janvier 2026  
**Plateforme** : SadServers  
**Niveau** : Easy  

---

## 🎯 Objectif

Accéder à un serveur web sur port 80 protégé par Port Knocking en trouvant le port correct à "frapper" pour débloquer l'accès.

---

## 📋 Énoncé

Un serveur web tourne sur le port `:80` mais est protégé par **Port Knocking**. Trouver le "knock" nécessaire (envoi d'un SYN à un seul port, pas une séquence) pour pouvoir exécuter `curl localhost`.

**Test de validation** : `curl localhost` retourne un message avec md5sum `fe474f8e1c29e9f412ed3b726369ab65`  
(Note : le md5sum inclut le terminateur newline : `echo $(curl localhost)`)

**Contraintes** :
- Time to Solve : 15 minutes
- OS : Debian 11
- Root Access : Non

---

## ✅ Résolution

### 1. Vérifier les ports à l'écoute

```bash
ss -tuln
```

**Explication** :
- `ss` : Socket statistics (remplace `netstat`)
- `-t` : TCP sockets
- `-u` : UDP sockets
- `-l` : Listening (ports à l'écoute)
- `-n` : Numérique (pas de résolution DNS)

**Sortie attendue** : Liste des ports ouverts (TCP et UDP) sur la machine.

### 2. Découvrir l'outil client knock

```bash
dpkg -l | grep knock
```

**Explication** : 
- `dpkg -l` : Liste tous les packages installés (Debian/Ubuntu)
- `grep knock` : Filtre les packages contenant "knock"

**Résultat attendu** : Package `knockd` ou `knock` installé (client/serveur port knocking).

### 3. Tenter le knock sur chaque port à l'écoute

Pour chaque port identifié dans `ss -tuln`, tenter un knock :

**TCP ports** :
```bash
knock localhost <PORT>
curl localhost
```

**UDP ports** :
```bash
knock localhost -u <PORT>
curl localhost
```

**Explication** :
- `knock localhost <PORT>` : Envoie un paquet SYN TCP au port spécifié
- `knock localhost -u <PORT>` : Envoie un paquet UDP au port spécifié
- Après chaque knock, tester `curl localhost` pour vérifier si accès débloqué

**Processus de recherche** :
1. Lister tous les ports à l'écoute
2. Pour chaque port, exécuter `knock localhost <PORT>`
3. Tester immédiatement `curl localhost`
4. Si échec, passer au port suivant
5. Si succès, vérifier md5sum

### 4. Validation

Une fois le bon port trouvé et l'accès débloqué :

```bash
curl localhost
# Affiche message du serveur web

echo $(curl localhost) | md5sum
# fe474f8e1c29e9f412ed3b726369ab65
```

**Explication** : `echo $(curl localhost)` capture la sortie avec newline, puis `md5sum` calcule l'empreinte.


## 🏷️ Tags

`#Linux` `#Security` `#PortKnocking` `#Networking` `#Firewall` `#SadServers`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
