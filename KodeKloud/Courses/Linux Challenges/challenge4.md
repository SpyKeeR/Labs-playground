# Linux Challenge 4

- Accéder aux labs pratiques : [Linux Challenges](https://learn.kodekloud.com/user/courses/linux-challenges)

## Trouver et copier les fichiers cachés

```bash
mkdir -p /opt/appdata/hidden
find /home/bob/preserved -type f -name ".*" -exec cp "{}" /opt/appdata/hidden/ \;
```

## Trouver et copier les fichiers non cachés

```bash
mkdir -p /opt/appdata/files
find /home/bob/preserved -type f -not -name ".*" -exec cp "{}" /opt/appdata/files/ \;
```

## Supprimer les fichiers contenant des mots se terminant par "t"

```bash
rm -f $(find /opt/appdata/ -type f -exec grep -l 't\>' "{}"  \; )
```

## Remplacer "yes" par "no"

```bash
find /opt/appdata -type f -name "*" -exec sed -i 's/\byes\b/no/g' "{}" \;
```

## Remplacer "raw" par "processed" (insensible à la casse)

```bash
find /opt/appdata -type f -name "*" -exec sed -i 's/\braw\b/processed/ig' "{}" \;
```

## Créer l’archive appdata.tar.gz

```bash
cd /opt
# /opt/appdata contains the final processed data
tar -zcf appdata.tar.gz appdata
```

## Configurer les permissions

```bash
chmod +t /opt/appdata
chown bob:bob /opt/appdata.tar.gz
chmod 440 /opt/appdata.tar.gz
```

### Créer un lien symbolique pour bob

```bash
ln -s /opt/appdata.tar.gz /home/bob/appdata.tar.gz
```

## Script filter.sh et fichier filtré filtered.txt

```bash
vi /home/bob/filter.sh
```

```text
#!/bin/bash
tar -xzOf /opt/appdata.tar.gz | grep processed > /home/bob/filtered.txt
```

```bash
chmod +x /home/bob/filter.sh
/home/bob/filter.sh
```