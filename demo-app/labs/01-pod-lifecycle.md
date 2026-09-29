# Lab 01 - Pod Lifecycle

Definition : un Pod passe par des phases successives (Pending, Running,
Succeeded, Failed) qui disent ou en est l'application.

Commande de diagnostic :

    kubectl get pod -n demo -w

Mini-lab :

    # Deployer l'ensemble
    kubectl apply -f k8s/

    # Observer les transitions en direct
    kubectl get pod -n demo -w

Ce qu'on observe :
- Pending : le Pod attend d'etre place sur un noeud, ou attend ses volumes.
- Running mais 0/1 READY : les conteneurs tournent, mais la readiness refuse.
- Running 1/1 READY : le Pod recoit du trafic.

Arret propre :

    kubectl delete pod -n demo -l app=demo-api
    # Le log "Arret propre en cours (SIGTERM recu)" apparait avant la fin.
