import subprocess
from subprocess import check_output

class NginxController():
    def __init__(self):
        self.userName = ""
        self.serviceName = ""
        self.clusterName = ""
        self.containerId = ""

def nginxGenerateConfig(self):
    print("Generating Nginx Config")
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py {self.clusterName} {self.serviceName} {self.userName}"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

def nginxDeleteConfig(self):
    print("Deleting Nginx Config")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{self.clusterName}-{self.serviceName}-{self.userName}-nginx.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{self.clusterName}-{self.serviceName}-{self.userName}-nginx-2.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{self.clusterName}-{self.serviceName}-{self.userName}-modsecurity.conf"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa
