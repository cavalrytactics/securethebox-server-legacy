import sys

def writeConfig(**kwargs):
    template = """
kind: PersistentVolume
apiVersion: v1
metadata:
  name: {clusterName}-{userName}-pv
  labels:
    type: local
  annotations:
    pv.beta.kubernetes.io/gid: "{gid}"
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/var/log/challenge{challengeId}"
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/01_persistent-volume-'+str(sys.argv[2])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),userName=str(sys.argv[2]),challengeId=str(sys.argv[3]),gid=str(sys.argv[4]))