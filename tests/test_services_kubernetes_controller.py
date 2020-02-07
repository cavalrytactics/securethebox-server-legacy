from app_controllers.services.kubernetes_controller import KubernetesController
import os
import time

kc = KubernetesController()

globalData = {
    "serviceName_ingress": "traefik",
    "serviceName_service": "jenkins",
    "serviceName_dns": "external-dns",
    "serviceName_authentication": "auth",
    "userName": "charles",
    "emailAddress": "jidokaus@gmail.com",
    "kubectlAction_apply": "apply",
    "kubectlAction_delete": "delete",
    "kubernetesPodId": "pod_id_123",
    "unencryptedFileNames": ["securethebox-service-account.json"],
    "environmentVariablesList": ["APPENV","SKIPKUBE","GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
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
    for file in globalData["unencryptedFileNames"]:
        assert kc.setFileName(file) == True

def test_setTravisEncryptDecryptFile():
    kc.setCurrentDirectory()
    for file in globalData["unencryptedFileNames"]:
        kc.setFileName(file)
        assert kc.setTravisEncryptFile() == True
        assert kc.setTravisUnencryptFile() == True

def test_setGoogleKubernetesComputeCluster():
    if os.getenv("APPENV") == "DEV":
        assert kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"]) == True
    elif os.getenv("APPENV") == "PROD":
        assert kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"]) == True

def test_setServiceName():
    assert kc.setServiceName(globalData["serviceName_service"]) == True

def test_setUserName():
    assert kc.setUserName(globalData["userName"]) == True

def test_setEmailAddress():
    assert kc.setEmailAddress(globalData["emailAddress"]) == True

def test_setEnvironmentVariables():
    for var in globalData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var) == True

def test_setKubernetesPodId():
    assert kc.setKubernetesPodId(globalData["kubernetesPodId"]) == True

def test_setKubectlAction():
    assert kc.setKubectlAction(globalData["kubectlAction_apply"]) == True
    assert kc.setKubectlAction(globalData["kubectlAction_delete"]) == True

def test_generateIngressYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(globalData["serviceName_ingress"])
    kc.setUserName(globalData["userName"])
    kc.setEmailAddress(globalData["emailAddress"])
    assert kc.generateIngressYamlFiles() == True

def test_generateServiceYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(globalData["serviceName_service"])
    kc.setUserName(globalData["userName"])
    assert kc.generateServiceYamlFiles() == True

def test_generateAuthenticationYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(globalData["serviceName_authentication"])
    kc.setUserName(globalData["userName"])
    kc.setEmailAddress(globalData["emailAddress"])
    for var in globalData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var) == True
    assert kc.generateAuthenticationYamlFiles() == True

def test_generateDnsYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(globalData["serviceName_dns"])
    kc.setUserName(globalData["userName"])
    kc.setEmailAddress(globalData["emailAddress"])
    for var in globalData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var) == True
    assert kc.generateDnsYamlFiles() == True

