import subprocess
import json
import os 
import subprocess
from subprocess import check_output
import time
from os import path
from os import environ
import yaml
from kubernetes import client, config, utils
from kubernetes.client import configuration
import re

class KubernetesController():
    def __init__(self):
        self.podId = ""
        self.currentDirectory = ""
        self.clusterName = ""
        self.serviceName = ""
        self.userName = ""
        self.emailAddress = ""
        self.kubectlAction = ""
        self.fileName = ""
        self.encryptedEnvironmentVariables = {}

    def setFileName(self, fileName):
        try:
            self.fileName = fileName
            return True
        except:
            return False
            
    def setTravisEncryptFile(self):
        try:
            fullUncryptedFilePath = f"{self.currentDirectory}/app_controllers/secrets/"
            unencryptedFileName = self.fileName
            encryptedFileName = f"{unencryptedFileName}.enc"
            fileExists = path.exists(f"{fullUncryptedFilePath}{unencryptedFileName}")
            if fileExists == True:
                process = subprocess.Popen([f"echo 'yes' | travis encrypt-file -f -p ./app_controllers/secrets/kubernetesConfig.yml"],stdout=subprocess.PIPE, shell=True)
                finished = True
                keyVariableKEY = ""
                keyVariableVALUE = ""
                ivVariableKEY = ""
                ivVariableVALUE = ""
                decryptCommand = ""
                keyEnvironmentVariable = ""
                ivEnvironmentVariable = ""
                while finished:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        finished = True
                    
                    if "openssl" in output.strip().decode("utf-8"):
                        decryptCommand = str(output.strip().decode("utf-8"))
                        dep = ""
                        with open("./.travis.yml","r") as f:
                            dep = yaml.safe_load(f)
                            if decryptCommand not in dep["jobs"]["include"][0]["before_install"]:
                                dep["jobs"]["include"][0]["before_install"].append(decryptCommand)
                        with open("./.travis.yml","w") as f:
                            yaml.dump(dep, f)
                        os.rename(f"{self.currentDirectory}/{encryptedFileName}",f"{self.currentDirectory}/app_controllers/secrets/{encryptedFileName}")

                        keyEnvironmentVariableMatch = re.finditer("(([$]encrypted.)(.*[_]key))", str(decryptCommand), re.MULTILINE)
                        ivEnvironmentVariableMatch1 = re.finditer("([-]iv.)([$]encrypted.)(.*[_]iv)", str(decryptCommand), re.MULTILINE)
                        for matchNum, match in enumerate(keyEnvironmentVariableMatch, start=1):
                            keyEnvironmentVariable = str(match.group())
                        for matchNum, match in enumerate(ivEnvironmentVariableMatch1, start=1):
                            ivEnvironmentVariable = str(match.group())
                        ivEnvironmentVariableMatch2 = re.finditer("([$]encrypted.)(.*[_]iv)", str(ivEnvironmentVariable), re.MULTILINE)
                        for matchNum, match in enumerate(ivEnvironmentVariableMatch2, start=1):
                            ivEnvironmentVariable = str(match.group())
                        setattr(self, keyEnvironmentVariable, "")
                        keyVariableKEY = keyEnvironmentVariable
                        setattr(self, ivEnvironmentVariable, "")
                        ivVariableKEY = ivEnvironmentVariable
                    
                    if "key:" in output.strip().decode("utf-8"):
                        setattr(self, keyVariableKEY, output.strip().decode("utf-8"))
                        self.encryptedEnvironmentVariables[keyVariableKEY] = output.strip().decode("utf-8").replace("key:","").strip()
                        
                    if "iv:" in output.strip().decode("utf-8"):
                        setattr(self, ivVariableKEY, output.strip().decode("utf-8"))
                        self.encryptedEnvironmentVariables[ivVariableKEY] = output.strip().decode("utf-8").replace("iv:","").strip()
                        return True
            else:
                print("Unencrypted File does not EXIST!",f"{fullUncryptedFilePath}{unencryptedFileName}")
            return True
        except:
            print("You may need to login to Travis")
            return False

    def setTravisUnencryptFile(self):
        try:
            fullencryptedFilePath = f"{self.currentDirectory}/app_controllers/secrets/"
            encryptedFileName = f"{self.fileName}.enc"
            unencryptedFileName = f"{self.fileName}"
            fileCreated = path.exists(f"{fullencryptedFilePath}{encryptedFileName}")
            if fileCreated == True:
                keyVariableKEY = ""
                keyVariableVALUE = ""
                ivVariableKEY = ""
                ivVariableVALUE = ""
                for variable in self.encryptedEnvironmentVariables.keys():
                    if "key" in variable:
                        keyVariableKEY = variable
                        keyVariableVALUE = self.encryptedEnvironmentVariables[variable]
                    elif "iv" in variable:
                        ivVariableKEY = variable
                        ivVariableVALUE = self.encryptedEnvironmentVariables[variable]
                os.chdir(fullencryptedFilePath)
                subprocess.Popen([f"openssl aes-256-cbc -K {keyVariableVALUE} -iv {ivVariableVALUE} -in {encryptedFileName} -out {unencryptedFileName} -d"],shell=True).wait()
                os.chdir(self.currentDirectory)
                return True
            else:
                print("Encrypted File does not EXIST!",f"{fullUncryptedFilePath}{unencryptedFileName}")
            return True
        except:
            print("You may need to login to Travis")
            return False
            
    def loadRemoteConfig(self):
        try:
            config.load_kube_config(config_file=self.currentDirectory+"/app_controllers/secrets/kubernetesConfig.yml")
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

    def setEnvironmentVariable(self, environmentVariable):
        try:
            if os.getenv(environmentVariable) is not None:
                setattr(self, environmentVariable, os.getenv(environmentVariable))
            else:
                print(f"{environmentVariable} is not set")
                return False
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
                subprocess.Popen([f"python3.7 {fullFilePath}.py {self.clusterName} {self.serviceName} {self.userName} {self.emailAddress} {self.GOOGLE_CLIENT_ID} {self.GOOGLE_CLIENT_SECRET}"],shell=True).wait()
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
                if fileCreated == True:
                    return False 
            return True
        except:
            return False

    def manageIngressPod(self):
        config.load_kube_config(config_file="./app_controllers/secrets/kubernetesConfig.yml")
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
        config.load_kube_config(config_file="./app_controllers/secrets/kubernetesConfig.yml")
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