# Challenge 02 - Install and Configure SFTP

**Difficulté** : Level 3  
**Domaine** : SFTP, SSH, Security, User Management  
**Date** : 17 janvier 2026

---

## 📋 Consigne

Certains développeurs de l'équipe du projet Nautilus ont demandé un accès SFTP à au moins l'un des serveurs d'application dans le Stratos DC. Après avoir examiné les exigences, l'équipe des administrateurs système a décidé de configurer le serveur SFTP sur le serveur App Server 2 dans le Stratos Datacenter. Veuillez le configurer selon les instructions suivantes :

a. Créer un utilisateur SFTP yousuf et définir son mot de passe à ksH85UJjhb. Il existe déjà un groupe appelé ftp, vous pouvez utiliser le même.

b. L'authentification par mot de passe doit être activée pour cet utilisateur.

c. L'utilisateur SFTP ne doit être autorisé qu'à effectuer des connexions SFTP.


---

## 🔧 Réalisation

### Étape 1 : Connexion App Server 2

```bash
ssh steve@stapp02
# Password: Am3ric@ (user steve)
```

### Étape 2 : Configuration SSH daemon (sshd_config)

```bash
# Éditer configuration SSH server
sudo vi /etc/ssh/sshd_config
```

**Modifications `/etc/ssh/sshd_config`** :

Rechercher section `Subsystem` (fin fichier) et remplacer par :

```bash
# override default of no subsystems
#Subsystem      sftp    /usr/libexec/openssh/sftp-server
Subsystem       sftp    internal-sftp

# Example of overriding settings on a per-user basis
Match Group ftp
        X11Forwarding no
        AllowTcpForwarding no
        PermitTTY no
        GatewayPorts no
        ForceCommand internal-sftp
        PasswordAuthentication yes
```

**Explications configuration** :

**Subsystem sftp** :
- `#Subsystem sftp /usr/libexec/openssh/sftp-server` : Ancien sftp-server externe (commenté)
- `Subsystem sftp internal-sftp` : Nouveau sftp-server builtin SSH (moderne, sécurisé)

**Match Group ftp** :
- Applique directives suivantes UNIQUEMENT aux users du groupe `ftp`
- Users autres groupes = configuration SSH normale (pas restrictions)

**Restrictions sécurité** :
- `X11Forwarding no` : Bloque X11 GUI forwarding (pas interface graphique)
- `AllowTcpForwarding no` : Bloque TCP port forwarding (pas tunnels SSH)
- `PermitTTY no` : Bloque allocation TTY (pas shell interactif)
- `GatewayPorts no` : Bloque gateway ports (sécurité réseau)
- `ForceCommand internal-sftp` : FORCE commande internal-sftp (ignore commandes user, SFTP-only)
- `PasswordAuthentication yes` : Active authentification password (requirement challenge)

### Étape 3 : Création user SFTP

```bash
# Créer user yousuf
sudo useradd -G ftp -s /usr/sbin/nologin -m yousuf

# Options :
# -G ftp          : Ajouter user au groupe 'ftp' (Match Group trigger)
# -s /usr/sbin/nologin : Shell nologin (empêche login interactif)
# -m              : Créer home directory /home/yousuf
```

**Vérification user** :
```bash
id yousuf
# Output : uid=1003(yousuf) gid=1003(yousuf) groups=1003(yousuf),50(ftp)
# Groupe ftp (gid=50) présent ✅
```

### Étape 4 : Configuration password user

```bash
sudo passwd yousuf
# Enter new password: ksH85UJjhb
# Retype password: ksH85UJjhb
# passwd: all authentication tokens updated successfully
```

### Étape 5 : Redémarrage SSH daemon

```bash
sudo systemctl restart sshd
sudo systemctl status sshd
# Status : Active (running)
```

**Vérification** :
- No errors journalctl : `sudo journalctl -u sshd -n 20`
- SSHD listening : `sudo ss -tulnp | grep :22`

### Étape 6 : Validation SFTP access

**Test connexion SFTP** :
```bash
# Depuis Jump Host ou machine locale
sftp yousuf@stapp02
# Password: ksH85UJjhb

# Output attendu :
# Connected to stapp02.
# sftp>
```

**Test commandes SFTP** :
```bash
sftp> pwd
# Remote working directory: /home/yousuf

sftp> ls
# (Liste fichiers home directory)

sftp> put test.txt
# Uploading test.txt to /home/yousuf/test.txt

sftp> get test.txt
# Fetching /home/yousuf/test.txt

sftp> exit
# Bye
```

**Test restriction shell SSH (doit échouer)** :
```bash
# Essayer connexion SSH normale (doit être bloquée)
ssh yousuf@stapp02
# Output attendu :
# This service allows sftp connections only.
# Connection to stapp02 closed.
```

✅ User `yousuf` peut SFTP, mais PAS SSH shell (restriction OK)

---

## 🔗 Ressources

**Documentation OpenSSH** :
- [OpenSSH sshd_config Manual](https://man.openbsd.org/sshd_config)
- [SFTP Subsystem](https://man.openbsd.org/sftp-server)
- [Match Directive](https://man.openbsd.org/sshd_config#Match)

**Security guides** :
- [SSH Hardening Guide](https://www.ssh.com/academy/ssh/sshd_config)
- [SFTP Chroot Tutorial](https://www.digitalocean.com/community/tutorials/how-to-enable-sftp-without-shell-access-on-centos-7)

