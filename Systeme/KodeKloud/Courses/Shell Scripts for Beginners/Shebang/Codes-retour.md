# Lab Code retour

## Exercice 1

Réponse : 0

## Exercice 2

Réponse : 127

## Exercice 3

Réponse : 126
	  
## Exercice 4

      ```
      mission_name=$1

      mkdir $mission_name
      
      rocket-add $mission_name
      
      rocket-start-power $mission_name
      rocket-internal-power $mission_name
      rocket-start-sequence $mission_namerocket-start-engine $mission_name
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
      ```