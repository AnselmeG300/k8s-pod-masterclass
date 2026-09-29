#!/usr/bin/env bash
# Setup complet de la demo sur Killercoda.
# Cible : le playground Kubernetes (cluster kubeadm, 2 noeuds, session 60 min).
#
# Prealable UNIQUE (a faire une fois depuis ta machine, PAS dans Killercoda) :
#   docker build -t TON_COMPTE/demo-api:1.0 .
#   docker push TON_COMPTE/demo-api:1.0
#
# Usage dans Killercoda :
#   git clone <ton-repo> && cd demo-app
#   IMAGE=TON_COMPTE/demo-api:1.0 ./killercoda/setup.sh
#
# Options :
#   USE_EMPTYDIR=true  -> Postgres en emptyDir, sans provisioner de stockage
#
set -euo pipefail

IMAGE="${IMAGE:-CHANGE_ME/demo-api:1.0}"
USE_EMPTYDIR="${USE_EMPTYDIR:-false}"
LPP_VERSION="v0.0.37"   # local-path-provisioner (v0.0.34+ pour CVE-2025-62878)

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ "$IMAGE" = "CHANGE_ME/demo-api:1.0" ]; then
  echo "ATTENTION : variable IMAGE non definie."
  echo "Le cluster Killercoda ne voit pas les images construites localement."
  echo "Pousse l'image sur ton Docker Hub, puis relance avec :"
  echo "  IMAGE=TON_COMPTE/demo-api:1.0 ./killercoda/setup.sh"
  exit 1
fi

echo "==> Namespace et secret"
kubectl apply -f "$ROOT/k8s/00-namespace.yaml" -f "$ROOT/k8s/01-secret.yaml"

if [ "$USE_EMPTYDIR" = "true" ]; then
  echo "==> Postgres (emptyDir, sans provisioner)"
  kubectl apply -f "$ROOT/killercoda/02-postgres-emptydir.yaml"
else
  echo "==> Provisioner de stockage local-path ($LPP_VERSION)"
  kubectl apply -f "https://raw.githubusercontent.com/rancher/local-path-provisioner/${LPP_VERSION}/deploy/local-path-storage.yaml"
  kubectl -n local-path-storage rollout status deploy/local-path-provisioner --timeout=120s
  echo "==> local-path defini comme StorageClass par defaut"
  kubectl patch storageclass local-path \
    -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
  echo "==> Postgres (StatefulSet + PVC)"
  kubectl apply -f "$ROOT/k8s/02-postgres.yaml"
fi

echo "==> API, Service et PodDisruptionBudget (image : $IMAGE)"
kubectl apply -f "$ROOT/k8s/10-deployment.yaml" -f "$ROOT/k8s/11-service.yaml" -f "$ROOT/k8s/12-pdb.yaml"
kubectl set image deployment/demo-api api="$IMAGE" -n demo

echo "==> Attente de la disponibilite (l'init container attend d'abord la base)"
kubectl -n demo rollout status deployment/demo-api --timeout=180s || true

echo
echo "Etat du namespace demo :"
kubectl get pod -n demo -o wide
echo
echo "Tester l'API :"
echo "  kubectl -n demo port-forward svc/demo-api 8080:80 &"
echo "  curl -s localhost:8080/ ; echo"
