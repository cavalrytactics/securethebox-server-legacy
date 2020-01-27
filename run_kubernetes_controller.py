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


def setTravisEncryptDecryptFile():
    kc.setCurrentDirectory()
    for file in testData["unencryptedFileNames"]:
        kc.setFileName(file)
        print("Encrypting",file)
        kc.setTravisEncryptFile()

if __name__ == "__main__":
    setTravisEncryptDecryptFile()
    