def test_generateStorageYamlFiles():
    kc.setCurrentDirectory()
    kc.setUserName(globalData["userName"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.generateStorageYamlFiles() == True

def test_setGoogleProjectId():
    assert kc.setGoogleProjectId(globalData["googleProjectId"]) == True

def test_setGoogleKubernetesComputeZone():
    assert kc.setGoogleKubernetesComputeZone(globalData["googleKubernetesComputeZone"]) == True

def test_setGoogleKubernetesComputeCluster():
    if os.getenv("APPENV") == "DEV":
        assert kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"]) == True
    elif os.getenv("APPENV") == "PROD":
        assert kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"]) == True

def test_setGoogleKubernetesComputeRegion():
    assert kc.setGoogleKubernetesComputeRegion(globalData["googleKubernetesComputeRegion"]) == True

def test_setGoogleServiceAccountEmail():
    assert kc.setGoogleServiceAccountEmail(globalData["googleServiceAccountEmail"]) == True

def test_loadGoogleKubernetesServiceAccount():
    kc.setCurrentDirectory()
    kc.setFileName(globalData["googleServiceAccountFile"])
    kc.setGoogleServiceAccountEmail(globalData["googleServiceAccountEmail"])
    assert kc.loadGoogleKubernetesServiceAccount() == True

def test_createGoogleKubernetesCluster():
    kc.setCurrentDirectory()
    kc.setFileName(globalData["googleServiceAccountFile"])
    kc.setGoogleKubernetesComputeRegion(globalData["googleKubernetesComputeRegion"])
    kc.setGoogleKubernetesComputeZone(globalData["googleKubernetesComputeZone"])
    kc.setGoogleProjectId(globalData["googleProjectId"])
    kc.setGoogleServiceAccountEmail(globalData["googleServiceAccountEmail"])
    if os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
        assert kc.createGoogleKubernetesCluster() == True

def test_getGoogleKubernetesClusterCredentials():
    kc.setCurrentDirectory()
    kc.setFileName(globalData["googleServiceAccountFile"])
    kc.setGoogleServiceAccountEmail(globalData["googleServiceAccountEmail"])
    if os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
        assert kc.getGoogleKubernetesClusterCredentials() == True

def test_selectGoogleKubernetesClusterContext():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setGoogleProjectId(globalData["googleProjectId"])
    kc.setGoogleKubernetesComputeZone(globalData["googleKubernetesComputeZone"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
        assert kc.selectGoogleKubernetesClusterContext() == True
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
        assert kc.getGoogleKubernetesClusterCredentials() == True

def test_manageKubernetesIngressPod_apply():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(globalData["serviceName_ingress"])
    kc.setKubectlAction(globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
        kc.selectGoogleKubernetesClusterContext()
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
        kc.selectGoogleKubernetesClusterContext()
    assert kc.manageKubernetesIngressPod() == True

def test_manageKubernetesStoragePod_apply():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesStoragePod() == True

def test_manageKubernetesAuthenticationPod_apply():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(globalData["serviceName_service"])
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesAuthenticationPod() == True

def test_manageKubernetesDnsPod_apply():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(globalData["serviceName_dns"])
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesDnsPod() == True

def test_manageKubernetesServicePod_apply():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(globalData["serviceName_service"])
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesServicePod() == True

def test_getKubernetesPodId():
    kc.setUserName(globalData["userName"])
    kc.setServiceName(globalData["serviceName_service"])
    value, podId = kc.getKubernetesPodId()
    assert value == True
    assert podId != "0"

def test_getKubernetesPodStatus():
    kc.setUserName(globalData["userName"])
    kc.setServiceName(globalData["serviceName_service"])
    value, podId = kc.getKubernetesPodId()
    kc.setKubernetesPodId(podId)
    value, podStatus = kc.getkubernetesPodStatus()
    assert value == True

def test_manageKubernetesServicePod_delete():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(globalData["serviceName_service"])
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesServicePod() == True

def test_manageKubernetesAuthenticationPod_delete():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(globalData["serviceName_service"])
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesAuthenticationPod() == True

def test_manageKubernetesDnsPod_delete():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(globalData["serviceName_dns"])
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesDnsPod() == True

def test_manageKubernetesStoragePod_delete():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesStoragePod() == True

def test_manageKubernetesIngressPod_delete():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName(globalData["serviceName_ingress"])
    kc.setKubectlAction(globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
        kc.selectGoogleKubernetesClusterContext()
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
        kc.selectGoogleKubernetesClusterContext()
    assert kc.manageKubernetesIngressPod() == True

def test_deleteGoogleKubernetesCluster():
    kc.setCurrentDirectory()
    kc.setFileName(globalData["googleServiceAccountFile"])
    kc.setGoogleKubernetesComputeRegion(globalData["googleKubernetesComputeRegion"])
    kc.setGoogleKubernetesComputeZone(globalData["googleKubernetesComputeZone"])
    kc.setGoogleProjectId(globalData["googleProjectId"])
    kc.setGoogleServiceAccountEmail(globalData["googleServiceAccountEmail"])
    if os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
        kc.selectGoogleKubernetesClusterContext()
        assert kc.deleteGoogleKubernetesCluster() == True

def test_deleteIngressYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(globalData["serviceName_ingress"])
    kc.setUserName(globalData["userName"])
    assert kc.deleteIngressYamlFiles() == True

def test_deleteServiceYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(globalData["serviceName_service"])
    kc.setUserName(globalData["userName"])
    assert kc.deleteServiceYamlFiles() == True

def test_deleteAuthenticationYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(globalData["serviceName_authentication"])
    kc.setUserName(globalData["userName"])
    assert kc.deleteAuthenticationYamlFiles() == True
    
def test_deleteDnsYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setServiceName(globalData["serviceName_dns"])
    kc.setUserName(globalData["userName"])
    assert kc.deleteDnsYamlFiles() == True

def test_deleteStorageYamlFiles():
    kc.setCurrentDirectory()
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    kc.setUserName(globalData["userName"])
    assert kc.deleteStorageYamlFiles() == True