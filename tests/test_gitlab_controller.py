from app_controllers.services.gitlab_controller import GitlabController
import os

gc = GitlabController()

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
    assert gc.setCurrentDirectory() == True

def test_setClusterName():
    assert gc.setClusterName(testData["googleKubernetesComputeCluster"]) == True

def test_setServiceName():
    assert gc.setServiceName(testData["serviceName_service"]) == True

def test_setUserName():
    assert gc.setUserName(testData["userName"]) == True

def test_setEmailAddress():
    assert gc.setEmailAddress(testData["emailAddress"]) == True

def test_setEnvironmentVariables():
    for var in testData["environmentVariablesList"]:
        assert gc.setEnvironmentVariable(var) == True
