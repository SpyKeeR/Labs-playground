# Lab Logique Conditionnelle

## Exercice 1

	```
	nom_mission=$1

	mkdir $nom_mission

	rocket-add $nom_mission

	rocket-start-power $nom_mission
	rocket-internal-power $nom_mission
	rocket-start-sequence $nom_mission
	rocket-start-engine $nom_mission
	rocket-lift-off $nom_mission

	statut_rocket=$(rocket-status $nom_mission)

	echo "Le statut du lancement est $statut_rocket"

	if [ $statut_rocket = "failed" ]
	then
	  rocket-debug $nom_mission
	fi
	```

## Exercice 2
 
	```
	if [ -d "/home/bob/caleston" ]
	then
	  echo "Le répertoire existe"
	else
	  echo "Répertoire non trouvé"
	fi
	```

## Exercice 3

	```
	if [ $1 -gt $2 ]
	then
		echo $1
	else
		echo $2
	fi
	```

## Exercice 4

	```
	numero_mois=$1

	if [ -z $numero_mois ]
	then
	  echo "Aucun numéro de mois renseigné. Veuillez entrer un numéro de mois en argument."
	  echo "ex: ./print-month-number 5"
	  exit
	fi

	if [[ $numero_mois -lt 1 && $numero_mois -gt 12 ]]
	then
	  echo "Numéro de mois invalide. Veuillez entrer un nombre valide entre 1 et 12."
	  exit
	fi

	if [ $numero_mois -eq 1 ]
	then
	  echo "Janvier"
	elif [ $numero_mois -eq 2 ]
	then
	  echo "Février"
	elif [ $numero_mois -eq 3 ]
	then
	  echo "Mars"
	elif [ $numero_mois -eq 4 ]
	then
	  echo "Avril"
	elif [ $numero_mois -eq 5 ]
	then
	  echo "Mai"
	elif [ $numero_mois -eq 6 ]
	then
	  echo "Juin"
	elif [ $numero_mois -eq 7 ]
	then
	  echo "Juillet"
	elif [ $numero_mois -eq 8 ]
	then
	  echo "Août"
	elif [ $numero_mois -eq 9 ]
	then
	  echo "Septembre"
	elif [ $numero_mois -eq 10 ]
	then
	  echo "Octobre"
	elif [ $numero_mois -eq 11 ]
	then
	  echo "Novembre"
	elif [ $numero_mois -eq 12 ]
	then
	  echo "Décembre"
	fi
	```