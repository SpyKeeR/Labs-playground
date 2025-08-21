# Lab Fonctions

## Exercice 1

Le nom de la fonction se trouve après le mot-clé `function` et avant les doubles parenthèses `()`.
Le nom de la fonction est : prepare-directory-structure

## Exercice 2

    ```
      function prepare-directory-structure(){
      mkdir apps
      cd apps  mkdir app1 app2 app3  touch app1/logs app2/logs app3/logs
      }
    ```

## Exercice 3

    ```
      function add(){
        sum=$(( $1 + $2 ))
      }
      
      result=$(add 3 5)
      echo "Le résultat est $result"
      
    ```
	  
## Exercice 4

    ```
      function add(){
        sum=$(( $1 + $2 ))
        echo $sum
      }
      
      result=$(add 3 5)
      echo "Le résultat est $result"
      
    ```
	  
## Exercice 5
  
    ```
      function add(){
        sum=$(( $1 + $2 ))
      }
      
      result=$(add 3 5)
      echo "Le résultat est $result"
    ```
	  
## Exercice 6
 
	```
	#!/bin/bash
	function read_numbers(){
	  read -p "Entrez le nombre 1 : " number1
	  read -p "Entrez le nombre 2 : " number2
	}

	while true
	do
	  echo "1. Addition"
	  echo "2. Soustraction"
	  echo "3. Multiplication"
	  echo "4. Division"
	  echo "5. Quitter"

	  read -p "Entrez votre choix : " choice

	  case $choice in
		1) read_numbers
		   echo $(( $number1 + $number2 )) ;;
		2) read_numbers
		   echo $(( $number1 - $number2 )) ;;
		3) read_numbers
		   echo $(( $number1 * $number2 )) ;;
		4) read_numbers
		   echo $(( $number1 / $number2 )) ;;
		5) break ;;
	  esac

	done
	```

## Exercice 7
  
    ```
      function launch_rocket(){
        mission_name=$1
      
        mkdir $mission_name
      
        rocket-add $mission_name
      
        rocket-start-power $mission_name
        rocket-internal-power $mission_name
        rocket-start-sequence $mission_name
        rocket-start-engine $mission_name
        rocket-lift-off $mission_name
      
        rocket_status=$(rocket-status $mission_name)
      
        echo "The status of launch is $rocket_status"
      
        if [ $rocket_status = "launching" ]
        then
          sleep 2
          rocket_status=$(rocket-status $mission_name)
        fi
      
        if [ $rocket_status = "failed" ]
        then
          rocket-debug
          exit 1
        fi
      }
      
      launch_rocket $1
    ```