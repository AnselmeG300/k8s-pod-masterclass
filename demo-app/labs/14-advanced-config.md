# Lab 14 - Advanced Pod Configuration

Definition : categorie qui regroupe tout ce qui affine le comportement du
Pod une fois les bases posees : securityContext, terminationGracePeriodSeconds,
configuration DNS, variables d'environnement, volumes.

Sur le fil rouge, deux points comptent vraiment :
- securityContext : non-root, rootfs en lecture seule, capabilities droppees.
- terminationGracePeriodSeconds : laisse le temps au SIGTERM d'etre traite.

Commande de diagnostic :

    kubectl get pod -n demo <nom-du-pod> -o jsonpath='{.spec.securityContext}{"\n"}'

Mini-lab (verifier le durcissement) :

    # Confirmer que le rootfs est bien en lecture seule
    kubectl exec -n demo <nom-du-pod> -c api -- sh -c 'touch /test 2>&1 || echo "rootfs en lecture seule, OK"'

    # Observer l'arret propre : le SIGTERM est traite avant le SIGKILL
    kubectl delete pod -n demo <nom-du-pod>
    # (log "Arret propre en cours (SIGTERM recu)" dans les logs juste avant)
