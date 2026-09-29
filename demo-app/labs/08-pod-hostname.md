# Lab 08 - Pod Hostname

Definition : par defaut le hostname d'un Pod est son nom, qui change a
chaque recreation. Les champs hostname et subdomain, combines a un Service
headless, donnent a chaque Pod un nom DNS stable et joignable
individuellement.

Sur le fil rouge : l'API passe par un Service classique (pas besoin
d'identite stable). C'est Postgres, en StatefulSet derriere un Service
headless, qui obtient un nom stable : postgres-0.postgres.demo.svc.

Commande de diagnostic :

    kubectl get pod postgres-0 -n demo -o jsonpath='{.spec.hostname}{"\n"}'

Mini-lab :

    # Resoudre le nom stable du Pod Postgres depuis un autre Pod
    kubectl run dns-test -n demo --rm -it --image=busybox:1.36 --restart=Never -- \
      nslookup postgres-0.postgres.demo.svc.cluster.local

Ce qu'on observe : le nom reste identique meme si le Pod est recree,
contrairement a un nom de Pod de Deployment (suffixe aleatoire).
