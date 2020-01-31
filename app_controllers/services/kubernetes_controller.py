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
from kubernetes.client.rest import ApiException
import re
import shutil
import requests
from google.cloud import container_v1

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
        self.kubernetesDeploymentImage = ""
        self.kubernetesDeploymentName = ""
        self.kubernetesHost = ""
        self.googleProjectId = ""
        self.googleCredentials = ""
        self.googleKubernetesComputeZone = ""
        self.googleKubernetesComputeCluster = ""
        self.googleKubernetesClusterOperationInfo = ""
        self.googleServiceAccountEmail = ""

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
            encryptedFileExists = path.exists(f"{fullUncryptedFilePath}{encryptedFileName}")

            if shutil.which("travis") is None:
                print("Travis command does not exist!")
                return True

            if fileExists == True:
                process = subprocess.Popen([f"echo 'yes' | travis encrypt-file -f -p ./app_controllers/secrets/{self.fileName}"],stdout=subprocess.PIPE, shell=True)
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
                            finalDecryptCommand = decryptCommand.replace(f"./app_controllers/secrets/{self.fileName} -d", f"{self.fileName} -d ; cd ../../")
                            if finalDecryptCommand not in dep["jobs"]["include"][0]["before_install"]:
                                dep["jobs"]["include"][0]["before_install"].append(finalDecryptCommand)
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

    def setKubernetesDeploymentName(self, kubernetesDeploymentName):
        self.kubernetesDeploymentName = kubernetesDeploymentName

    def setKubernetesDeploymentImage(self, kubernetesDeploymentImage):
        self.kubernetesDeploymentImage = kubernetesDeploymentImage

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

    def setGoogleProjectId(self, googleProjectId):
        try:
            self.googleProjectId = googleProjectId
            return True
        except:
            return False
    
    def setGoogleKubernetesComputeZone(self, googleKubernetesComputeZone):
        try:
            self.googleKubernetesComputeZone = googleKubernetesComputeZone
            return True
        except:
            return False

    def setGoogleKubernetesComputeCluster(self, googleKubernetesComputeZone):
        try:
            self.googleKubernetesComputeZone = googleKubernetesComputeZone
            return True
        except:
            return False

    def setGoogleServiceAccountEmail(self, googleServiceAccountEmail):
        try:
            self.googleServiceAccountEmail = googleServiceAccountEmail
            return True
        except:
            return False

    def loadGoogleKubernetesServiceAccount(self):
        try:
            subprocess.Popen([f"gcloud auth activate-service-account --key-file {self.currentDirectory}/app_controllers/secrets/{self.fileName} >> /dev/null 2>&1"],shell=True).wait()
            subprocess.Popen([f"gcloud config set account {self.googleServiceAccountEmail} >> /dev/null 2>&1"],shell=True).wait()
            return True
        except:
            return False

    def loadKubernetesConfig(self):
        try:

            return True
        except:
            return False

    # def getKubernetesApiToken(self):
    #     try:
    #         if shutil.which("kubectl") is not None:
    #             print("kubectl exists")
    #             APISERVERcommand = ["kubectl","config","view","--minify","-o","jsonpath='{.clusters[0].cluster.server}'"]
    #             APISERVER = str(check_output(APISERVERcommand).decode("utf-8").replace("'",""))
    #             self.kubernetesHost = APISERVER
    #             print("APISERVER",APISERVER)
    #             # APISERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
    #             SECRETNAMEcommand = ["kubectl","get","serviceaccount","default","-o","jsonpath='{.secrets[0].name}'"]
    #             SECRETNAME = str(check_output(SECRETNAMEcommand).decode("utf-8").replace("'",""))
    #             # SECRET_NAME=$(kubectl get serviceaccount default -o jsonpath='{.secrets[0].name}')
    #             TOKENcommand = ["kubectl","get","secret",SECRETNAME,"-o","jsonpath='{.data.token}'"]
    #             TOKEN = str(check_output(TOKENcommand).decode("utf-8").replace("'",""))
    #             # TOKEN=$(kubectl get secret $SECRET_NAME -o jsonpath='{.data.token}' | base64 --decode)
    #             self.kubernetesApiToken = TOKEN
    #             headers = {"Authorization": f"Bearer {self.kubernetesApiToken}"}
    #             rep = requests.get(self.kubernetesHost,headers=headers,verify=False)
    #             print("RESPONSE:",rep.text)
    #             return True
    #         else:
    #             print("kubectl does not exist!")
    #     except:
    #         return False

    # def selectKubernetesContext(self):
    #     contexts, active_context = config.list_kube_config_contexts()
    #     if not contexts:
    #         print("Cannot find any context in kube-config file.")
    #         return
    #     contexts = [context['name'] for context in contexts]
    #     active_index = contexts.index(active_context['name'])
    #     print(contexts, active_index)
    #     # option, _ = pick(contexts, title="Pick the context to load",
    #     #              default_index=active_index)
    #     # Configs can be set in Configuration class directly or using helper
    #     # utility
    #     config.load_kube_config(context="kubesail-ncmd")

    #     print("Active host is %s" % configuration.Configuration().host)

    #     v1 = client.CoreV1Api()
    #     print("Listing pods with their IPs:")
    #     ret = v1.list_pod_for_all_namespaces(watch=False)
    #     for item in ret.items:
    #         print(
    #             "%s\t%s\t%s" %
    #             (item.status.pod_ip,
    #             item.metadata.namespace,
    #             item.metadata.name))

    # def kubernetesCreateServiceAccount(self):
    #     config.load_kube_config(context=(),config_file=self.currentDirectory+"/app_controllers/secrets/kubernetesConfig.yml")
    #     # print(self.currentDirectory)
    #     v1 = client.CoreV1Api()
    #     print("Listing pods with their IPs:")
    #     ret = v1.list_pod_for_all_namespaces(watch=False)
    #     for i in ret.items:
    #         print("%s\t%s\t%s" %
    #             (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


    # def kubernetesCreateClusterRoleBinding(self):
    #     # config.load_kube_config(config_file=self.currentDirectory+"/app_controllers/secrets/kubernetesConfig.yml")
    #     config.load_kube_config()
    #     role_ref = client.V1RoleRef(
    #             api_group="rbac.authorization.k8s.io",
    #             kind="ClusterRole",
    #             name="cluster-admin"
    #         )
        
    #     subjects = client.V1Subject(
    #         api_group="rbac.authorization.k8s.io",
    #         kind="User",
    #         name="cchong.vise@gmail.com"
    #         )

        
    #     cluster_role_binding = client.V1ClusterRoleBinding(
    #         role_ref=role_ref,
    #         api_version="rbac.authorization.k8s.io/v1",
    #         kind="ClusterRoleBinding",
    #         metadata=client.V1ObjectMeta(name="cluster-admin"),
    #         subjects=subjects
    #         )

    #     api = client.CoreV1Api()

    #     api.cluster_role_binding(
    #         version="v1",
    #         namespace="default",
    #         body=cluster_role_binding,
    #         group="rbac.authorization.k8s.io",
    #         plural="cluster_role_binding"
    #     )
        

    # def kubernetesCreateDeployment(self):
    #     # config.load_kube_config(config_file=self.currentDirectory+"/app_controllers/secrets/kubernetesConfig.yml")
    #     config.load_kube_config()
    #     apps_v1_api = client.AppsV1Api()
    #     volumeMounts = client.V1VolumeMount(
    #         mount_path="/etc/traefik/config",
    #         name="config"
    #     )
        
    #     volumeConfig = client.V1ConfigMapVolumeSource(
    #         name="traefik-config"
    #     )

    #     volumes = client.V1Volume(
    #         name="config",
    #         config_map=volumeConfig
    #     )
    #     container = client.V1Container(
    #         name=self.kubernetesDeploymentName,
    #         image=self.kubernetesDeploymentImage,
    #         image_pull_policy="Never",
    #         args=["--configfile=/etc/traefik/config/traefik.toml",
    #         "--api","--kubernetes","--logLevel=DEBUG"],
    #         volume_mounts=[volumeMounts],
    #         ports=[
    #             client.V1ContainerPort(container_port=443,name="https",protocol="TCP"),
    #             client.V1ContainerPort(container_port=80,name="http",protocol="TCP"),
    #             client.V1ContainerPort(container_port=8080,name="admin",protocol="TCP")],
    #     )
    #     # Template
    #     template = client.V1PodTemplateSpec(
    #         metadata=client.V1ObjectMeta(labels={"app": f"{self.serviceName}-{self.clusterName}-ingress-controller"}),
    #         spec=client.V1PodSpec(containers=[container],service_account_name="traefik-us-west1-a-ingress-controller"))
    #     # Spec
    #     spec = client.V1DeploymentSpec(
    #         replicas=1,
    #         selector={"app":f"{self.serviceName}-{self.clusterName}-ingress-controller"},
    #         template=template)
    #     # Deployment
    #     deployment = client.V1Deployment(
    #         api_version="apps/v1",
    #         kind="Deployment",
    #         metadata=client.V1ObjectMeta(name=f"{self.serviceName}-{self.clusterName}-ingress-controller"),
    #         spec=spec)
    #     # Creation of the Deployment in specified namespace
    #     # (Can replace "default" with a namespace you may have created)
    #     apps_v1_api.create_namespaced_deployment(
    #         namespace="default", body=deployment
    #     )


    # def kubernetesCreateService(self):
    #     core_v1_api = client.CoreV1Api()
    #     body = client.V1Service(
    #         api_version="v1",
    #         kind="Service",
    #         metadata=client.V1ObjectMeta(
    #             name="service-example"
    #         ),
    #         spec=client.V1ServiceSpec(
    #             selector={"app": "deployment"},
    #             ports=[client.V1ServicePort(
    #                 port=5678,
    #                 target_port=5678
    #             )]
    #         )
    #     )
    #     # Creation of the Deployment in specified namespace
    #     # (Can replace "default" with a namespace you may have created)
    #     core_v1_api.create_namespaced_service(namespace="default", body=body)


    # def kubernetesCreateIngress(self):
    #     body = client.NetworkingV1beta1Ingress(
    #         api_version="networking.k8s.io/v1beta1",
    #         kind="Ingress",
    #         metadata=client.V1ObjectMeta(name="ingress-example", annotations={
    #             "nginx.ingress.kubernetes.io/rewrite-target": "/"
    #         }),
    #         spec=client.NetworkingV1beta1IngressSpec(
    #             rules=[client.NetworkingV1beta1IngressRule(
    #                 host="example.com",
    #                 http=client.NetworkingV1beta1HTTPIngressRuleValue(
    #                     paths=[client.NetworkingV1beta1HTTPIngressPath(
    #                         path="/",
    #                         backend=client.NetworkingV1beta1IngressBackend(
    #                             service_port=5678,
    #                             service_name="service-example")

    #                     )]
    #                 )
    #             )
    #             ]
    #         )
    #     )
        
        # Creation of the Deployment in specified namespace
        # (Can replace "default" with a namespace you may have created)
        # client.NetworkingV1beta1Api().create_namespaced_ingress(
        #     namespace="default",
        #     body=body
        # )
    # def manageIngressPod(self):
    #     try:
    #         config.load_kube_config(config_file=self.currentDirectory+"/app_controllers/secrets/kubernetesConfig.yml")
    #         fileList = ["01_permissions", "02_cluster-role", "03_config", "04_deployment", "05_service", "06_ingress"]
    #         currentDirectory = self.currentDirectory
    #         for file in fileList:
    #             print(file)
    #             if "deployment" in file:
    #                 fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/{file}"
    #                 try:
    #                     with open(f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml","r") as f:
    #                         print("opened file...")
    #                         dep = yaml.safe_load(f)
    #                         print(dep)
    #                         k8s_apps_v1 = client.AppsV1Api()
    #                         print(k8s_apps_v1)
    #                         resp = k8s_apps_v1.create_namespaced_deployment(body=dep, namespace="default")
    #                 except:
    #                     print("Error", f"{fullFilePath}-{self.clusterName}-{self.serviceName}.yml")
    #                     return False
    #         return True
    #     except:
    #         return False

    # def kubernetesManageIngressPod(self):
    #     # print(action,"Ingress Pod:",serviceName)
    #     # print(f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml")
    #     subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/01_permissions-{self.clusterName}-{self.serviceName}.yml"],shell=True).wait()
    #     subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/02_cluster-role-{self.clusterName}-{self.serviceName}.yml"],shell=True).wait()
    #     subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/03_config-{self.clusterName}-{self.serviceName}.yml"],shell=True).wait()
    #     subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/04_deployment-{self.clusterName}-{self.serviceName}.yml"],shell=True).wait()
    #     subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/05_service-{self.clusterName}-{self.serviceName}.yml"],shell=True).wait()
    #     subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/06_ingress-{self.clusterName}-{self.serviceName}.yml"],shell=True).wait()



def manageAuthenticationPod(self):
        try:
            config.load_kube_config(config_file=self.currentDirectory+"/app_controllers/secrets/kubernetesConfig.yml")
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