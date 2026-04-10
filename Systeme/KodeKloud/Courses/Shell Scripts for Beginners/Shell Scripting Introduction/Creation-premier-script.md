# Lab - Création du premier script

## Exercice 1
  
	```bash
	vi create-and-launch-rocket
	```

	```text
	mkdir lunar-mission
	rocket-add lunar-mission
	rocket-start-power lunar-mission
	rocket-internal-power lunar-mission
	rocket-start-sequence lunar-mission
	rocket-start-engine lunar-mission
	rocket-lift-off lunar-mission
	rocket-status lunar-mission
	```
 
## Exercice 2
  
	```bash
	$ chmod +x create-and-launch-rocket
	```
 
## Exercice 3
  
	```bash
	$ ./create-and-launch-rocket
	```

## Exercice 4
  
	```bash
	$ chmod +x /home/bob/say_hello.sh
	```

## Exercice 5
  
	```bash
	$ vi create-directory-structure.sh
	```
  
	```text
	mkdir countries
	cd countries
	mkdir USA India UK
	echo "Washington, D.C" > USA/capital.txt
	echo "London" > UK/capital.txt
	echo "New Delhi" > India/capital.txt
	uptime
	```

## Exercice 6
  
	```bash
	vi create-directory-structure-v2.sh
	```
	
	```text
	mkdir countries
	mkdir -p countries/USA countries/India countries/UK
	echo "Washington, D.C" > countries/USA/capital.txt
	echo "London" > countries/UK/capital.txt
	echo "New Delhi" > countries/India/capital.txt
	uptime
	```