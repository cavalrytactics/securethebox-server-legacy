from app_controllers.services.kubernetes_controller import KubernetesController
import os
import time
import json
import pytest

pytest.globalData = []

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

kc = KubernetesController()

def test_setCurrentDirectory():
    assert kc.setCurrentDirectory() == True

def test_setFileName():
    for file in pytest.globalData["unencryptedFileNames"]:
        assert kc.setFileName(file) == True

def test_setTravisEncryptDecryptFile():
    kc.setCurrentDirectory()
    for file in pytest.globalData["unencryptedFileNames"]:
        kc.setFileName(file)
        assert kc.setTravisEncryptFile() == True
        assert kc.setTravisUnencryptFile() == True

def test_setGoogleKubernetesComputeCluster():
    if os.getenv("APPENV") == "DEV":
        assert kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"]) == True
    elif os.getenv("APPENV") == "PROD":
        assert kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"]) == True

def test_setServiceName():
    assert kc.setServiceName(pytest.globalData["serviceName_service"]) == True

def test_setUserName():
    assert kc.setUserName(pytest.globalData["userName"]) == True

def test_setEmailAddress():
    assert kc.setEmailAddress(pytest.globalData["emailAddress"]) == True

def test_setEnvironmentVariables():
    for var in pytest.globalData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var) == True

def test_setKubernetesPodId():
    assert kc.setKubernetesPodId(pytest.globalData["kubernetesPodId"]) == True

def test_setKubectlAction():
    assert kc.setKubectlAction(pytest.globalData["kubectlAction_apply"]) == True
    assert kc.setKubectlAction(pytest.globalData["kubectlAction_delete"]) == True

