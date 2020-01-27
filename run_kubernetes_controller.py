from app_controllers.services.kubernetes_controller import KubernetesController
import os
import yaml
import subprocess
from os import path
from subprocess import check_output
import re

kc = KubernetesController()

testData = {
    "clusterName": "us-west1-a",
    "serviceName_ingress": "traefik",
    "serviceName_service": "jenkins",
    "serviceName_authentication": "auth",
    "userName": "charles",
    "emailAddress": "jidokaus@gmail.com",
    "kubectlAction_apply": "apply",
    "kubectlAction_delete": "delete",
    "dockerePodId": "pod_id_123",
    "unencryptedFileNames": ["kubernetesConfig.yml"],
    "environmentVariablesList": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
}

def test_setCurrentDirectory():
    assert kc.setCurrentDirectory() == True

def test_setFileName():
    for file in testData["unencryptedFileNames"]:
        assert kc.setFileName(file) == True

def test_setTravisEncryptFile():
    kc.setCurrentDirectory() == True
    for file in testData["unencryptedFileNames"]:
        kc.setFileName(file)
        assert kc.setTravisEncryptFile() == True

def test_setClusterName():
    assert kc.setClusterName(testData["clusterName"]) == True

def test_setServiceName():
    assert kc.setServiceName(testData["serviceName_service"]) == True

def test_setUserName():
    assert kc.setUserName(testData["userName"]) == True

def test_setEmailAddress():
    assert kc.setEmailAddress(testData["emailAddress"]) == True

def test_setEnvironmentVariables():
    for var in testData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var) == True
# def test_setGoogleClientId():
#     kc.setCurrentDirectory()
#     assert kc.setGoogleClientId() == True

# def test_setGoogleClientSecret():
#     kc.setCurrentDirectory()
#     assert kc.setGoogleClientSecret() == True

def test_setPodId():
    assert kc.setPodId(testData["dockerePodId"]) == True

def test_setKubectlAction():
    assert kc.setKubectlAction(testData["kubectlAction_apply"]) == True
    assert kc.setKubectlAction(testData["kubectlAction_delete"]) == True

def test_generateIngressYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_ingress"])
    kc.setUserName(testData["userName"])
    assert kc.generateIngressYamlFiles() == True

def test_generateServiceYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_service"])
    kc.setUserName(testData["userName"])
    assert kc.generateServiceYamlFiles() == True

# def test_generateAuthenticationYamlFiles():
#     kc.setCurrentDirectory()
#     kc.setClusterName(testData["clusterName"])
#     kc.setServiceName(testData["serviceName_authentication"])
#     kc.setUserName(testData["userName"])
#     kc.setEmailAddress(testData["emailAddress"])
#     for var in testData["environmentVariablesList"]:
#         assert kc.setEnvironmentVariable(var)
#     assert kc.generateAuthenticationYamlFiles() == True

def test_loadRemoteConfig():
    kc.setCurrentDirectory()
    assert kc.loadRemoteConfig() == True

# def test_manageAuthenticationPod():
#     kc.setCurrentDirectory()
#     kc.setClusterName(testData["clusterName"])
#     kc.setServiceName(testData["serviceName_authentication"])
#     kc.setUserName(testData["userName"])
#     kc.setKubectlAction(testData["kubectlAction_apply"])
#     assert kc.manageAuthenticationPod() == True

# def test_manageIngressPod():
#     kc.setCurrentDirectory()
#     kc.setClusterName(testData["clusterName"])
#     kc.setServiceName(testData["serviceName_ingress"])
#     kc.setKubectlAction(testData["kubectlAction_apply"])
#     assert kc.manageIngressPod() == True

def test_deleteIngressYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_ingress"])
    kc.setUserName(testData["userName"])
    kc.loadRemoteConfig()
    assert kc.deleteIngressYamlFiles() == True

def test_deleteServiceYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_service"])
    kc.setUserName(testData["userName"])
    assert kc.deleteServiceYamlFiles() == True

def test_deleteAuthenticationYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_authentication"])
    kc.setUserName(testData["userName"])
    assert kc.deleteAuthenticationYamlFiles() == True




if __name__ == "__main__":
    fullUncryptedFilePath = f"./app_controllers/secrets/"
    unencryptedFileName = "kubernetesConfig.yml"
    encryptedFileName = f"{unencryptedFileName}.enc"
    # fileCreated = path.exists(f"{fullUncryptedFilePath}{unencryptedFileName}")
    # inputF = "y".encode("utf-8")
    # output = subprocess.Popen([f"echo 'yes' | travis encrypt-file {fullUncryptedFilePath}{unencryptedFileName}"],shell=True).wait()
    
    # p = subprocess.run(['travis', 'encrypt-file', '-p', './app_controllers/secrets/kubernetesConfig.yml'] ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=inputF)
    # print("OUTPUT:",p.stdout.decode('utf-8'))
    # p = subprocess.run(["echo 'hello world!'"], shell=True, capture_output=True)

    # out = subprocess.run("echo 'yes' |travis encrypt-file ./app_controllers/secrets/kubernetesConfig.yml", shell=True, text=True, capture_output=True)
    # print("OUTPUT:",out.stdout, out.stderr)

    process = subprocess.Popen([f"echo 'yes' | travis encrypt-file -f ./app_controllers/secrets/kubernetesConfig.yml"],stdout=subprocess.PIPE, shell=True)
    finished = True
    while finished:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            finished = True
        if "openssl" in output.strip().decode("utf-8"):
            decryptCommand = str(output.strip().decode("utf-8")).replace("kubernetesConfig.yml.enc","./app_controllers/secrets/kubernetesConfig.yml.enc")
            dep = ""
            with open("./.travis.yml","r") as f:
                dep = yaml.safe_load(f)

            for index, existingCommand in enumerate(dep["matrix"]["include"][0]["before_install"]):
                if "openssl" in str(existingCommand):
                    print("POPPING",index)
                    del dep["matrix"]["include"][0]["before_install"][index]
                # if decryptCommand not in dep["matrix"]["include"][0]["before_install"]:
                #     dep["matrix"]["include"][0]["before_install"].append(decryptCommand)
            # with open("./.travis.yml","w") as f:
            #     yaml.dump(dep, f)
                print(dep["matrix"]["include"][0]["before_install"])
            
            keyEnvironmentVariable = ""
            ivEnvironmentVariable = ""
            keyEnvironmentVariableMatch = re.finditer("((\$encrypted.)(.*\_key))", str(decryptCommand), re.MULTILINE)
            ivEnvironmentVariableMatch1 = re.finditer("(\-iv.)(\$encrypted.)(.*\_iv)", str(decryptCommand), re.MULTILINE)
            for matchNum, match in enumerate(keyEnvironmentVariableMatch, start=1):
                keyEnvironmentVariable = str(match.group())
            for matchNum, match in enumerate(ivEnvironmentVariableMatch1, start=1):
                ivEnvironmentVariable = str(match.group())
            ivEnvironmentVariableMatch2 = re.finditer("(\$encrypted.)(.*\_iv)", str(ivEnvironmentVariable), re.MULTILINE)
            for matchNum, match in enumerate(ivEnvironmentVariableMatch2, start=1):
                ivEnvironmentVariable = str(match.group())
            print(keyEnvironmentVariable,ivEnvironmentVariable)
            finished = False






    # print(output)
    