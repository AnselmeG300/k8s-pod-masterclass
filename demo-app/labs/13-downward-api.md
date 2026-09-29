# Lab 13 - Downward API

Definition : mecanisme qui expose a un conteneur des informations sur son
propre Pod (nom, namespace, IP, noeud, labels), en variables d'environnement
ou en fichiers dans un volume.

Sur le fil rouge : POD_NAME et NODE_NAME viennent de la Downward API et sont
renvoyes dans les reponses de l'API.

Commande de diagnostic :

    kubectl exec -n demo <nom-du-pod> -c api -- env | grep -E 'POD_NAME|NODE_NAME'

Mini-lab :

    # L'app renvoie son identite : utile pour savoir quel replica a repondu
    kubectl port-forward -n demo svc/demo-api 8080:80 &
    curl -s localhost:8080/ ; echo

Ce qu'on observe : le champ "pod" et le champ "node" de la reponse changent
selon le replica qui traite la requete.
