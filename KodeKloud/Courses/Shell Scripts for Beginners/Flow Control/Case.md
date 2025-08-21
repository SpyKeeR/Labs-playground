# Labs Case

## Exercice 1

Le script est manquant du mot-clé in à la ligne 4. Les lignes 7 et 9 manquent de ;;. La ligne 13 manque de )

## Exercice 2

    ```
	numero_mois=$1

	# Vérifie si un numéro de mois a été fourni
	if [ -z $numero_mois ]
	then
	  echo "Aucun numéro renseigné, merci de respecter le format"
	  echo "ex: ./print-month-number 5"
	  exit
	fi

	# Vérifie si le numéro de mois est valide (entre 1 et 12)
	if [[ $numero_mois -lt 1 || $numero_mois -gt 12 ]]
	then
	  echo "Numéro de mois invalide. Merci de saisir un numéro entre 1 et 12."
	  exit
	fi

	# Affiche le nom du mois correspondant au numéro
	case $numero_mois in
	  1) echo "Janvier" ;;
	  2) echo "Février" ;;
	  3) echo "Mars" ;;
	  4) echo "Avril" ;;
	  5) echo "Mai" ;;
	  6) echo "Juin" ;;
	  7) echo "Juillet" ;;
	  8) echo "Août" ;;
	  9) echo "Septembre" ;;
	  10) echo "Octobre" ;;
	  11) echo "Novembre" ;;
	  12) echo "Décembre" ;;
	esac
	```
	 
## Exercice 3

	```
	while true
	do
	  echo "1. Ajouter"
	  echo "2. Soustraire"
	  echo "3. Multiplier"
	  echo "4. Diviser"
	  echo "5. Quitter"

	  read -p "Entrez votre choix : " choix

	  if [ $choix -eq 1 ]
	  then
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			echo "Résultat=$(( $nombre1 + $nombre2 ))"
	  elif [ $choix -eq 2 ]
	  then
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			echo "Résultat=$(( $nombre1 - $nombre2 ))"
	  elif [ $choix -eq 3 ]
	  then
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			echo "Résultat=$(( $nombre1 * $nombre2 ))"
	  elif [ $choix -eq 4 ]
	  then
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			echo "Résultat=$(( $nombre1 / $nombre2 ))"
	  elif [ $choix -eq 5 ]
	  then
		break
	  fi

	done
	```
	
## Exercice 4

    ```
    while true
	do
	  echo "1. Ajouter"
	  echo "2. Soustraire"
	  echo "3. Multiplier"
	  echo "4. Diviser"
	  echo "5. Moyenne"
	  echo "6. Quitter"

	  read -p "Entrez votre choix : " choix

	  case $choix in
		1)
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			echo "Résultat=$(( $nombre1 + $nombre2 ))"
			;;
		2)
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			echo "Résultat=$(( $nombre1 - $nombre2 ))"
			;;
		3)
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			echo "Résultat=$(( $nombre1 * $nombre2 ))"
			;;
		4)
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			echo "Résultat=$(( $nombre1 / $nombre2 ))"
			;;
		5)
			read -p "Entrez le nombre 1 : " nombre1
			read -p "Entrez le nombre 2 : " nombre2
			somme=$(( nombre1 + nombre2 ))
			echo "Résultat=$(echo "$somme / 2" | bc -l)"
			;;
		6)
			break
			;;
	  esac

	done
    ```

## Exercice 5

    ```
	couleur=$1
	rouge=`tput setaf 1`
	vert=`tput setaf 2`
	reset=`tput sgr0`

	case $couleur in
		rouge) echo "${rouge}Ceci est rouge${reset}";;
		vert) echo "${vert}Ceci est vert${reset}";;
		*) echo "Rouge et vert sont les seules options";;
	esac
    ```