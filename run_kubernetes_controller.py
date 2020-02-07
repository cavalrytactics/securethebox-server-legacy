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
    "serviceName_ingress": "traefik",
    "serviceName_service": "jenkins",
    "serviceName_authentication": "auth",
    "userName": "charles",
    "emailAddress": "jidokaus@gmail.com",
    "kubectlAction_apply": "apply",
    "kubectlAction_delete": "delete",
    "kubernetesPodId": "pod_id_123",
    "unencryptedFileNames": ["securethebox-service-account.json"],
    "environmentVariablesList": ["APPENV","GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
    "googleProjectId": "securethebox",
    "googleKubernetesComputeZone": "us-west1-a",
    "googleKubernetesComputeCluster": "test",
    "googleKubernetesComputeRegion": "us-west1",
    "googleServiceAccountEmail": "kubernetes-sa@securethebox.iam.gserviceaccount.com",
    "googleServiceAccountFile": "securethebox-service-account.json",
    "localKubernetesCluster": "docker-desktop",
}


def test_setCurrentDirectory():
    assert kc.setCurrentDirectory() == True

def test_setFileName():
    for file in testData["unencryptedFileNames"]:
        assert kc.setFileName(file) == True


def createCluster():
    kc.setCurrentDirectory()
    kc.setFileName(testData["googleServiceAccountFile"])
    kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setGoogleKubernetesComputeRegion(testData["googleKubernetesComputeRegion"])
    kc.setGoogleKubernetesComputeZone(testData["googleKubernetesComputeZone"])
    kc.setGoogleProjectId(testData["googleProjectId"])
    kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"])
    kc.createGoogleKubernetesCluster()
 

def deleteCluster():
    kc.setCurrentDirectory()
    kc.setFileName(testData["googleServiceAccountFile"])
    kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setGoogleKubernetesComputeRegion(testData["googleKubernetesComputeRegion"])
    kc.setGoogleKubernetesComputeZone(testData["googleKubernetesComputeZone"])
    kc.setGoogleProjectId(testData["googleProjectId"])
    kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"])
    kc.deleteGoogleKubernetesCluster()

def selectCluster():
    kc.setCurrentDirectory()
    kc.setServiceName(testData["serviceName_ingress"])
    kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setKubectlAction(testData["kubectlAction_apply"])
    kc.createkubernetesManageIngressPod()


def test():
    for var in testData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setGoogleProjectId(testData["googleProjectId"])
    kc.setGoogleKubernetesComputeZone(testData["googleKubernetesComputeZone"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(testData["localKubernetesCluster"])
        assert kc.selectGoogleKubernetesClusterContext() == True
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
        assert kc.selectGoogleKubernetesClusterContext() == True

def t():
    kc.setUserName(testData["userName"])
    kc.setServiceName(testData["serviceName_service"])
    value, podId = kc.getKubernetesPodId()
    kc.setKubernetesPodId(podId)
    value, podStatus = kc.getkubernetesPodStatus()
    print(value,podStatus)


        
if __name__ == "__main__":
    # createCluster()
    # deleteCluster()
    # selectCluster()
    t()
    

    