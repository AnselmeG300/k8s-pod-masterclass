# Lab 09 - Quality of Service Classes

Definition : Kubernetes classe chaque Pod selon la declaration de ses
ressources. La classe decide de l'ordre d'eviction en cas de pression
memoire sur le noeud.
- Guaranteed : requests == limits (CPU et memoire) sur tous les conteneurs.
- Burstable : des requests definies, inferieures aux limits.
- BestEffort : ni requests ni limits. Premier sacrifie.

Sur le fil rouge : API en Burstable, Postgres en Guaranteed.

Commande de diagnostic :

    kubectl get pod -n demo -o custom-columns='NOM:.metadata.name,QOS:.status.qosClass'

Mini-lab :

    kubectl get pod -n demo \
      -o custom-columns='NOM:.metadata.name,QOS:.status.qosClass'

Ce qu'on observe :
- postgres-0 : Guaranteed
- demo-api-xxxx : Burstable

Pour verifier le raisonnement : requests et limits par conteneur

    kubectl get pod postgres-0 -n demo \
      -o jsonpath='{.spec.containers[0].resources}{"\n"}'
