import sys

def writeConfig(**kwargs):
    template = """
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: auth
  annotations:
    kubernetes.io/ingress.class: traefik
    kubernetes.io/preserve-host: "true"
    traefik.frontend.passHostHeader: "false"
    traefik.frontend.priority: "1"
    ingress.kubernetes.io/auth-type: forward
    ingress.kubernetes.io/auth-url: http://auth
    ingress.kubernetes.io/auth-response-headers: X-Forwarded-User
    ingress.kubernetes.io/auth-trust-headers: true
spec:
  rules:
  - host: auth.securethebox.us
    http:
      paths:
      - path: /
        backend:
          serviceName: auth
          servicePort: http
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/authentication/'+str(sys.argv[2])+'/03_ingress-'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))