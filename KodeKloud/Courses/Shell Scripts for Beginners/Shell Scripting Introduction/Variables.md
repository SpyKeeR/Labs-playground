# Lab - Variables

## Exercice 1

	```
	mission_name=lunar-mission

	mkdir $mission_name

	rocket-add $mission_name

	rocket-start-power $mission_name
	rocket-internal-power $mission_name
	rocket-start-sequence $mission_name
	rocket-start-engine $mission_name
	rocket-lift-off $mission_name

	rocket-status $mission_name
	$ bash create-and-launch-rocket
	```

## Exercice 2

	```
	user_name=Michael
	echo "Salut $user_name, bienvenue chez xFusionCorp Industries. Nous et le reste de la direction sommes ravis de t’accueillir à bord."
	```
	
## Exercice 3

	```
	uptime=$(uptime)
	echo "Le temps de fonctionnement du système est : $uptime"
	```

## Exercice 4

	```
	file_name="create-and-launch-rocket"
	cp $file_name ${file_name}_bkp
	```

## Exercice 5

	```
	FILE01="Japan"
	FILE02="South Korea"
	FILE03="Canada"
	cd /home/bob
	echo "Création du fichier appelé $FILE01"
	touch $FILE01
	echo "Création du fichier appelé $FILE02"
	touch $FILE02
	echo "Création du fichier appelé $FILE03"
	touch $FILE03
	```