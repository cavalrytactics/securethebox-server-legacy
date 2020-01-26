import subprocess
import json
import os 
import subprocess
from subprocess import check_output
import time
from os import path
import yaml
from kubernetes import client, config, utils

class KubernetesController():
    def __init__(self):
        self.podId = ""
        self.currentDirectory = ""
        self.clusterName = ""
        self.serviceName = ""
        self.userName = ""
        self.emailAddress = ""
        self.googleClientId = ""
        self.googleClientSecret = ""
        self.kubectlAction = ""

    def loadRemoteConfig(self):
        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()
            print("Listing pods with their IPs:")
            ret = v1.list_pod_for_all_namespaces(watch=False)
            for i in ret.items:
                print("%s\t%s\t%s" %
                    (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
            return True
        except:
            return False

    def setCurrentDirectory(self):
        try:
            self.currentDirectory = os.getcwd()
            return True
        except:
            return False
    
    def setClusterName(self, clusterName):
        try:
            self.clusterName = clusterName
            return True
        except:
            return False
    
    def setServiceName(self, serviceName):
        try:
            self.serviceName = serviceName
            return True
        except:
            return False

    def setUserName(self, userName):
        try:
            self.userName = userName
            return True
        except:
            return False

    def setEmailAddress(self, emailAddress):
        try:
            self.emailAddress = emailAddress
            return True
        except:
            return False

    def setGoogleClientId(self):
        try:
            filePath = "./app_controllers/secrets/googleClientId.txt"
            fileExists = path.exists(filePath)
            if fileExists == False:
                with open(filePath, 'w') as file:
                    environmentVariable = os.environ(['GOOGLE_CLIENT_ID'])
                    file.write(environmentVariable)
            else:
                readGoogleClientIdFile = open(filePath,'r')
                self.googleClientId = readGoogleClientIdFile.read().rstrip('\n')
            return True
        except:
            return False

    def setGoogleClientSecret(self):
        try:
            filePath = "./app_controllers/secrets/googleClientSecret.txt"
            fileExists = path.exists(filePath)
            if fileExists == False:
                with open(filePath, 'w') as file:
                    environmentVariable = os.environ(['GOOGLE_CLIENT_SECRET'])
                    file.write(environmentVariable)
            else:
                readGoogleClientIdFile = open(filePath,'r')
                self.googleClientId = readGoogleClientIdFile.read().rstrip('\n')
            return True
        except:
            return False

    def setPodId(self, podId):
        try:
            self.setPodId = podId
            return True
        except:
            return False
    
    def setKubectlAction(self, kubectlAction):
        try:
            self.kubectlAction = kubectlAction
            return True
        except:
            return False

    def generateIngressYamlFiles(self):
        try:
            fileList = ["01_permissions", "02_cluster-role", "03_config", "04_deployment", "05_service", "06_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/{file}"
                subprocess.Popen([f"python3.7 {fullFilePath}.py {self.clusterName} {self.serviceName}"],shell=True).wait()
                fileCreated = path.exists(f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml")
                if fileCreated == False:
                    return False
            return True
        except:
            return False

    def generateServiceYamlFiles(self):
        try:
            fileList = ["01_deployment", "02_service", "03_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/{file}"
                subprocess.Popen([f"python3.7 {fullFilePath}.py {self.clusterName} {self.serviceName} {self.userName}"],shell=True).wait()
                fileCreated = path.exists(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml")
                if fileCreated == False:
                    return False
            return True
        except:
            return False

    def generateAuthenticationYamlFiles(self):
        try:
            fileList = ["01_deployment", "02_service", "03_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/authentication/{self.serviceName}/{file}"
                subprocess.Popen([f"python3.7 {fullFilePath}.py {self.clusterName} {self.serviceName} {self.userName} {self.emailAddress} {self.googleClientId} {self.googleClientSecret}"],shell=True).wait()
                print(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml")
                fileCreated = path.exists(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml")
                if fileCreated == False:
                    return False
            return True
        except:
            return False

    def deleteIngressYamlFiles(self):
        try:
            fileList = ["01_permissions", "02_cluster-role", "03_config", "04_deployment", "05_service", "06_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/{file}"
                try:
                    subprocess.Popen([f"rm -rf {fullFilePath}-{self.clusterName}-{self.serviceName}.yml"],shell=True).wait()
                except:
                    continue
                fileCreated = path.exists(f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml")
                if fileCreated == True:
                    print(fileCreated, f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml")
                    return False 
            return True
        except:
            return False

    def deleteServiceYamlFiles(self):
        try:
            fileList = ["01_deployment", "02_service", "03_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/{file}"
                try:
                    subprocess.Popen([f"rm -rf {fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml"],shell=True).wait()
                except:
                    continue
                fileCreated = path.exists(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml")
                print(fileCreated)
                if fileCreated == True:
                    return False 
            return True
        except:
            return False

    def deleteAuthenticationYamlFiles(self):
        try:
            fileList = ["01_deployment", "02_service", "03_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/{file}"
                try:
                    subprocess.Popen([f"rm -rf {fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml"],shell=True).wait()
                except:
                    continue
                fileCreated = path.exists(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml")
                print(fileCreated)
                if fileCreated == True:
                    return False 
            return True
        except:
            return False

#  depends on file
    def manageIngressPod(self):
        config.load_kube_config()
        try:
            fileList = ["01_permissions", "02_cluster-role", "03_config", "04_deployment", "05_service", "06_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/{file}"
                try:
                    k8s_client = client.ApiClient()
                    print(f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml")
                    utils.create_from_yaml(k8s_client, f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml")
                    print("Created utils")
                    k8s_api = client.ExtensionsV1beta1Api(k8s_client)
                    deps = k8s_api.read_namespaced_deployment(f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml", "default")
                    print("Deployment {0} created".format(deps.metadata.name))


                    # with open(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml") as f:
                    #     dep = yaml.safe_load(f)
                    #     print("Loaded yaml",dep)
                    #     k8s_client = client.ApiClient()
                    #     if self.kubectlAction == "apply":
                    #         print("Selected Apply")
                    #         resp = k8s_client.ExtensionsV1beta1Api(body=dep, namespace="default")
                    #         print("Deployment created. status='%s'" % resp.metadata.name)
                    #     elif self.kubectlAction == "delete":
                    #         resp = k8s_client.delete_namespaced_deployment(body=dep, namespace="default")
                    #         print("Deployment deleted. status='%s'" % resp.metadata.name)
                except:
                    print("Error", f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml")
                    return False
            return True
        except:
            return False

    def manageAuthenticationPod(self):
        config.load_kube_config()
        try:
            fileList = ["01_deployment", "02_service", "03_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/authentication/{self.serviceName}/{file}"
                try:
                    k8s_client = client.ApiClient()
                    print(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml")
                    utils.create_from_yaml(k8s_client, f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml")
                    k8s_api = client.ExtensionsV1beta1Api(k8s_client)
                    deps = k8s_api.read_namespaced_deployment(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml", "default")
                    print("Deployment {0} created".format(deps.metadata.name))


                    # with open(f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml") as f:
                    #     dep = yaml.safe_load(f)
                    #     print("Loaded yaml",dep)
                    #     k8s_client = client.ApiClient()
                    #     if self.kubectlAction == "apply":
                    #         print("Selected Apply")
                    #         resp = k8s_client.ExtensionsV1beta1Api(body=dep, namespace="default")
                    #         print("Deployment created. status='%s'" % resp.metadata.name)
                    #     elif self.kubectlAction == "delete":
                    #         resp = k8s_client.delete_namespaced_deployment(body=dep, namespace="default")
                    #         print("Deployment deleted. status='%s'" % resp.metadata.name)
                except:
                    print("Error", f"{fullFilePath}-{self.clusterName}-{self.serviceName}-{self.userName}.yml")
                    return False
            return True
        except:
            return False

def kubernetesGetPodId(serviceName, userName):
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    findPod = True
    while findPod:
        print(f"Setup {serviceName}:")
        print("PodList",pod_list)
        for i in pod_list:
            time.sleep(1)
            if f'{serviceName}' in str(i):
                pod_id = str(i)
                findPod=False
                print("FOUND POD_ID:",pod_id)
    return pod_id

def kubernetesGetPodStatus(podId):
    command = ["kubectl","get","pod",podId,"-o","json"]
    command_output = check_output(command)
    parsedJSON = json.loads(command_output)
    currentState = parsedJSON["status"]["containerStatuses"][0]["state"]
    # print(parsedJSON["status"]["containerStatuses"][0]["state"])
    for i in currentState:
        print("Key:",i)
        if i == "running":
            return True
        elif i != "running":
            return False

def kubernetesGeneratePodsYaml(clusterName,serviceName,userName):
    print("Generating Pod Yaml",clusterName,serviceName,userName)
    subprocess.Popen([f"python3.7 ./app_controllers/infrastructure/kubernetes-deployments/pods/{serviceName}/01_deployment.py {clusterName} {serviceName} {userName}"],shell=True).wait()

def kubernetesManageIngressPod(clusterName,serviceName, action):
    print(action,"Ingress Pod:",serviceName)
    # print(f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml")
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/ingress/{serviceName}/02_{clusterName}-{serviceName}-cluster-role.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/ingress/{serviceName}/03_{clusterName}-{serviceName}-config.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/ingress/{serviceName}/04_{clusterName}-{serviceName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/ingress/{serviceName}/05_{clusterName}-{serviceName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/ingress/{serviceName}/06_{clusterName}-{serviceName}-ingress.yml"],shell=True).wait()

def kubernetesCreatePersistentVolumes(action):
    print('Creating Persistent Volume and Claim')
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True).wait()
    # kubectl apply -f ./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/persistent-volume.yml
    # kubectl apply -f ./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/persistent-volume-claim.yml

def kubernetesManagePods(clusterName, serviceName, userName, action):
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/pods/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()

def kubernetesManageServicesPod(clusterName, serviceName, userName, action):
    print(action,"Service Pod:",serviceName)
    if action == 'apply':
        print('Creating Persistent Volume and Claim')
        subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True).wait()
        subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()