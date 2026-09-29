# Lab 11 - Static Pods

Definition : des Pods geres directement par le kubelet d'un noeud, a
partir d'un fichier YAML pose dans un repertoire du noeud, sans passer par
l'API server. Ils y apparaissent en lecture seule (kubectl ne peut pas les
modifier).

Utilite : faire tourner des Pods sans dependre du plan de controle. C'est
ainsi que demarrent l'apiserver, etcd et le scheduler eux-memes (bootstrap).

Note honnete : cette notion est de l'infrastructure. Elle ne s'illustre pas
sur notre API. Le lab ci-dessous se fait sur le noeud, pas sur le fil rouge.

Commande de diagnostic :

    kubectl get pod -n kube-system -o wide

Mini-lab (sur le noeud, avec un cluster kubeadm ou minikube ssh) :

    # Le repertoire surveille par le kubelet
    cat /var/lib/kubelet/config.yaml | grep staticPodPath
    ls /etc/kubernetes/manifests/

Ce qu'on observe : les manifestes du plan de controle sont la, lances en
Static Pods. Ils remontent dans l'API server suffixes du nom du noeud.
