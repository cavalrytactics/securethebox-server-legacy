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
    "unencryptedFileNames": ["securethebox-service-account.json"],
    "environmentVariablesList": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
    "googleProjectId": "securethebox",
    "googleKubernetesComputeZone": "us-west1-a",
    "googleKubernetesComputeCluster": "us-west1-a",
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

if __name__ == "__main__":
    # createCluster()
    # deleteCluster()
    selectCluster()
    

    