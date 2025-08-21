# Labo - RPM & YUM

- Accéder aux labs pratiques : [Labo](https://kodekloud.com/free-labs/linux/yum-and-rpm)

---

## Quels gestionnaires de paquets utilise une machine CentOS ?
CentOS utilise :  RPM et YUM

---

## Trouver le nom exact du paquet **wget** installé avec `rpm`
```bash
    $ rpm -qa | grep wget
```
---

## Installer un paquet **firefox** téléchargé dans `/home/bob`  
```bash
    $ sudo rpm -ivh /home/bob/firefox-68.6.0-1.el7.centos.x86_64.rpm
```
---

## Installer un paquet **firefox** avec ses dépendances via YUM
```bash
    $ sudo yum install firefox -y
```
---

## Vérifier combien de dépôts logiciels sont configurés pour YUM
```bash
    $ sudo yum repolist
```
---

## Vérifier quel paquet fournit la commande **tcpdump**
```bash
    $ sudo yum provides tcpdump
```