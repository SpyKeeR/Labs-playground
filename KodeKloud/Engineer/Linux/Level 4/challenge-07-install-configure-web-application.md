# Challenge 07 - Install and Configure Web Application

**Difficulté** : Level 4  
**Domaine** : Apache, Virtual Directories, Multi-Sites  
**Date** : 20 janvier 2026

---

## 📋 Consigne

xFusionCorp Industries prévoit d'héberger deux sites web statiques sur leur infrastructure dans le Stratos Datacenter. Le développement de ces sites web est encore en cours, mais nous voulons préparer les serveurs. Veuillez effectuer les étapes suivantes pour accomplir la tâche :

a. Installer le package httpd et ses dépendances sur le serveur d'application 2.

b. Apache doit servir sur le port 6200.

c. Il y a deux sauvegardes de sites web `/home/thor/news` et `/home/thor/cluster` sur jump_host. Configurez-les sur Apache de manière à ce que news fonctionne sur le lien `http://localhost:6200/news/` et cluster fonctionne sur le lien `http://localhost:6200/cluster/` sur le serveur d'application mentionné.

d. Une fois configuré, vous devriez pouvoir accéder au site web en utilisant la commande curl sur le serveur d'application respectif, c'est-à-dire `curl http://localhost:6200/news/` et `curl http://localhost:6200/cluster/`

---

## 🔧 Réalisation

### Étape 1 : Transfert fichiers depuis Jump Host

```bash
scp /home/thor/* steve@stapp02:/home/steve/
# Password: Am3ric@
```

**Explication** : Copie répertoires `news` et `cluster` vers app server

### Étape 2 : Connexion App Server 2

```bash
ssh steve@stapp02
# Password: Am3ric@
```

### Étape 3 : Installation Apache

```bash
sudo yum install httpd -y
```

### Étape 4 : Déplacement sites web

```bash
sudo mv /home/steve/news /var/www/html/
sudo mv /home/steve/cluster /var/www/html/
```

**Vérification** :
```bash
ls -l /var/www/html/
# drwxr-xr-x news
# drwxr-xr-x cluster
```

### Étape 5 : Permissions

```bash
sudo chown -R :apache /var/www/html
```

**Explication** : Groupe `apache` propriétaire (lecture fichiers)

### Étape 6 : Configuration port Apache

```bash
sudo vi /etc/httpd/conf/httpd.conf
```

**Modifier directive Listen** :
```apache
# Avant
Listen 80

# Après
Listen 6200
```

### Étape 7 : Activation Apache

```bash
sudo systemctl enable --now httpd
```

### Étape 8 : Vérification

```bash
curl http://localhost:6200/news/
# Affiche contenu site news ✅

curl http://localhost:6200/cluster/
# Affiche contenu site cluster ✅
```


## 🔗 Ressources

- [Apache DocumentRoot](https://httpd.apache.org/docs/2.4/mod/core.html#documentroot)
- [Apache Alias Directive](https://httpd.apache.org/docs/2.4/mod/mod_alias.html#alias)
