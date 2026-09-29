# Lab 03 - Init Containers

Definition : un conteneur qui s'execute AVANT les conteneurs principaux
et doit se terminer avec succes pour que ceux-ci demarrent. Sert a
preparer le terrain (attendre une dependance, initialiser un volume).

Sur le fil rouge : wait-for-db boucle tant que Postgres ne repond pas.

Commande de diagnostic :

    kubectl get pod -n demo <nom-du-pod> -o jsonpath='{.status.initContainerStatuses[*].state}'

Mini-lab :

    # Deployer SANS la base d'abord
    kubectl apply -f k8s/00-namespace.yaml -f k8s/01-secret.yaml
    kubectl apply -f k8s/10-deployment.yaml

    # Le Pod reste en Init:0/2, l'init boucle sur la base
    kubectl get pod -n demo
    kubectl logs -n demo <nom-du-pod> -c wait-for-db

    # Lancer la base : l'init se termine, l'app demarre
    kubectl apply -f k8s/02-postgres.yaml
    kubectl get pod -n demo -w
