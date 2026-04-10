# Challenge 03 - Install and Configure Tomcat Server

**Difficulté** : Level 3  
**Domaine** : Tomcat, Java Applications, WAR Deployment  
**Date** : 18 janvier 2026

---

## 📋 Consigne

L'équipe de développement d'applications Nautilus a récemment terminé la version bêta de l'une de leurs applications basées sur Java, qu'ils prévoient de déployer sur l'un des serveurs d'applications dans le Stratos DC. Après une réunion d'équipe interne, ils ont décidé d'utiliser le serveur d'application tomcat. En vous basant sur les exigences mentionnées ci-dessous, complétez la tâche :

a. Installer le serveur tomcat sur App Server 2.

b. Le configurer pour qu'il s'exécute sur le port 6200.

c. Il y a un fichier ROOT.war sur le Jump host à l'emplacement /tmp.

Déployez-le sur ce serveur tomcat et assurez-vous que la page web fonctionne directement sur l'URL de base, c'est-à-dire curl http://stapp02:6200


---

## 🔧 Réalisation

### Étape 1 : Transfert WAR file vers App Server 2

```bash
# Depuis Jump Host
sudo scp /tmp/ROOT.war steve@stapp02:/home/steve
# Password: Am3ric@ (user steve)
```

**Explication** :
- `scp` : Secure Copy via SSH (transfert fichiers encrypted)
- `/tmp/ROOT.war` : Source (Jump Host)
- `steve@stapp02:/home/steve` : Destination (App Server 2 home directory steve)

### Étape 2 : Connexion App Server 2

```bash
ssh steve@stapp02
# Password: Am3ric@
```

### Étape 3 : Installation Tomcat

```bash
sudo yum install tomcat -y
```

**Packages installés** :
- `tomcat` : Apache Tomcat server (core)
- Dependencies : Java JDK, servlet API, etc.

**Vérification installation** :
```bash
rpm -qa | grep tomcat
# tomcat-7.0.76-16.el7.noarch (version peut varier)

# Répertoires Tomcat
ls -l /usr/share/tomcat/
# bin/  conf/  lib/  logs/  temp/  webapps/  work/
```

### Étape 4 : Configuration port Tomcat

```bash
sudo vi /etc/tomcat/server.xml
```

**Rechercher ligne Connector** (environ ligne 69) :
```xml
<!-- Default Connector (commented) -->
<!--
<Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443" />
-->

<!-- Active Connector (décommenté par défaut) -->
<Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443" />
```

**Modifier port 8080 → 6200** :
```xml
<Connector port="6200" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443" />
```

**Sauvegarder** : `:wq`

### Étape 5 : Déploiement ROOT.war

```bash
sudo mv /home/steve/ROOT.war /var/lib/tomcat/webapps/
```

**Explication** :
- `/var/lib/tomcat/webapps/` : Répertoire déploiement applications Tomcat
- `ROOT.war` : Nom spécial = déploiement context path `/` (base URL)
- Tomcat auto-déploie fichiers `.war` au démarrage (explode archive)

**Vérification** :
```bash
ls -l /var/lib/tomcat/webapps/
# ROOT.war
```

### Étape 6 : Démarrage Tomcat

```bash
sudo systemctl enable --now tomcat
```

**Vérification service** :
```bash
sudo systemctl status tomcat
# Active (running)

# Logs Tomcat
sudo tail -f /var/log/tomcat/catalina.out
# Output attendu :
# INFO: Server startup in 1234 ms
```

**Vérification déploiement ROOT.war** :
```bash
ls -l /var/lib/tomcat/webapps/
# ROOT/       (directory - WAR extracted)
# ROOT.war    (original archive)
```

Tomcat décompresse `ROOT.war` → `ROOT/` directory automatiquement.

### Étape 7 : Validation application

```bash
# Test local App Server 2
curl stapp02:6200
# Output : Page HTML application Java

# Test localhost
curl localhost:6200
# Output : Page HTML (identique)
```

**Test depuis Jump Host** :
```bash
curl http://stapp02:6200
# Output : Page HTML application ✅
```

---

## 🔗 Ressources

**Documentation Tomcat** :
- [Apache Tomcat 9 Documentation](https://tomcat.apache.org/tomcat-9.0-doc/)
- [Tomcat Configuration Reference](https://tomcat.apache.org/tomcat-9.0-doc/config/)
- [Deployer Documentation](https://tomcat.apache.org/tomcat-9.0-doc/deployer-howto.html)

**Java Web Applications** :
- [Servlet Specification](https://jakarta.ee/specifications/servlet/)
- [JSP Tutorial](https://www.oracle.com/java/technologies/jspt.html)