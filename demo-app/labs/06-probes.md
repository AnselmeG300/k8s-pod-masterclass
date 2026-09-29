# Lab 06 - Liveness, Readiness, Startup Probes

Definition : trois sondes, trois roles.
- Startup : l'app a-t-elle fini de demarrer ? (protege le demarrage lent)
- Liveness : est-elle toujours vivante ? sinon on redemarre le conteneur.
- Readiness : peut-elle recevoir du trafic ? sinon on la sort du Service.

Piege classique : ne jamais mettre la base dans la liveness. Une base qui
tombe ferait redemarrer tous les Pods en boucle, sans raison.

Commande de diagnostic :

    kubectl describe pod -n demo <nom-du-pod> | grep -A3 -E 'Liveness|Readiness|Startup'

Mini-lab (readiness vs liveness) :

    # Couper la base : readyz -> 503, healthz -> 200
    kubectl scale statefulset postgres -n demo --replicas=0

    # Le Pod passe NOT READY mais N'EST PAS redemarre (RESTARTS reste stable)
    kubectl get pod -n demo -w

    # Retablir : le Pod redevient READY sans avoir redemarre
    kubectl scale statefulset postgres -n demo --replicas=1
