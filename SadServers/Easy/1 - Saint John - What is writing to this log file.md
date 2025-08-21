# Saint John - What is Writing to this log file?

## 1. Identifier le processus utilisant le fichier de log

```bash
lsof | grep /var/log/bad.log
```

*Affiche le processus qui écrit dans le fichier `/var/log/bad.log`.*

## 2. Vérifier les détails du processus

```bash
ps -p 591 -f
```

*Montre le chemin et l'interpréteur utilisé pour exécuter le processus.*

## 3. Vérifier la hiérarchie des processus

```bash
pstree -p
```

*Affiche comment le processus est appelé et ses relations avec d'autres processus.*

## 4. Vérifier les tâches cron de l'utilisateur

```bash
crontab -l
```

*Affiche les tâches planifiées pour l'utilisateur, notamment celle qui relance le script au démarrage.*

## 5. Terminer le processus

```bash
kill -15 591
```

*Arrête le processus identifié pour libérer le fichier de log.*