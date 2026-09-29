# Lab 10 - Scheduling

Definition : le scheduler decide sur quel noeud placer un Pod. On peut
l'orienter avec nodeSelector (simple), nodeAffinity (regles souples ou
dures), tolerations (accepter des noeuds taches), topologySpreadConstraints
(repartir les replicas).

Sur le fil rouge : un nodeSelector commente dans le Deployment sert
d'exemple a activer.

Commande de diagnostic :

    kubectl get pod -n demo -o wide

Mini-lab :

    # Voir sur quels noeuds tournent les replicas
    kubectl get pod -n demo -o wide

    # Forcer un placement : labelliser un noeud puis decommenter le
    # nodeSelector du Deployment (kubernetes.io/os: linux, ou un label maison)
    kubectl label node <nom-du-noeud> role=api
    # nodeSelector: { role: api }  dans 10-deployment.yaml, puis reappliquer

Note : sur un cluster mono-noeud (minikube), le placement est trivial.
L'interet apparait des qu'il y a plusieurs noeuds.
