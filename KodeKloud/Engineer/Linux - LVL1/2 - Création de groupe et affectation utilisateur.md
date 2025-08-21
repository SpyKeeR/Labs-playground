# Instructions

L’équipe d’administration système de **xFusionCorp Industries** a défini des niveaux d’accès spécifiques pour les utilisateurs.  
Au lieu d’attribuer des droits individuellement à chaque utilisateur, l’équipe a décidé de créer des groupes correspondant aux différents niveaux d’accès, puis d’ajouter les utilisateurs à ces groupes selon les besoins.  

**Tâches à réaliser :**  

1. Créer un groupe nommé `nautilus_developers` sur tous les serveurs App du datacenter Stratos.  
2. Ajouter l’utilisateur `mohammed` au groupe `nautilus_developers` sur tous les serveurs App (créer l’utilisateur si nécessaire).  

---

# Solution

1. **Se connecter à chaque serveur App**  

```bash
ssh tony@172.16.238.10   # App Server 1
ssh steve@172.16.238.11   # App Server 2
ssh banner@172.16.238.12  # App Server 3
```

2. **Lister les groupes existants (facultatif)**  

```bash
cat /etc/group
```

3. **Créer le groupe `nautilus_developers`**  

```bash
sudo groupadd nautilus_developers
```

4. **Vérifier la création du groupe**  

```bash
grep -E "^nautilus_developers:" /etc/group
```

5. **Lister les utilisateurs existants (facultatif)**  

```bash
cat /etc/passwd
```

6. **Créer l’utilisateur `mohammed` si nécessaire**  

```bash
sudo useradd mohammed
```

7. **Vérifier que l’utilisateur existe**  

```bash
grep -E "^mohammed:" /etc/passwd
```

Cette commande recherche une ligne qui commence par `mohammed:` dans le fichier `/etc/passwd` et affiche les informations de l’utilisateur (nom, UID, répertoire personnel, shell).

8. **Ajouter l’utilisateur `mohammed` au groupe `nautilus_developers`**  

```bash
sudo usermod -aG nautilus_developers mohammed
```

- `-a` : append / ajouter sans retirer l’utilisateur de ses groupes actuels.  
- `-G` : spécifie le ou les groupes auxquels ajouter l’utilisateur.  

Après cette commande, `mohammed` sera membre du groupe `nautilus_developers` tout en conservant ses autres appartenances à des groupes.