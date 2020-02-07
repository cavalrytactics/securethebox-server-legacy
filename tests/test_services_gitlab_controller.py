from app_controllers.services.gitlab_controller import GitlabController
import os
import time

gc = GitlabController()

globalData = {
    "serviceName_ingress": "traefik",
    "serviceName_service": "jenkins",
    "serviceName_authentication": "auth",
    "userName": "charles",
    "emailAddress": "jidokaus@gmail.com",
    "kubectlAction_apply": "apply",
    "kubectlAction_delete": "delete",
    "kubernetesPodId": "pod_id_123",
    "unencryptedFileNames": ["securethebox-service-account.json"],
    "environmentVariablesList": ["APPENV", "SKIPKUBE", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
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
    assert gc.setClusterName(globalData["localKubernetesCluster"]) == True


def test_setServiceName():
    assert gc.setServiceName("gitlab") == True


def test_setUserName():
    assert gc.setUserName(globalData["userName"]) == True


def test_setEmailAddress():
    assert gc.setEmailAddress(globalData["emailAddress"]) == True


# def test_checkStatus():
#     # gc.setServerURL("http://gitlab-charles.docker-desktop.securethebox.us")
#     gc.setUserName("charles")
#     assert gc.checkStatus() == True

# def test_getResetPasswordToken():
#     gc.setUserName(globalData["userName"])
#     assert gc.getResetPasswordToken() == True


def test_setResetPassword():
    # gc.setServerURL("http://gitlab-charles.docker-desktop.securethebox.us")
    gc.setUserName(globalData["userName"])
    gc.getResetPasswordToken()
    assert gc.setResetPassword() == True


def test_createProject():
    # gc.setServerURL("http://gitlab-charles.docker-desktop.securethebox.us")
    gc.setUserName(globalData["userName"])
    assert gc.createProject() == True


def test_createPersonalAccessToken():
    # gc.setServerURL("http://gitlab-charles.docker-desktop.securethebox.us")
    gc.setUserName(globalData["userName"])
    assert gc.createPersonalAccessToken() == True


def test_setProjectPublic():
    # gc.setServerURL("http://gitlab-charles.docker-desktop.securethebox.us")
    gc.setUserName(globalData["userName"])
    assert gc.setProjectPublic() == True


def test_setProjectAllowOutbound():
    # gc.setServerURL("http://gitlab-charles.docker-desktop.securethebox.us")
    gc.setUserName(globalData["userName"])
    assert gc.setProjectAllowOutbound() == True

# def test_addProjectDeployKey():
#     gc.setUserName(globalData["userName"])
#     assert gc.addProjectDeployKey() == True


def test_addProjectWebhookDisableSSL():
    # gc.setServerURL("http://gitlab-charles.docker-desktop.securethebox.us")
    gc.setUserName(globalData["userName"])
    assert gc.addProjectWebhookDisableSSL() == True
