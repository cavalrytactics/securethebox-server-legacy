import sys

def writeConfig(**kwargs):
    template = """
kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  name: auth
  labels:
    app: auth
spec:
  replicas: 1
  selector:
    matchLabels:
      app: auth
  template:
    metadata:
      labels:
        app: auth
    spec:
      containers:
      - name: auth
        image: thomseddon/traefik-forward-auth:2
        env:
          - name: PROVIDERS_GOOGLE_CLIENT_ID
            value: "{googleClientId}"
          - name: PROVIDERS_GOOGLE_CLIENT_SECRET
            value: "{googleClientSecret}"
          - name: SECRET
            value: "random"
          - name: INSECURE_COOKIE
            value: "true"
          - name: COOKIE_DOMAINS
            value: "securethebox.us,us-west1-a.securethebox.us,jenkins-{userName}.us-west1-a.securethebox.us,gitlab-{userName}.us-west1-a.securethebox.us"
          - name: DOMAINS
            value: "securethebox.us,us-west1-a.securethebox.us,jenkins-{userName}.us-west1-a.securethebox.us,gitlab-{userName}.us-west1-a.securethebox.us"
          - name: AUTH_HOST
            value: "auth.securethebox.us"
          - name: DEFAULT_ACTION
            value: "allow"
          - name: WHITELIST
            value: "{emailAddress},service-account@securethebox.iam.gserviceaccount.com"
        ports:
          - containerPort: 4181
            protocol: TCP
        livenessProbe:
            tcpSocket:
              port: 4181
            initialDelaySeconds: 20
            failureThreshold: 3
            successThreshold: 1
            periodSeconds: 10
            timeoutSeconds: 2
        volumeMounts:
          - name: dockersock
            mountPath: "/var/run/docker.sock"
      volumes:
      - name: dockersock
        hostPath:
          path: /var/run/docker.sock
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/authentication/'+str(sys.argv[2])+'/01_deployment-'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]),emailAddress=str(sys.argv[4]),googleClientId=str(sys.argv[5]),googleClientSecret=str(sys.argv[6]))