# Challenge 07 : Install a Package

**Date** : 9 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Installer package `git` sur tous les app servers via gestionnaire packages yum.

---

## 📋 Énoncé

Selon nouvelles exigences applicatives partagées par équipe développement projet Nautilus, plusieurs nouveaux packages doivent être installés sur tous les app servers du Stratos Datacenter. La plupart sont complétés sauf `git`.

**Tâche** : Installer package `git` sur tous les app servers.

**Serveurs cibles** :
- `tony@stapp01` (App Server 1)
- `steve@stapp02` (App Server 2)
- `banner@stapp03` (App Server 3)

---

## ✅ Résolution

### App Server 1

```bash
ssh tony@stapp01
sudo yum install git -y
git --version
```

**Sortie attendue** :
```
git version 2.x.x
```

### App Server 2

```bash
ssh steve@stapp02
sudo yum install git -y
git --version
```

### App Server 3

```bash
ssh banner@stapp03
sudo yum install git -y
git --version
```

**Explication commandes** :
- `yum install git` : Installe package git depuis repos configurés
- `-y` : Assume "yes" à toutes les prompts (non-interactif)
- `git --version` : Vérifier installation réussie

---

## 💡 Notes

- **yum** : Package manager RedHat/CentOS (remplacé par `dnf` sur RHEL 8+)
- **-y flag** : Automation installations (scripts, CI/CD)
- **Vérification version** : Confirme package installé et accessible PATH

---

## 🏷️ Tags

`#Linux` `#yum` `#PackageManagement` `#git` `#Installation` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
