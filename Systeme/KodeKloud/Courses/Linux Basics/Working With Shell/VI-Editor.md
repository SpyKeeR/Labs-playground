# Labo - VI Editor

- Accéder aux labs pratiques : [Labo](https://kodekloud.com/free-labs/linux/vi-editor)

---

## Passer en **mode insertion**

    Appuyer sur i

---

## Quitter le **mode insertion** et revenir en **mode commande**

    Appuyer sur ESC

---

## Supprimer un caractère

    Placer le curseur sur le caractère à supprimer et appuyer sur x

---

## Modifier le contenu du fichier en **Welcome to KodeKloud** puis sauvegarder

	1. Passer en mode insertion avec `i`  
	2. Supprimer tout le contenu et saisir :  
		```
		   Welcome to KodeKloud  
		```
	3. Appuyer sur `ESC` pour revenir en mode commande  
	4. Taper :  
		```
		   :w!
		```
---

## Modifier le port d’écoute d’Apache de **80** vers **5000**

	1. Passer en mode insertion avec `i`  
	2. Remplacer `80` par `5000` sur la ligne 10  

---

## Supprimer la ligne commençant par **LogFormat**

	1. Aller à la ligne 33  
	2. Taper :  
		```
		   dd
		```
---

## Annuler la dernière modification

    Appuyer sur u

---

## Trouver le caractère **6** dans le fichier
	Taper dans le mode de commande : 
	```
		/6
	```