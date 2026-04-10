# Challenge Linux 1

- Accéder aux labs pratiques : [Linux Challenges](https://learn.kodekloud.com/user/courses/linux-challenges)

---
## 1. Passer en root

```bash
sudo -i
```

## 2. Installer le package LVM

```bash
yum install -y lvm2
```

## 3. Créer le groupe dba_users et ajouter l’utilisateur bob

```bash
groupadd dba_users
usermod -G dba_users bob
```

## 4. Créer des volumes physiques (PVs)

```bash
pvcreate /dev/vdb
pvcreate /dev/vdc
```

## 5. Créer un groupe de volumes (VG) dba_storage

```bash
vgcreate dba_storage /dev/vdb /dev/vdc
```

## 6. Créer un volume logique (LV) volume_1 avec tout l’espace disponible

```bash
lvcreate -n volume_1 -l 100%FREE dba_storage
```

## 7. Formater et monter le volume

```bash
mkfs.xfs /dev/dba_storage/volume_1
mkdir -p /mnt/dba_storage
mount -t xfs /dev/dba_storage/volume_1 /mnt/dba_storage
```

## 8. Rendre le montage persistant

```bash
echo "/dev/mapper/dba_storage-volume_1 /mnt/dba_storage xfs defaults 0 0" >> /etc/fstab
```

## 9. Définir les permissions et la propriété du groupe

```bash
chown :dba_users /mnt/dba_storage
chmod 770 /mnt/dba_storage
```