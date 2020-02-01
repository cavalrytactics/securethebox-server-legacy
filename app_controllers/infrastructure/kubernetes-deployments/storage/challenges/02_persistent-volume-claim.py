import sys

def writeConfig(**kwargs):
    template = """
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: {clusterName}-{userName}-pvc
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/02_persistent-volume-claim-'+str(sys.argv[2])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),userName=str(sys.argv[2]),challengeId=str(sys.argv[3]),gid=str(sys.argv[4]))