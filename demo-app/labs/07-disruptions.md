# Lab 07 - Disruptions

Definition : toute interruption qui supprime un Pod.
- Involontaire : crash de noeud, panne materielle. Non encadrable.
- Volontaire : drain pour maintenance, mise a jour. Encadrable par un
  PodDisruptionBudget (PDB).

Sur le fil rouge : 2 replicas + PDB minAvailable 1.

Commande de diagnostic :

    kubectl get pdb -n demo

Mini-lab :

    # Etat du budget
    kubectl get pdb demo-api -n demo

    # Simuler une maintenance : drainer un noeud
    kubectl drain <nom-du-noeud> --ignore-daemonsets --delete-emptydir-data

Ce qu'on observe : le drain evacue les Pods un par un et respecte le PDB.
Il ne peut pas evacuer les deux replicas en meme temps.

    # Reautoriser le noeud
    kubectl uncordon <nom-du-noeud>
