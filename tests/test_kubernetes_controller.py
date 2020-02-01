from app_controllers.services.kubernetes_controller import KubernetesController
import os

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

def test_setTravisEncryptDecryptFile():
    kc.setCurrentDirectory()
    for file in testData["unencryptedFileNames"]:
        kc.setFileName(file)
        assert kc.setTravisEncryptFile() == True
        assert kc.setTravisUnencryptFile() == True

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

def test_setKubernetesPodId():
    assert kc.setKubernetesPodId(testData["kubernetesPodId"]) == True

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

def test_generateAuthenticationYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_authentication"])
    kc.setUserName(testData["userName"])
    kc.setEmailAddress(testData["emailAddress"])
    for var in testData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var) == True
    assert kc.generateAuthenticationYamlFiles() == True

def test_generateStorageYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setUserName(testData["userName"])
    assert kc.generateStorageYamlFiles() == True

def test_setGoogleProjectId():
    assert kc.setGoogleProjectId(testData["googleProjectId"]) == True

def test_setGoogleKubernetesComputeZone():
    assert kc.setGoogleKubernetesComputeZone(testData["googleKubernetesComputeZone"]) == True

def test_setGoogleKubernetesComputeCluster():
    assert kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"]) == True

def test_setGoogleKubernetesComputeRegion():
    assert kc.setGoogleKubernetesComputeRegion(testData["googleKubernetesComputeRegion"]) == True

def test_setGoogleServiceAccountEmail():
    assert kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"]) == True

def test_loadGoogleKubernetesServiceAccount():
    kc.setCurrentDirectory()
    kc.setFileName(testData["googleServiceAccountFile"])
    kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"])
    assert kc.loadGoogleKubernetesServiceAccount() == True


# def test_createGoogleKubernetesCluster():
#     kc.setCurrentDirectory()
#     kc.setFileName(testData["googleServiceAccountFile"])
#     kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
#     kc.setGoogleKubernetesComputeRegion(testData["googleKubernetesComputeRegion"])
#     kc.setGoogleKubernetesComputeZone(testData["googleKubernetesComputeZone"])
#     kc.setGoogleProjectId(testData["googleProjectId"])
#     kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"])
#     assert kc.createGoogleKubernetesCluster() == True

# def test_getGoogleKubernetesClusterCredentials():
#     kc.setCurrentDirectory()
#     kc.setFileName(testData["googleServiceAccountFile"])
#     kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
#     kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"])
#     kc.getGoogleKubernetesClusterCredentials() == True

def test_selectGogoleKubernetesClusterContext():
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(testData["localKubernetesCluster"])
        assert kc.selectGoogleKubernetesClusterContext() == True
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
        assert kc.selectGoogleKubernetesClusterContext() == True

# def test_deleteGoogleKubernetesCluster():
#     kc.setCurrentDirectory()
#     kc.setFileName(testData["googleServiceAccountFile"])
#     kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
#     kc.setGoogleKubernetesComputeRegion(testData["googleKubernetesComputeRegion"])
#     kc.setGoogleKubernetesComputeZone(testData["googleKubernetesComputeZone"])
#     kc.setGoogleProjectId(testData["googleProjectId"])
#     kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"])
#     assert kc.deleteGoogleKubernetesCluster() == True

def test_managekubernetesIngressPod_apply():
    kc.setCurrentDirectory()
    kc.setServiceName(testData["serviceName_ingress"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(testData["localKubernetesCluster"])
        assert kc.selectGoogleKubernetesClusterContext() == True
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setKubectlAction(testData["kubectlAction_apply"])
    assert kc.managekubernetesIngressPod() == True

def test_managekubernetesIngressPod_delete():
    kc.setCurrentDirectory()
    kc.setServiceName(testData["serviceName_ingress"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(testData["localKubernetesCluster"])
        assert kc.selectGoogleKubernetesClusterContext() == True
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setKubectlAction(testData["kubectlAction_delete"])
    assert kc.managekubernetesIngressPod() == True

def test_managekubernetesStoragePod_apply():
    kc.setCurrentDirectory()
    kc.setUserName(testData["userName"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(testData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setKubectlAction(testData["kubectlAction_apply"])
    assert kc.managekubernetesStoragePod() == True

def test_managekubernetesServicePod_apply():
    kc.setCurrentDirectory()
    kc.setServiceName(testData["serviceName_service"])
    kc.setUserName(testData["userName"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(testData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setKubectlAction(testData["kubectlAction_apply"])
    assert kc.managekubernetesServicePod() == True

def test_getKubernetesPodId():
    kc.setUserName(testData["userName"])
    kc.setServiceName(testData["serviceName_service"])
    value, podId = kc.getKubernetesPodId()
    assert value == True
    assert podId != "0"

def test_getKubernetesPodStatus():
    kc.setUserName(testData["userName"])
    kc.setServiceName(testData["serviceName_service"])
    value, podId = kc.getKubernetesPodId()
    kc.setKubernetesPodId(podId)
    value, podStatus = kc.getkubernetesPodStatus()
    assert value == True

def test_managekubernetesServicePod_delete():
    kc.setCurrentDirectory()
    kc.setServiceName(testData["serviceName_service"])
    kc.setUserName(testData["userName"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(testData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setKubectlAction(testData["kubectlAction_delete"])
    assert kc.managekubernetesServicePod() == True

def test_managekubernetesStoragePod_delete():
    kc.setCurrentDirectory()
    kc.setUserName(testData["userName"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(testData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD":
        kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"])
    kc.setKubectlAction(testData["kubectlAction_delete"])
    assert kc.managekubernetesStoragePod() == True

def test_deleteIngressYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_ingress"])
    kc.setUserName(testData["userName"])
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
    for var in testData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var)
    assert kc.deleteAuthenticationYamlFiles() == True
    
def test_deleteStorageYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setUserName(testData["userName"])
    assert kc.deleteStorageYamlFiles() == True