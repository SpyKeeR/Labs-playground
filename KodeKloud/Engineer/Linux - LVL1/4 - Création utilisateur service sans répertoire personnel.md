# Instructions

L’équipe d’administration système de **xFusionCorp Industries** a déployé un nouvel outil sur tous les serveurs App.  
Cet outil nécessite la création d’un **compte utilisateur service** dédié.  

**Tâche à réaliser :**  

- Créer un utilisateur nommé `anita` sur le **App Server 2** **sans répertoire personnel**.  

---

# Solution

1. **Se connecter au serveur App 2**  

```bash
ssh steve@172.16.238.11
```

2. **Créer l’utilisateur `anita` sans répertoire personnel**  

```bash
sudo useradd --no-create-home anita
```

- `--no-create-home` : empêche la création d’un répertoire personnel pour l’utilisateur.  
- Cette option est utile pour les comptes service qui n’ont pas besoin de répertoire personnel.  

3. **Vérifier que l’utilisateur a bien été créé**  

```bash
grep "anita:" /etc/passwd
```

4. **Supprimer l’utilisateur si nécessaire**  

```bash
sudo userdel --remove anita
```