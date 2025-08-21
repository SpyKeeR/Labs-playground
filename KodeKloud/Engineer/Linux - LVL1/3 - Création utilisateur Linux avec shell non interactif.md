# Instructions

L’équipe d’administration système de **xFusionCorp Industries** a installé un outil d’agent de sauvegarde sur tous les serveurs App.  
Selon les exigences de cet outil, il est nécessaire de créer un utilisateur avec un **shell non-interactif**.  

**Tâche à réaliser :**  

- Créer un utilisateur nommé `mariyam` avec un shell non-interactif sur le **App Server 1**.  

---

# Solution

1. **Se connecter au serveur App 1**  

```bash
ssh tony@172.16.238.10
```

2. **Créer l’utilisateur `mariyam` avec un shell non-interactif**  

```bash
sudo useradd --shell /bin/false mariyam
```

- `--shell /bin/false` : définit le shell de l’utilisateur à `/bin/false`, ce qui empêche toute connexion interactive.  
- Ce type de compte est généralement utilisé pour les comptes système ou pour des utilisateurs qui n’ont pas besoin d’accéder directement au serveur.  

3. **Vérifier que l’utilisateur a bien été créé**  

```bash
id mariyam
```

Cette commande affiche les informations de l’utilisateur `mariyam` : UID (identifiant utilisateur), GID (identifiant du groupe), et les groupes auxquels il appartient.  
Si l’utilisateur a été créé correctement, la sortie sera similaire à :  

```
uid=1001(mariyam) gid=1001(mariyam) groups=1001(mariyam)
```