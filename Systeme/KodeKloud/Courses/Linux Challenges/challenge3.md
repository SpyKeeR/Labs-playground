# Linux Challenge 3

- Accéder aux labs pratiques : [Linux Challenges](https://learn.kodekloud.com/user/courses/linux-challenges)

## Créer le groupe admins

```bash
groupadd admins
```

## Utilisateur david

```bash
useradd -s /bin/zsh david
passwd david
usermod -aG admins
```

## Utilisateur natasha

```bash
useradd -s /bin/zsh natasha
passwd natasha
usermod -aG admins
```

## Créer le groupe devs

```bash
groupadd devs
```

## Utilisateur ray

```bash
useradd -s /bin/sh ray
passwd ray
usermod -aG devs
```

### Utilisateur lisa

```bash
useradd -s /bin/sh lisa
passwd lisa
usermod -aG devs
```

## Propriétaire et permissions du répertoire /data

```bash
chown bob:devs /data
chmod 770 /data
setfacl -m g:admins:rwx /data
```

## Configuration sudo

```bash
visudo
```

```text
%admins ALL=(ALL) NOPASSWD:ALL
%devs ALL=(ALL) NOPASSWD:/usr/bin/dnf
```

## Limite de processus pour devs

```bash
vi /etc/security/limits.conf
```

```text
@devs            -       nproc           30
```

## Quota disque pour devs sur /data

```bash
setquota -g devs 100M 500M 0 0 /dev/vdb1
```