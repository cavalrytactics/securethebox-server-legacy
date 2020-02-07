from app_controllers.challenges.kubernetes_manager import KubernetesManager
import os

km = KubernetesManager()

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
    "environmentVariablesList": ["APPENV","SKIPKUBE","GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
    "googleProjectId": "securethebox",
    "googleKubernetesComputeZone": "us-west1-a",
    "googleKubernetesComputeCluster": "test",
    "googleKubernetesComputeRegion": "us-west1",
    "googleServiceAccountEmail": "kubernetes-sa@securethebox.iam.gserviceaccount.com",
    "googleServiceAccountFile": "securethebox-service-account.json",
    "localKubernetesCluster": "docker-desktop",
    "testProdKubernetesCluster": "gke_securethebox_us-west1-a_test",
}

def test_setVariables():
    if os.getenv("APPENV") == "DEV":
        assert km.setVariables(globalData["localKubernetesCluster"],globalData["userName"],"apply",globalData["emailAddress"]) == True
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        assert km.setVariables(globalData["testProdKubernetesCluster"],globalData["userName"],"apply",globalData["emailAddress"]) == True
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "YES":
        assert km.setVariables(globalData["testProdKubernetesCluster"],globalData["userName"],"apply",globalData["emailAddress"]) == True

def test_manageKubernetesCluster_apply():
    if os.getenv("APPENV") == "DEV":
        km.setVariables(globalData["localKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        km.setVariables(globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
        assert km.manageKubernetesCluster() == True

def test_manageKubernetesDns_apply():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesDns() == True

def test_manageKubernetesIngress_apply():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesIngress() == True

def test_manageKubernetesStorage_apply():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesStorage() == True

def test_manageKubernetesAuthentication_apply():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesAuthentication() == True

def test_manageKubernetesServices_apply():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesServices() == True

def test_manageKubernetesServices_delete():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesServices() == True

def test_manageKubernetesAuthentication_delete():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesAuthentication() == True
    
def test_manageKubernetesStorage_delete():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesStorage() == True

def test_manageKubernetesIngress_delete():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesIngress() == True

def test_manageKubernetesDns_delete():
    km.setVariables(globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesDns() == True

def test_manageKubernetesCluster_delete():
    if os.getenv("APPENV") == "DEV":
        km.setVariables(globalData["localKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        km.setVariables(globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
        assert km.manageKubernetesCluster() == True