# Labo - Working with Shell

- Accéder aux labs pratiques : [Labo](https://kodekloud.com/free-labs/linux/working-with-the-shell)

---

## 1. Vérifier le répertoire personnel d’un utilisateur (exemple : **bob**)  
```bash
    $ grep bob /etc/passwd | cut -d ":" -f6
```
---

## 2. Vérifier le répertoire personnel via une variable intégrée du shell  
```bash
    $ echo $HOME
```
---

## 3. Dans la commande `echo Welcome`, que représente le mot **Welcome** ?  
    → "Welcome" est un argument
---

## 4. Vérifier le type de la commande **git**  
```bash
    $ type git
```
---

## 5. Créer un répertoire  
```bash
    $ mkdir /home/bob/birds
```
---

## 6. Créer des répertoires récursivement  
```bash
    $ mkdir -p /home/bob/fish/salmon
```
---

## 7. Créer plusieurs répertoires  
```bash
    $ mkdir -p /home/bob/{mammals/{elephant,monkey},birds/eagle,reptile/{snake,frog},amphibian/salamander}
```
---

## 8. Déplacer un répertoire  
```bash
    $ mv /home/bob/reptile/frog /home/bob/amphibian
```
---

## 9. Renommer un répertoire  
```bash
    $ mv /home/bob/reptile/snake /home/bob/reptile/crocodile
```
---

## 10. Supprimer un répertoire  
```bash
    $ rm -r /home/bob/reptile
```