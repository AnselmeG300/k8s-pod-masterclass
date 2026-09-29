# Lab 02 - Pod Conditions

Definition : les conditions sont le detail sous la phase. Elles disent
quelle etape precise est franchie : PodScheduled, Initialized,
ContainersReady, Ready.

Commande de diagnostic :

    kubectl get pod -n demo <nom-du-pod> -o jsonpath='{.status.conditions}' | python3 -m json.tool

ou, plus lisible :

    kubectl describe pod -n demo <nom-du-pod>

Mini-lab :

    # Couper la base pour voir la condition Ready basculer a False
    kubectl scale statefulset postgres -n demo --replicas=0

    # Ready passe a False, mais Initialized reste True
    kubectl get pod -n demo <nom-du-pod> -o jsonpath='{.status.conditions[*].type}{"\n"}'
    kubectl describe pod -n demo <nom-du-pod> | grep -A6 Conditions

    # Retablir
    kubectl scale statefulset postgres -n demo --replicas=1

Lecture :
- Ready=False mais Running : c'est la readiness probe (base injoignable).
- Initialized=False : un init container est coince (ici wait-for-db).
