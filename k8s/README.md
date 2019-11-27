# Basic configuration for running in Kubenetes

These files can be modified and applied using kubectl apply -f {file}.  The configmap is built by converting the yaml config file to json:

    kubectl apply -f hem_namespace.yaml
    kubectl apply -f hem_configmap.yaml
    kubectl apply -f hem_pod.yaml

