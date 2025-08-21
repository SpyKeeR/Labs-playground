# Labo - DPKG & APT

- Accéder aux labs pratiques : [Labo](https://kodekloud.com/free-labs/linux/dpkg-and-apt)

---

## Quel gestionnaire de paquets est utilisé sur une distribution basée sur Debian ?
Les distributions Debian utilisent :  dpkg

---

## Installer un paquet **firefox** téléchargé dans `/root/firefox.deb`  
```bash
    $ sudo dpkg -i /root/firefox.deb
```
---

## Installer un paquet avec **APT**
```bash
    $ sudo apt install firefox
```
---

## Rechercher le paquet pour installer le navigateur **Chromium**  
(Utiliser `apt search` pour trouver le nom exact du paquet. Description : *Chromium web browser, open-source version of Chrome*)
```bash
    $ sudo apt search chromium-browser
```
---

## Installer le navigateur **chromium-browser**
```bash
    $ sudo apt install -y chromium-browser
```
---

## Supprimer le navigateur **firefox**
```bash
    $ sudo apt remove firefox
```