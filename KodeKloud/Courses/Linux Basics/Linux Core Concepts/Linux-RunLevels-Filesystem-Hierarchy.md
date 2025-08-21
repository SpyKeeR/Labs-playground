# Labo - Linux Kernel, RunLevels, Filesystem Hierarchy Standard (FHS)

- Accéder aux labs pratiques : [Labo](https://kodekloud.com/free-labs/linux/linux-kernel-modules-boot-and-filetypes)

---

## Exécuter une commande nécessitant les privilèges **sudo**
```bash
    $ sudo ls /root
```
---

## Vérifier quel est le processus d’initialisation (init) utilisé (systemd ou sysV)
```bash
    $ sudo ls -l /sbin/init
```
---

## Vérifier la **cible systemd par défaut** (ex : `graphical.target` ou `multi-user.target`)
```bash
    $ sudo systemctl get-default
```
---

## Changer la cible systemd par défaut en **multi-user.target**
```bash
    $ sudo systemctl set-default multi-user.target
```
---

## Vérifier le type du fichier **firefox.deb** (situé dans `/root`)
```bash
    $ sudo file /root/firefox.deb
```
---

## Vérifier le type du fichier **sample_script.sh** (situé dans `/root`)
```bash
    $ sudo file /root/sample_script.sh
```
---

## Dans quel répertoire installer un **IDE tiers** (third-party) ?

Les logiciels tiers sont habituellement installés dans :  /opt

---

## Dans quel répertoire se trouvent les fichiers liés aux périphériques blocs visibles via `lsblk` ?

Les fichiers de périphériques (Device Nodes) sont situés dans :   /dev

---

## Quel est le nom du **vendeur (vendor)** du **contrôleur Ethernet** de ce système ?

Utiliser la commande suivante puis chercher la section **network** :  
```bash
    $ sudo lshw
```