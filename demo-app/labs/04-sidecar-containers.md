# Lab 04 - Sidecar Containers

Definition : un conteneur secondaire qui tourne en parallele du conteneur
principal, dans le meme Pod, pour lui rendre un service (logs, proxy,
synchro). Depuis Kubernetes 1.29, on le declare comme un init container
avec restartPolicy Always : il demarre avant l'app et s'arrete apres.

Sur le fil rouge : log-shipper suit le fichier de log via un emptyDir
partage et le pousse sur stdout.

Commande de diagnostic :

    kubectl logs -n demo <nom-du-pod> -c log-shipper

Mini-lab :

    # Generer du trafic sur l'API
    kubectl port-forward -n demo svc/demo-api 8080:80 &
    for i in $(seq 1 5); do curl -s localhost:8080/ ; echo; done

    # Les lignes ecrites par l'API sortent via le sidecar
    kubectl logs -n demo <nom-du-pod> -c log-shipper --tail=20
