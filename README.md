# Lancer la demo sur Killercoda

Le playground Kubernetes de Killercoda donne un cluster kubeadm de deux
noeuds, pour une session de 60 minutes. C'est un bon terrain pour ces labs :
avec deux noeuds, le scheduling, le drain, le PodDisruptionBudget et le
hostname deviennent reellement demonstrables.

Deux specificites de l'environnement obligent a adapter le lancement.

## 1. L'image de l'API

Le cluster tourne sous containerd. Une image construite en local n'est pas
visible par le cluster. Le chemin le plus simple :

Une fois, depuis TA machine (pas dans Killercoda) :

    docker build -t TON_COMPTE/demo-api:1.0 .
    docker push TON_COMPTE/demo-api:1.0

Ensuite, dans chaque session Killercoda, l'image est simplement tiree depuis
Docker Hub. Rien a reconstruire.

## 2. Le stockage

Le cluster est livre sans provisioner de stockage par defaut. Le PVC du
StatefulSet Postgres resterait bloque en Pending. Le script installe donc
le local-path-provisioner de Rancher et le definit comme StorageClass par
defaut, ce qui garde le StatefulSet intact.

Si l'installation du provisioner echoue (pas d'acces reseau, par exemple),
bascule sur la variante emptyDir avec l'option `USE_EMPTYDIR=true`.

## Lancement

    git clone <ton-repo>
    cd demo-app
    IMAGE=TON_COMPTE/demo-api:1.0 ./killercoda/setup.sh

Variante sans provisioner (Postgres en emptyDir) :

    IMAGE=TON_COMPTE/demo-api:1.0 USE_EMPTYDIR=true ./killercoda/setup.sh

## Bon a savoir

- La session dure 60 minutes et ne survit pas a un rafraichissement de page.
  Tout est scripte pour etre rejoue vite.
- La variante emptyDir sacrifie l'identite reseau stable du StatefulSet :
  le lab Pod Hostname se fait alors sur la version StatefulSet (mode par
  defaut), pas sur cette variante.
- Les labs 11 (Static Pods) et 12 (User Namespaces) restent de
  l'infrastructure et se traitent sur le noeud, comme indique dans `labs/`.
