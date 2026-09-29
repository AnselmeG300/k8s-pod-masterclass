# Lab 05 - Ephemeral Containers

Definition : un conteneur injecte dans un Pod DEJA en cours d'execution,
uniquement pour du debug. Temporaire, sans probes, ne redemarre jamais.
Utile quand l'image principale est minimaliste (pas de shell, pas d'outils).

Notre image API est basee sur python-slim et n'a pas les outils reseau.

Commande de diagnostic :

    kubectl debug -n demo <nom-du-pod> -it --image=busybox:1.36 --target=api

Mini-lab :

    # S'attacher un conteneur outille dans le Pod de l'API
    kubectl debug -n demo <nom-du-pod> -it --image=busybox:1.36 --target=api

    # Depuis l'interieur, tester la base sans rien redemarrer
    nc -z postgres 5432 && echo "base joignable"
    wget -qO- localhost:8000/readyz

Note : --target permet de partager l'espace des processus du conteneur vise.
