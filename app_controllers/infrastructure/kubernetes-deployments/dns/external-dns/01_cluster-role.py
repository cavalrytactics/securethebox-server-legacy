import sys

def writeConfig(**kwargs):
    template = """
apiVersion: v1
kind: ServiceAccount
metadata:
name: external-dns
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
name: external-dns
rules:
- apiGroups: [""]
resources: ["services"]
verbs: ["get","watch","list"]
- apiGroups: [""]
resources: ["pods"]
verbs: ["get","watch","list"]
- apiGroups: ["extensions"] 
resources: ["ingresses"] 
verbs: ["get","watch","list"]
- apiGroups: [""]
resources: ["nodes"]
verbs: ["list"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
name: external-dns-viewer
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: external-dns
subjects:
- kind: ServiceAccount
name: external-dns
namespace: default
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/dns/external-dns/01_cluster-role-external-dns-'+str(sys.argv[2])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]), userName=str(sys.argv[2]))