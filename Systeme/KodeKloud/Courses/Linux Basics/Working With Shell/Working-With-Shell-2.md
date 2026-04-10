# Labo - Working with Shell part 2

- Accéder aux labs pratiques : [Labo](https://kodekloud.com/free-labs/linux/working-with-shell-ii)

---

## Créer une archive tar du répertoire **python** et la compresser avec **gzip**  
Le fichier compressé doit être disponible à **/home/bob/python.tar.gz**
```bash
    $ tar -cf /home/bob/python.tar /home/bob/reptile/snake/python
    $ gzip /home/bob/python.tar
```
---

## Extraire un fichier compressé **eaglet.dat.gz** dans le même répertoire  
```bash
    $ gunzip /home/bob/birds/eagle/eaglet.dat.gz
```
---

## Trouver l’emplacement du fichier **caleston-code**  
```bash
    $ sudo find / -name caleston-code
```
---

## Trouver le fichier **dummy.service** et enregistrer son chemin absolu  
Le résultat doit être redirigé dans **/home/bob/dummy-service**
```bash
    $ sudo find / -name dummy.service
    $ echo /etc/systemd/system/dummy.service > /home/bob/dummy-service
```
---

## Rechercher un fichier dans **/etc** contenant la chaîne **172.16.238.197**  
Sauvegarder le chemin trouvé dans **/home/bob/ip**
```bash
    $ sudo grep -ir 172.16.238.197 /etc/ > /home/bob/ip
```
---

## Créer un fichier **/home/bob/file_wth_data.txt**  
Le fichier doit contenir une seule ligne : *a file in my home directory*
```bash
    $ echo "a file in my home directory" > /home/bob/file_wth_data.txt
```
---

## Exécuter le script Python et rediriger les erreurs dans un fichier  
Exécuter **/home/bob/my_python_test.py** et rediriger la sortie d’erreur standard vers **/home/bob/py_error.txt**
```bash
    $ python3 /home/bob/my_python_test.py 2>/home/bob/py_error.txt
```
---

## Lire un fichier compressé sans l’extraire et en sauvegarder la première ligne  
Lire **/usr/share/man/man1/tail.1.gz** et copier la première ligne dans **/home/bob/pipes**
```bash
    $ zcat /usr/share/man/man1/tail.1.gz | head -1 > /home/bob/pipes
```