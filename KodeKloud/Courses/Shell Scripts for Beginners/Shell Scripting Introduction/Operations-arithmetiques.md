# Lab - Arithmetic Operations

## Exercice 1
  
	```
	A=20
	B=10

	echo "La somme est $(( A + B ))"
	echo "La différence est $(( A - B ))"
	echo "Le produit est $(( A * B ))"
	echo "Le quotient est $(( A / B ))"
	```

## Exercice 2
  
	```
	A=$1   # Premier argument passé au script
	B=$2   # Deuxième argument passé au script

	echo "La somme est $(( A + B ))"
	echo "La différence est $(( A - B ))"
	echo "Le produit est $(( A * B ))"
	echo "Le quotient est $(( A / B ))"
	```
	
## Exercice 3
  
	```
	prix=$(( $1 * $2 ))  # $1 = prix unitaire, $2 = quantité
	echo "Le prix total pour les articles est de ${prix} dollars"
	```
	
## Exercice 4

	```
	paniers=4
	pommes_par_panier=5

	total_pommes=`expr $paniers \* $pommes_par_panier`
	echo "Nombre total de pommes = $total_pommes"
	```
	
## Exercice 5
  
	```
	num1=$1
	num2=$2
	num3=$3

	somme=$(( num1 + num2 + num3 ))
	moyenne=$(echo "$somme / 3" | bc -l)

	echo "La moyenne est $moyenne"
	```