# demo-api : application fil rouge Kubernetes

Petite API HTTP (FastAPI) adossee a une base Postgres. Elle sert de fil rouge
pour illustrer, sur un cas unique et realiste, tous les elements d'un Pod.

L'app ne fait presque rien de metier : elle expose des endpoints de sante et
ecrit des logs. Tout est concu pour donner un point d'accroche concret a
chaque notion.

## Endpoints

- `GET /` : identite du Pod (nom, noeud).
- `GET /startupz` : 200 une fois le warm-up termine, 503 avant. Cible de la startup probe.
- `GET /healthz` : 200 tant que le process repond. Cible de la liveness probe. Ne depend PAS de la base.
- `GET /readyz` : 200 si warm-up fini ET base joignable, sinon 503. Cible de la readiness probe.

## Variables d'environnement

| Variable        | Defaut       | Role                                          |
|-----------------|--------------|-----------------------------------------------|
| DB_HOST         | postgres     | Hote de la base                               |
| DB_PORT         | 5432         | Port de la base                               |
| DB_NAME         | demo         | Nom de la base                                |
| DB_USER         | demo         | Utilisateur                                   |
| DB_PASSWORD     | demo         | Mot de passe (a mettre en Secret)             |
| POD_NAME        | hostname     | Injecte via Downward API                      |
| NODE_NAME       | inconnu      | Injecte via Downward API                      |
| STARTUP_DELAY   | 15           | Duree du warm-up simule (secondes)            |
| LOG_PATH        | /var/log/app/app.log | Fichier de log suivi par le sidecar   |

## Pourquoi cette app, notion par notion

C'est le mapping qui servira de colonne vertebrale au carrousel.

| Notion du Pod              | Point d'accroche dans l'app                                            |
|----------------------------|------------------------------------------------------------------------|
| Pod Lifecycle              | Pending, Running, arret propre sur SIGTERM (log dedie dans lifespan).   |
| Pod Conditions             | PodScheduled, Initialized, ContainersReady, Ready pilotees par les probes. |
| Init Containers            | Un init container attend que Postgres reponde avant de lancer l'API.   |
| Sidecar Containers         | Un sidecar tail le fichier de log partage via un emptyDir.             |
| Ephemeral Containers       | Debug a chaud avec kubectl debug, sans redemarrer le conteneur.        |
| Liveness / Readiness / Startup | /healthz, /readyz, /startupz : trois roles distincts, pas d'amalgame. |
| Disruptions                | Un PodDisruptionBudget protege l'API pendant les drains de noeud.      |
| Pod Hostname               | hostname et subdomain, visibles dans la reponse de l'app.             |
| QoS Classes                | requests/limits regles pour montrer Guaranteed vs Burstable.          |
| Scheduling                 | nodeSelector / affinity pour placer le Pod la ou on veut.             |
| Static Pods                | Variante geree par le kubelet (rappel : c'est ainsi que tourne le control plane). |
| User Namespaces            | Conteneur non-root, mapping des UID hote/conteneur.                    |
| Downward API               | POD_NAME et NODE_NAME injectes depuis les metadonnees du Pod.         |
| Advanced Pod Configuration | securityContext, volumes, terminationGracePeriodSeconds, etc.         |

## Construire et lancer

```bash
# Build de l'image
docker build -t demo-api:1.0 .

# Base de test locale (image standard, aucun code a ecrire)
docker run -d --name postgres -e POSTGRES_DB=demo \
  -e POSTGRES_USER=demo -e POSTGRES_PASSWORD=demo postgres:16-alpine

# L'API (pointe vers la base ci-dessus)
docker run --rm -p 8000:8000 --link postgres \
  -e DB_HOST=postgres demo-api:1.0
```

La base Postgres est une image standard : aucun code a produire de ce cote.

## Deploiement sur Kubernetes

Les manifestes sont dans `k8s/`. Ils portent, sur cette seule app, tous les
elements du Pod (init container, sidecar natif, trois probes, Downward API,
securityContext, QoS, PodDisruptionBudget).

    # Construire l'image et la rendre disponible au cluster
    docker build -t demo-api:1.0 .
    # minikube : eval $(minikube docker-env) puis rebuild
    # kind     : kind load docker-image demo-api:1.0

    kubectl apply -f k8s/
    kubectl get pod -n demo -w

## Mini-labs

Le dossier `labs/` contient un fichier par notion : definition courte,
commande de diagnostic, mini-lab reproductible. Voir `labs/README.md` pour
l'ordre conseille et les prerequis.
