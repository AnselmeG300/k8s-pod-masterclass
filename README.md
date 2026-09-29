# Mini-labs : les elements du Pod sur l'app fil rouge

Chaque fichier reprend une notion : definition courte, commande de
diagnostic cle, mini-lab reproductible, et ce qu'on observe.

Ordre conseille (celui du carrousel) :

1. Pod Lifecycle : 01-pod-lifecycle.md
2. Pod Conditions : 02-pod-conditions.md
3. Init Containers : 03-init-containers.md
4. Sidecar Containers : 04-sidecar-containers.md
5. Ephemeral Containers : 05-ephemeral-containers.md
6. Probes (liveness, readiness, startup) : 06-probes.md
7. Disruptions : 07-disruptions.md
8. Pod Hostname : 08-pod-hostname.md
9. QoS Classes : 09-qos-classes.md
10. Scheduling : 10-scheduling.md
11. Static Pods : 11-static-pods.md (infra, hors fil rouge)
12. User Namespaces : 12-user-namespaces.md
13. Downward API : 13-downward-api.md
14. Advanced Pod Configuration : 14-advanced-config.md

## Prerequis

- Un cluster (minikube ou kind conviennent), kubectl configure.
- L'image demo-api:1.0 construite et disponible pour le cluster.
  Avec minikube : `eval $(minikube docker-env) && docker build -t demo-api:1.0 .`
  Avec kind : `kind load docker-image demo-api:1.0`

## Deploiement complet

    kubectl apply -f k8s/
    kubectl get pod -n demo -w

## Honnetete sur la portee

Les notions 11 (Static Pods) et, en partie, 12 (User Namespaces) sont de
l'infrastructure : elles ne se demontrent pas sur l'API elle-meme. Les labs
correspondants se font sur le noeud ou exigent un cluster specifiquement
configure. C'est signale dans chaque fichier.
