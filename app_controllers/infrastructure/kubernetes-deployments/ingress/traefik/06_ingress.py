import sys

# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=traefik.securethebox.us"
# kubectl -n kube-system create secret tls traefik-ui-tls-cert --key=tls.key --cert=tls.crt

def writeConfig(**kwargs):
    template = """
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: {serviceName}-{clusterName}-ingress-controller
  namespace: default
  annotations:
    kubernetes.io/ingress.class: traefik
    external-dns.alpha.kubernetes.io/target: {serviceName}.{clusterName}.securethebox.us
    ingress.kubernetes.io/auth-trust-headers: true
    ingress.kubernetes.io/auth-type: forward
    ingress.kubernetes.io/auth-url: http://auth
    ingress.kubernetes.io/auth-response-headers: X-Forwarded-User
spec:
  rules:
    - host: {serviceName}.{clusterName}.securethebox.us
      http:
        paths:
        - path: /
          backend:
            serviceName: {serviceName}-{clusterName}-ingress-controller
            servicePort: admin
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/ingress/'+str(sys.argv[2])+'/06_ingress-'+str(sys.argv[1])+'-'+str(sys.argv[2])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]))