from app_controllers.services.kubernetes_controller import KubernetesController
import os
import time
import subprocess


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
    "googleProjectId": "securethebox-server",
    "googleKubernetesComputeZone": "us-west1-a",
    "googleKubernetesComputeCluster": "test",
    "googleKubernetesComputeRegion": "us-west1",
    "googleServiceAccountEmail": "securethebox-server@securethebox-server.iam.gserviceaccount.com",
    "googleServiceAccountFile": "securethebox-service-account.json",
    "localKubernetesCluster": "docker-desktop",
    "testProdKubernetesCluster": "gke_securethebox_us-west1-a_test",
}

os.environ["APPENV"] = "DEV"
os.environ["SKIPKUBE"] = "YES"

# DELETE POD
def test_manageKubernetesServicePod_delete_gitlab():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName("gitlab")
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesServicePod() == True

def test_manageKubernetesServicePod_delete_securethebox_server():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName("securethebox-server")
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_delete"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesServicePod() == True

# CREATE POD
def test_manageKubernetesServicePod_apply_gitlab():
    for x in range(20):
        time.sleep(1)
        print(x)
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName("gitlab")
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesServicePod() == True

def test_manageKubernetesServicePod_apply_securethebox_server():
    for var in globalData["environmentVariablesList"]:
        kc.setEnvironmentVariable(var)
    kc.setCurrentDirectory()
    kc.setServiceName("securethebox-server")
    kc.setUserName(globalData["userName"])
    kc.setKubectlAction(globalData["kubectlAction_apply"])
    if os.getenv("APPENV") == "DEV":
        kc.setGoogleKubernetesComputeCluster(globalData["localKubernetesCluster"])
    elif os.getenv("APPENV") == "PROD" and os.getenv("KUBESKIP") == "NO":
        kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
    assert kc.manageKubernetesServicePod() == True

# EXECUTE TESTS
def test_pytest():
    for x in range(120):
        time.sleep(1)
        print(x)
    # GET POD ID
    serviceName = "securethebox-server"
    userName = "charles"
    podId = ""
    command = ["kubectl", "get", "pods", "-o", "go-template", "--template",
                "'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    out = subprocess.check_output(command)
    pod_list = out.decode("utf-8").replace('\'', '').splitlines()
    pod_id = ''
    findPod = True
    while findPod:
        for i in pod_list:
            if f'{serviceName}' in str(i) and f'{userName}' in str(i):
                pod_id = str(i)
                findPod = False
                podId = pod_id
    
    # GET CONTAINER ID
    command2 = ["kubectl","describe","pod",podId]
    out2 = subprocess.check_output(command2).split()
    container_id = ''
    for i in out2:
        # print(i)
        if 'docker://' in str(i):
            container_id = i.decode("utf-8").replace('\'','').split("docker://",1)[1]
            print("FOUND CONTAINER_ID:",container_id)

    # EXECUTE PYTEST COMMAND WITHIN CONTAINER
    subprocess.Popen([f"docker exec -it {container_id} ./venv/bin/pytest -vs -x tests/test_services_gitlab_controller.py"], shell=True).wait()