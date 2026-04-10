# Challenge 01 - Install and Configure Nginx as an LBR

**Difficulté** : Level 4  
**Domaine** : Nginx, Load Balancing, High Availability  
**Date** : 19 janvier 2026

---

## 📋 Consigne

Le trafic augmente jour après jour sur l'un des sites web gérés par l'équipe de support production Nautilus. Par conséquent, l'équipe a observé une dégradation des performances du site web. Suite à des discussions sur ce problème, l'équipe a décidé de déployer cette application sur une stack haute disponibilité, c'est-à-dire sur l'infrastructure Nautilus dans le Stratos DC. Ils ont commencé la migration le mois dernier et c'est presque terminé, seule la configuration du serveur LBR est en attente. Configurez le serveur LBR selon les informations données ci-dessous :

a. Installer nginx sur le serveur LBR (load balancer).

b. Configurer le load-balancing avec un contexte http utilisant tous les serveurs d'applications. Assurez-vous de mettre à jour uniquement le fichier de configuration principal de Nginx situé à `/etc/nginx/nginx.conf`.

c. Assurez-vous de ne pas mettre à jour le port apache déjà défini dans la configuration apache sur tous les serveurs d'applications, et assurez-vous également que le service apache est actif et en cours d'exécution sur tous les serveurs d'applications.

d. Une fois terminé, vous pouvez accéder au site web en utilisant le bouton StaticApp dans la barre supérieure.

---

## 🔧 Réalisation

### Étape 1 : Connexion serveur Load Balancer

```bash
ssh loki@stlb01
# Password: Mischi3f
```

### Étape 2 : Installation Nginx

```bash
sudo yum install nginx -y
```

### Étape 3 : Configuration Load Balancer

```bash
sudo vi /etc/nginx/nginx.conf
```

**Supprimer bloc `server {}` par défaut et remplacer par** :
```nginx
upstream app {
    server stapp01:5001;
    server stapp02:5001;
    server stapp03:5001;
}

server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://app;
    }
}
```

**Explication configuration** :
- `upstream app` : Définit pool de serveurs backend
- `server stappXX:5001` : Backend servers Apache (port 5001)
- `proxy_pass http://app` : Redirige requêtes vers pool upstream

### Étape 4 : Validation configuration

```bash
sudo nginx -t
# nginx: configuration file /etc/nginx/nginx.conf test is successful
```

**Explication** : Test syntaxe avant redémarrage (éviter downtime)

### Étape 5 : Activation Nginx

```bash
sudo systemctl enable --now nginx
```

### Étape 6 : Vérification

**Test local** :
```bash
curl localhost
# Affiche contenu application ✅
```

**Test via interface Lab** :
- Cliquer bouton **StaticApp** → Page application s'affiche

---

## 🔑 Apprentissages clés

**Nginx Load Balancing** :
- Directive `upstream` : Groupe serveurs backend
- Algorithme par défaut : **Round-robin** (distribution équitable)
- Alternatives : `least_conn`, `ip_hash`, `weighted`

**Reverse Proxy** :
- `proxy_pass` : Forward requêtes HTTP vers backend
- LBR = Point d'entrée unique, backends transparents clients

**High Availability** :
- Distribution charge sur plusieurs serveurs
- Tolérance pannes (un backend down, autres prennent relais)

---

## 🔗 Ressources

- [Nginx Load Balancing](https://nginx.org/en/docs/http/load_balancing.html)
- [Nginx Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
