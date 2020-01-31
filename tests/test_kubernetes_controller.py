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
    "dockerePodId": "pod_id_123",
    "unencryptedFileNames": ["securethebox-service-account.json"],
    "environmentVariablesList": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
    "googleProjectId": "cavalrytactics",
    "googleKubernetesComputeZone": "us-west1-a",
    "googleKubernetesComputeCluster": "test",
    "googleServiceAccountEmail": "kubernetes-service-account@cavalrytactics.iam.gserviceaccount.com",
    "googleServiceAccountFile": "securethebox-service-account.json",
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

def test_generateAuthenticationYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_authentication"])
    kc.setUserName(testData["userName"])
    kc.setEmailAddress(testData["emailAddress"])
    for var in testData["environmentVariablesList"]:
        assert kc.setEnvironmentVariable(var)
    assert kc.generateAuthenticationYamlFiles() == True

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

def test_setGoogleProjectId():
    assert kc.setGoogleProjectId(testData["googleProjectId"]) == True

def test_setGoogleKubernetesComputeZone():
    assert kc.setGoogleKubernetesComputeZone(testData["googleKubernetesComputeZone"]) == True

def test_setGoogleKubernetesComputeCluster():
    assert kc.setGoogleKubernetesComputeCluster(testData["googleKubernetesComputeCluster"]) == True

def test_setGoogleServiceAccountEmail():
    assert kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"]) == True

def test_loadGoogleKubernetesServiceAccount():
    kc.setCurrentDirectory()
    kc.setFileName(testData["googleServiceAccountFile"])
    kc.setGoogleServiceAccountEmail(testData["googleServiceAccountEmail"])
    assert kc.loadGoogleKubernetesServiceAccount() == True

# def test_getKubernetesApiToken():
#     assert kc.getKubernetesApiToken() == True

# def test_loadKubernetesConfig():
#     kc.getKubernetesApiToken()
#     assert kc.loadKubernetesConfig() == True

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
