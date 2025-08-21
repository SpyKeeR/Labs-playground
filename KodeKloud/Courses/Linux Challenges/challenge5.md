# Linux Challenge 5

- Accéder aux labs pratiques : [Linux Challenges](https://learn.kodekloud.com/user/courses/linux-challenges)

## Résolution de nom locale

```bash
vi /etc/hosts
```

```text
10.0.0.50    mydb.kodekloud.com
```

## Ajouter une IP supplémentaire à l’interface eth1

```bash
ip address add 10.0.0.50/24 dev eth1
```

### Installer MariaDB et activer le service

```bash
yum install mariadb-server -y
systemctl enable --now mariadb
```

## Sécuriser le root MySQL

```bash
mysqladmin -u root password 'sd6857f7s8d8'
```

## Débloquer le compte root et ajouter au groupe wheel

```bash
usermod -U -aG wheel root
```

## Docker

```bash
docker pull nginx
docker run -d -p 80:80 --name myapp nginx
```

## Scripts pour gérer le conteneur

### Script de démarrage

```bash
vi /home/bob/container-start.sh
```

```text
#!/bin/bash

docker start myapp
echo "myapp container started!"
```

```bash
chmod +x /home/bob/container-start.sh
```

### Script d'arrêt

```bash
vi /home/bob/container-stop.sh
```

```text
#!/bin/bash

docker stop myapp
echo "myapp container stopped!"
```

```bash
chmod +x /home/bob/container-stop.sh
```

## Cron jobs pour démarrage/arrêt automatique

```bash
crontab -e
```

```text
0 0 * * * /home/bob/container-stop.sh
0 8 * * * /home/bob/container-start.sh
```

## PAM – restreindre su au groupe wheel sans mot de passe

```bash
vi /etc/pam.d/su
```

Décommenter les deux lignes commençant par #auth qui concernent le groupe wheel