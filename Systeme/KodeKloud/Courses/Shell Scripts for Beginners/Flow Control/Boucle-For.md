# Lab Boucle For

## Exercice 1

	```
	for mission in lunar-mission mars-mission jupiter-mission saturn-mission mercury-mission
	do
	   bash /home/bob/create-and-launch-rocket $mission
	done
```

## Exercice 2

	```
	for nom_mission in $(cat /tmp/assets/mission-names.txt)
	do
		bash /home/bob/create-and-launch-rocket $nom_mission
	done
	```

## Exercice 3

	```
	for i in {31..40}
	do
			echo $i
	done
	```

## Exercice 4

	```
	echo -e " Nom du log \t GET \t POST \t DELETE "
	echo -e "------------------------------------------------------------"

	for app in $(cat /tmp/assets/apps.txt)
	do
	  get_requests=$(cat /var/log/apps/${app}_app.log | grep "GET" | wc -l)
	  post_requests=$(cat /var/log/apps/${app}_app.log | grep "POST" | wc -l)
	  delete_requests=$(cat /var/log/apps/${app}_app.log | grep "DELETE" | wc -l)
	  echo -e " ${app} \t ${get_requests} \t ${post_requests} \t ${delete_requests}"
	done
	```

## Exercice 5

	```
	for file in $(ls images)
	do
			if [[ $file = *.jpeg ]]
			then
				new_name=$(echo $file | sed 's/jpeg/jpg/g')
				mv images/$file images/$new_name
			fi
	done
	```