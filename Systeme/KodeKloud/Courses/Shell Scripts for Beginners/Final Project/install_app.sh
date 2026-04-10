#!/bin/bash

# Fonction pour afficher du texte coloré
function print_color(){
  NC='\033[0m'  # Réinitialisation de la couleur
  case $1 in
    "green") COLOR='\033[0;32m' ;;  # Vert
    "red") COLOR='\033[0;31m' ;;    # Rouge
    "*") COLOR='\033[0m' ;;         # Couleur par défaut
  esac

  echo -e "${COLOR} $2 ${NC}"
}

# Vérifie si un service est actif
function check_service_status(){
  service_is_active=$(sudo systemctl is-active $1)

  if [ $service_is_active = "active" ]; then
    echo "$1 est actif et fonctionne"
  else
    echo "$1 n'est pas actif/fonctionnel"
    exit 1
  fi
}

# Vérifie si un port est configuré dans FirewallD
function is_firewalld_rule_configured(){
  firewalld_ports=$(sudo firewall-cmd --list-all --zone=public | grep ports)

  if [[ $firewalld_ports == *$1* ]]; then
    echo "FirewallD a le port $1 configuré"
  else
    echo "FirewallD : le port $1 n'est pas configuré"
    exit 1
  fi
}

# Vérifie si un élément est présent sur une page web
function check_item(){
  if [[ $1 = *$2* ]]; then
    print_color "green" "L'élément $2 est présent sur la page web"
  else
    print_color "red" "L'élément $2 n'est pas présent sur la page web"
  fi
}

echo "---------------- Configuration du serveur de base de données ------------------"

# Installation et démarrage de FirewallD
print_color "green" "Installation de FirewallD..."
sudo yum install -y firewalld
sudo service firewalld start
sudo systemctl enable firewalld
check_service_status firewalld

# Installation et démarrage de MariaDB
print_color "green" "Installation de MariaDB..."
sudo yum install -y mariadb-server
print_color "green" "Démarrage de MariaDB..."
sudo service mariadb start
sudo systemctl enable mariadb
check_service_status mariadb

# Configuration du Firewall pour le port de la base de données
print_color "green" "Configuration des règles FirewallD pour la base de données..."
sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
sudo firewall-cmd --reload
is_firewalld_rule_configured 3306

# Configuration de la base de données
print_color "green" "Configuration de la base de données..."
cat > setup-db.sql <<-EOF
CREATE DATABASE ecomdb;
CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'ecompassword';
GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'localhost';
FLUSH PRIVILEGES;
EOF
sudo mysql < setup-db.sql

# Chargement des données d'inventaire
print_color "green" "Chargement des données d'inventaire dans la base de données..."
cat > db-load-script.sql <<-EOF
USE ecomdb;
CREATE TABLE products (
  id mediumint(8) unsigned NOT NULL auto_increment,
  Name varchar(255) default NULL,
  Price varchar(255) default NULL,
  ImageUrl varchar(255) default NULL,
  PRIMARY KEY (id)
) AUTO_INCREMENT=1;

INSERT INTO products (Name,Price,ImageUrl) VALUES
("Laptop","100","c-1.png"),
("Drone","200","c-2.png"),
("VR","300","c-3.png"),
("Tablet","50","c-5.png"),
("Watch","90","c-6.png"),
("Phone Covers","20","c-7.png"),
("Phone","80","c-8.png"),
("Laptop","150","c-4.png");
EOF
sudo mysql < db-load-script.sql

# Vérification que les données ont bien été chargées
mysql_db_results=$(sudo mysql -e "use ecomdb; select * from products;")
if [[ $mysql_db_results == *Laptop* ]]; then
  print_color "green" "Les données d'inventaire ont été chargées dans MySQL"
else
  print_color "red" "Les données d'inventaire n'ont pas été chargées dans MySQL"
  exit 1
fi

print_color "green" "---------------- Configuration du serveur de base de données terminée ------------------"

# Configuration du serveur web
print_color "green" "---------------- Configuration du serveur web ------------------"
print_color "green" "Installation des packages du serveur web..."
sudo yum install -y httpd php php-mysql

print_color "green" "Configuration des règles FirewallD..."
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --reload
is_firewalld_rule_configured 80

# Remplace index.html par index.php dans la config Apache
sudo sed -i 's/index.html/index.php/g' /etc/httpd/conf/httpd.conf

print_color "green" "Démarrage du service httpd..."
sudo service httpd start
sudo systemctl enable httpd
check_service_status httpd

# Installation de GIT et récupération du projet web
print_color "green" "Installation de GIT..."
sudo yum install -y git
sudo git clone https://github.com/kodekloudhub/learning-app-ecommerce.git /var/www/html/

print_color "green" "Mise à jour du fichier index.php..."
sudo sed -i 's/172.20.1.101/localhost/g' /var/www/html/index.php

print_color "green" "---------------- Configuration du serveur web terminée ------------------"

# Vérification du contenu de la page web
web_page=$(curl http://localhost)
