# Labo - Shell Bash Linux

- Accéder aux labs pratiques : [Labo](https://kodekloud.com/free-labs/linux/linux-bash-prompt)

---

## 1. Vérifier le shell par défaut de l’utilisateur courant  
```bash
    $ echo $SHELL
```
---

## 2. Changer le shell de l’utilisateur `bob` de **Bash** vers **Bourne Shell**
```bash
    $ chsh -s /bin/sh bob
```
---

## 3. Afficher la valeur de la variable d’environnement **TERM**
```bash
    $ echo $TERM
```
---

## 4. Créer une variable d’environnement persistante **PROJECT=MERCURY**  
```bash
    $ echo export PROJECT=MERCURY >> ~/.profile
```
---

## 5. Quel répertoire suivant ne fait pas partie de la variable PATH ?
```bash
    /opt/caleston-code
```
---

## 6. Créer un alias **up** pour la commande **uptime** et le rendre persistant
```bash
    $ echo alias up=uptime >> ~/.profile
```
---

## 7. Modifier l’invite de commande de `bob` pour afficher la date  
Format attendu : **[Wed Apr 22]bob@caleston-lp10:~$**  et rendre la modification persistante.
```bash
    echo 'PS1=[\d]\u@\h:\w$' >> ~/.profile
```