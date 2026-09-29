# Lab 12 - User Namespaces

Definition : mecanisme Linux ou un conteneur peut se croire root alors que
sur le noeud son UID est un identifiant banal, sans privilege. Interet
securitaire : une evasion de conteneur n'aboutit pas a du root sur l'hote.

Stable depuis Kubernetes 1.33, et necessite un cluster correctement
configure (runtime et noyau compatibles).

Sur le fil rouge : on a deja une bonne base (image non-root dans le
Dockerfile). Les User Namespaces vont plus loin en isolant l'espace des UID.

Activation (champ au niveau du Pod) :

    spec:
      hostUsers: false

Commande de diagnostic :

    kubectl get pod -n demo <nom-du-pod> -o jsonpath='{.spec.hostUsers}{"\n"}'

Note honnete : a n'activer que si le cluster le supporte. A defaut, garder
au minimum runAsNonRoot true, deja en place dans nos manifestes.
