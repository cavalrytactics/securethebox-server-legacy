import sys

def writeConfig(**kwargs):
    template = """
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: {serviceName}-{userName}
  annotations:
    kubernetes.io/ingress.class: traefik
    kubernetes.io/preserve-host: "true"
    traefik.frontend.passHostHeader: "false"
    traefik.frontend.priority: "1"
spec:
  rules:
  - host: {serviceName}-{userName}.{clusterName}.securethebox.us
    http:
      paths:
      - path: /
        backend:
          serviceName: {serviceName}-{userName}
          servicePort: http
  - host: {serviceName}-{userName}-management.{clusterName}.securethebox.us
    http:
      paths:
      - path: /
        backend:
          serviceName: {serviceName}-{userName}
          servicePort: management
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/services/'+str(sys.argv[2])+'/03_ingress-'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))