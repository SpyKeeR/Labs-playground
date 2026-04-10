# Challenge 08 : Install Ansible

**Date** : 9 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Installer Ansible version spécifique via pip3 avec disponibilité globale pour tous les utilisateurs.

---

## 📋 Énoncé

Lors de la réunion hebdomadaire, l'équipe DevOps Nautilus a discuté des solutions d'automation et configuration management à implémenter. Après avoir considéré plusieurs options, l'équipe a décidé d'utiliser Ansible pour sa simplicité de setup et prérequis minimaux. L'équipe veut commencer tests avec Ansible, donc décision d'utiliser jump host comme Ansible controller pour tester différentes tâches sur autres serveurs.

**Tâche** : Installer Ansible version `4.9.0` sur Jump host en utilisant `pip3` uniquement. S'assurer que binaire Ansible est disponible globalement (tous les utilisateurs peuvent exécuter commandes Ansible).

---

## ✅ Résolution

### 1. Installer Ansible version spécifique

```bash
sudo python3 -m pip install ansible==4.9.0
```

**Explication** :
- `sudo` : Installation système (global)
- `python3 -m pip` : Appelle module pip de Python 3
- `install ansible==4.9.0` : Version spécifique (important pour compatibilité)

### 2. Vérifier installation

```bash
ansible --version
```

**Sortie attendue** :
```
ansible [core 2.x.x]
  config file = None
  configured module search path = ...
  ansible python module location = /usr/local/lib/python3.x/site-packages/ansible
  ansible collection location = ...
  executable location = /usr/local/bin/ansible
  python version = 3.x.x
```

### 3. Installer argcomplete (autocomplétion)

```bash
sudo python3 -m pip install argcomplete
```

**Explication** : Argcomplete permet autocomplétion commandes Ansible (Tab completion).

### 4. Activer argcomplete globalement

```bash
sudo /usr/local/bin/activate-global-python-argcomplete
```

**Explication** : Configure autocomplétion Ansible pour tous les utilisateurs système.

### 5. Recharger profil shell

```bash
source ~/.bash_profile
```

**Explication** : Applique changements sans déconnexion/reconnexion.

---

## 💡 Notes

- **pip vs pip3** : pip3 explicite version Python 3 (évite confusion pip Python 2)
- **python3 -m pip** : Méthode recommandée (garantit bon pip pour version Python)
- **ansible==4.9.0** : Version spécifique (= requis, pas >=)
- **Installation globale** : `sudo` rend disponible tous utilisateurs (`/usr/local/bin/`)

---

## 🏷️ Tags

`#Linux` `#Ansible` `#pip` `#Python` `#DevOps` `#Automation` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
