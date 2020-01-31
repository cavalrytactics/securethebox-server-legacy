from app_controllers.services.kubernetes_controller import KubernetesController
import os
import yaml
import subprocess
from os import path
from subprocess import check_output
import re
import shutil

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
    "environmentVariablesList": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
    "kubernetesDeploymentImage_ingress": "traefik:1.7",
    "kubernetesDeploymentName_ingress": "traefik",
}

def test_setCurrentDirectory():
    assert kc.setCurrentDirectory() == True

def test_setFileName():
    for file in testData["unencryptedFileNames"]:
        assert kc.setFileName(file) == True


def manageIngressPod():
    print("Starting ingress..")
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_ingress"])
    kc.setUserName(testData["userName"])
    kc.setKubectlAction(testData["kubectlAction_apply"])
    kc.generateIngressYamlFiles()
    # kc.kubernetesManageIngressPod()
    # kc.kubernetesCreateIngress()
    # kc.setKubernetesDeploymentImage(testData["kubernetesDeploymentImage_ingress"])
    # kc.setKubernetesDeploymentName(testData["kubernetesDeploymentName_ingress"])
    kc.kubernetesCreateClusterRoleBinding()
    # kc.kubernetesCreateDeployment()
    # kc.getKubernetesApiToken()
    # kc.loadKubernetesConfig()
    # kc.selectKubernetesContext()

if __name__ == "__main__":
    manageIngressPod()

    