# Lab - Arguments de commande

## Exercice 1

	```
	bob@caleston-lp10:~$ cat create-and-launch-rocket
	mission_name=$1
	mkdir $mission_name

	rocket-add $mission_name

	rocket-start-power $mission_name
	rocket-internal-power $mission_name
	rocket-start-sequence $mission_name
	rocket-start-engine $mission_name
	rocket-lift-off $mission_name

	rocket-status $mission_name
	```
  
## Exercice 2

	```
	$ bash print-capital.sh
	```
  
## Exercice 3
  
	```
	bob@caleston-lp10:~$ cat print-capital.sh
	echo "Capital city of $1 is $2"
	```
  
## Exercice 4
  
	```
	bob@caleston-lp10:~$ cat backup-file.sh
	set -e
	file_name=$1
	cp $file_name ${file_name}_bkp
	echo "Done"
	```
  
## Exercice 5
  
	```
	new_shell=$2
	user_name=$1
	useradd -s $new_shell $user_name
	```