def test_generateIngressYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(pytest.globalData["serviceName_ingress"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setEmailAddress(pytest.globalData["emailAddress"])
    assert kc.generateIngressYamlFiles() == True

def test_generateServiceYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(pytest.globalData["serviceName_service"])
    kc.setUserName(pytest.globalData["userName"])
    assert kc.generateServiceYamlFiles() == True

def test_generateAuthenticationYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(pytest.globalData["serviceName_authentication"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setEmailAddress(pytest.globalData["emailAddress"])
    for var in pytest.globalData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var) == True
    assert kc.generateAuthenticationYamlFiles() == True

def test_generateDnsYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(pytest.globalData["serviceName_dns"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setEmailAddress(pytest.globalData["emailAddress"])
    for var in pytest.globalData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var) == True
    assert kc.generateDnsYamlFiles() == True

def test_generateStorageYamlFiles():
    kc.setCurrentDirectory()
    kc.setUserName(pytest.globalData["userName"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.generateStorageYamlFiles() == True

def test_setGoogleProjectId():
    assert kc.setGoogleProjectId(pytest.globalData["googleProjectId"]) == True

def test_setGoogleKubernetesComputeZone():
    assert kc.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"]) == True

def test_setGoogleKubernetesComputeCluster():
    if os.getenv("APPENV") == "DEV":
        assert kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"]) == True
    elif os.getenv("APPENV") == "PROD":
        assert kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"]) == True

def test_setGoogleKubernetesComputeRegion():
    assert kc.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"]) == True

def test_setGoogleServiceAccountEmail():
    assert kc.setGoogleServiceAccountEmail(pytest.globalData["googleServiceAccountEmail"]) == True

def test_loadGoogleKubernetesServiceAccount():
    kc.setCurrentDirectory()
    kc.setFileName(pytest.globalData["googleServiceAccountFile"])
    kc.setGoogleServiceAccountEmail(pytest.globalData["googleServiceAccountEmail"])
    assert kc.loadGoogleKubernetesServiceAccount() == True

def test_createGoogleKubernetesCluster():
    kc.setCurrentDirectory()
    kc.setFileName(pytest.globalData["googleServiceAccountFile"])
    kc.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    kc.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    kc.setGoogleProjectId(pytest.globalData["googleProjectId"])
    kc.setGoogleServiceAccountEmail(pytest.globalData["googleServiceAccountEmail"])
    if os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        assert kc.createGoogleKubernetesCluster() == True

def test_getGoogleKubernetesClusterCredentials():
    kc.setCurrentDirectory()
    kc.setFileName(pytest.globalData["googleServiceAccountFile"])
    kc.setGoogleServiceAccountEmail(pytest.globalData["googleServiceAccountEmail"])
    if os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        assert kc.getGoogleKubernetesClusterCredentials() == True

def test_selectGoogleKubernetesClusterContext():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setGoogleProjectId(pytest.globalData["googleProjectId"])
    kc.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
        assert kc.selectGoogleKubernetesClusterContext() == True
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        assert kc.getGoogleKubernetesClusterCredentials() == True

def test_manageKubernetesIngressPod_apply():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(pytest.globalData["serviceName_ingress"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
        kc.selectGoogleKubernetesClusterContext()
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        kc.selectGoogleKubernetesClusterContext()
    assert kc.manageKubernetesIngressPod() == True

def test_manageKubernetesStoragePod_apply():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setUserName(pytest.globalData["userName"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesStoragePod() == True

def test_manageKubernetesAuthenticationPod_apply():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(pytest.globalData["serviceName_service"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesAuthenticationPod() == True

def test_manageKubernetesDnsPod_apply():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(pytest.globalData["serviceName_dns"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesDnsPod() == True

def test_manageKubernetesServicePod_apply():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(pytest.globalData["serviceName_service"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesServicePod() == True

def test_getKubernetesPodId():
    kc.setUserName(pytest.globalData["userName"])
    kc.setServiceName(pytest.globalData["serviceName_service"])
    value, podId = kc.getKubernetesPodId()
    assert value == True
    assert podId != "0"

def test_getKubernetesPodStatus():
    kc.setUserName(pytest.globalData["userName"])
    kc.setServiceName(pytest.globalData["serviceName_service"])
    value, podId = kc.getKubernetesPodId()
    kc.setKubernetesPodId(podId)
    value, podStatus = kc.getkubernetesPodStatus()
    assert value == True

def test_manageKubernetesServicePod_delete():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(pytest.globalData["serviceName_service"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesServicePod() == True

def test_manageKubernetesAuthenticationPod_delete():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(pytest.globalData["serviceName_service"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesAuthenticationPod() == True

def test_manageKubernetesDnsPod_delete():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(pytest.globalData["serviceName_dns"])
    kc.setUserName(pytest.globalData["userName"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesDnsPod() == True

def test_manageKubernetesStoragePod_delete():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setUserName(pytest.globalData["userName"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesStoragePod() == True

def test_manageKubernetesIngressPod_delete():
    for var in pytest.globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(pytest.globalData["serviceName_ingress"])
    kc.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
        kc.selectGoogleKubernetesClusterContext()
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        kc.selectGoogleKubernetesClusterContext()
    assert kc.manageKubernetesIngressPod() == True

def test_deleteGoogleKubernetesCluster():
    kc.setCurrentDirectory()
    kc.setFileName(pytest.globalData["googleServiceAccountFile"])
    kc.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    kc.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    kc.setGoogleProjectId(pytest.globalData["googleProjectId"])
    kc.setGoogleServiceAccountEmail(pytest.globalData["googleServiceAccountEmail"])
    if os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        kc.selectGoogleKubernetesClusterContext()
        assert kc.deleteGoogleKubernetesCluster() == True

def test_deleteIngressYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(pytest.globalData["serviceName_ingress"])
    kc.setUserName(pytest.globalData["userName"])
    assert kc.deleteIngressYamlFiles() == True

def test_deleteServiceYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(pytest.globalData["serviceName_service"])
    kc.setUserName(pytest.globalData["userName"])
    assert kc.deleteServiceYamlFiles() == True

def test_deleteAuthenticationYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(pytest.globalData["serviceName_authentication"])
    kc.setUserName(pytest.globalData["userName"])
    assert kc.deleteAuthenticationYamlFiles() == True
    
def test_deleteDnsYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(pytest.globalData["serviceName_dns"])
    kc.setUserName(pytest.globalData["userName"])
    assert kc.deleteDnsYamlFiles() == True

def test_deleteStorageYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    kc.setUserName(pytest.globalData["userName"])
    assert kc.deleteStorageYamlFiles() == True