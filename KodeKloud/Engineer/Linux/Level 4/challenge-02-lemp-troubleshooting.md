# Challenge 02 - LEMP Troubleshooting

**Difficulté** : Level 4  
**Domaine** : Nginx, PHP-FPM, LEMP Stack, Troubleshooting  
**Date** : 19 janvier 2026

---

## 📋 Consigne

Nous avons une stack LEMP configurée sur les serveurs d'applications et de base de données dans le Stratos DC. Elle utilise Nginx + php-fpm, pour l'instant nous avons déployé une page PHP exemple sur ces applications. En raison d'une mauvaise configuration, la page PHP ne se charge pas sur le serveur web. Il semble qu'au moins deux serveurs d'applications aient des problèmes. Trouvez plus de détails ci-dessous et assurez-vous que le site web fonctionne sur l'URL LBR et localement sur chaque application également.

1. Nginx est censé s'exécuter sur le port 80 sur tous les serveurs d'applications.

2. Le document root de Nginx est `/var/www/html/`

3. Testez la page web sur l'URL LBR (utilisez le bouton LBR dans la barre supérieure) et localement sur chaque serveur d'applications pour vous assurer qu'elle fonctionne. Elle ne doit afficher aucun message d'erreur ou page par défaut nginx.

---

## 🔧 Réalisation

### Étape 1 : Troubleshooting App Server 1

```bash
ssh tony@stapp01
# Password: Ir0nM@n
```

**Problème identifié** : Port incorrect

```bash
sudo vi /etc/nginx/nginx.conf
```

**Correction 1 : Port** :
```nginx
# Avant
listen 8084;

# Après
listen 80;
```

**Correction 2 : Index PHP** :
```nginx
# Avant
index index.html index.htm;

# Après
index index.php index.html index.htm;
```

**Explication** : Nginx doit traiter `index.php` en priorité pour applications PHP

**Redémarrage** :
```bash
sudo systemctl restart nginx
```

**Vérification** :
```bash
curl localhost
# Affiche page PHP ✅
```

---

### Étape 2 : Troubleshooting App Server 2

```bash
ssh steve@stapp02
# Password: Am3ric@
```

**Problème identifié** : Socket PHP-FPM incorrect

```bash
sudo vi /etc/nginx/nginx.conf
```

**Correction socket PHP-FPM** :
```nginx
# Avant
fastcgi_pass unix:/var/opt/remi/php74/run/php-fpm/www;

# Après
fastcgi_pass unix:/var/opt/remi/php74/run/php-fpm/www.sock;
```

**Explication** : Extension `.sock` manquante, Nginx ne peut communiquer avec PHP-FPM

**Redémarrage** :
```bash
sudo systemctl restart nginx
```

**Vérification** :
```bash
curl localhost
# Affiche page PHP ✅
```

---

### Étape 3 : Troubleshooting App Server 3

```bash
ssh banner@stapp03
# Password: BigGr33n
```

**Problème identifié** : Document root incorrect

```bash
sudo vi /etc/nginx/nginx.conf
```

**Correction root** :
```nginx
# Avant
root /var/www/html-data/;

# Après
root /var/www/html/;
```

**Explication** : Document root ne correspond pas au répertoire application

**Redémarrage** :
```bash
sudo systemctl restart nginx
```

**Vérification** :
```bash
curl localhost
# Affiche page PHP ✅
```

---

### Étape 4 : Vérification globale

**Test Load Balancer** :
```bash
curl stlb01
# Affiche page PHP (round-robin sur 3 backends) ✅
```

**Test via interface Lab** :
- Cliquer bouton **LBR** → Page PHP s'affiche sans erreur


## 🔗 Ressources

- [Nginx + PHP-FPM Configuration](https://www.nginx.com/resources/wiki/start/topics/examples/phpfcgi/)
- [PHP-FPM Documentation](https://www.php.net/manual/en/install.fpm.php)
