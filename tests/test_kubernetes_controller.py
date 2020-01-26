from app_controllers.services.kubernetes_controller import KubernetesController

kc = KubernetesController()

readgoogleClientId = open('./app_controllers/secrets/googleClientId.txt','r')
readgoogleClientSecret = open('./app_controllers/secrets/googleClientSecret.txt','r')
googleClientSecret = readgoogleClientSecret.read().rstrip('\n')
googleClientId = readgoogleClientId.read().rstrip('\n')

testData = {
    "clusterName": "us-west1-a",
    "serviceName_ingress": "traefik",
    "serviceName_service": "jenkins",
    "serviceName_authentication": "auth",
    "googleClientId": googleClientId,
    "googleClientSecret": googleClientSecret,
    "userName": "charles",
    "emailAddress": "jidokaus@gmail.com",
    "kubectlAction_apply": "apply",
    "kubectlAction_delete": "delete",
    "dockerePodId": "pod_id_123",
}

def test_setCurrentDirectory():
    assert kc.setCurrentDirectory() == True

def test_setClusterName():
    assert kc.setClusterName(testData["clusterName"]) == True

def test_setServiceName():
    assert kc.setServiceName(testData["serviceName_service"]) == True

def test_setUserName():
    assert kc.setUserName(testData["userName"]) == True

def test_setEmailAddress():
    assert kc.setEmailAddress(testData["emailAddress"]) == True

def test_setGoogleClientId():
    assert kc.setGoogleClientId(testData["googleClientId"]) == True

def test_setGoogleClientSecret():
    assert kc.setGoogleClientSecret(testData["googleClientSecret"]) == True

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
    kc.setGoogleClientId(testData["googleClientId"])
    kc.setGoogleClientSecret(testData["googleClientSecret"])
    assert kc.generateAuthenticationYamlFiles() == True

# def test_loadRemoteConfig():
#     assert kc.loadRemoteConfig() == True

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

def test_deleteIngressYamlFiles():
    kc.setCurrentDirectory()
    kc.setClusterName(testData["clusterName"])
    kc.setServiceName(testData["serviceName_ingress"])
    kc.setUserName(testData["userName"])
    kc.loadRemoteConfig()
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
    assert kc.deleteAuthenticationYamlFiles() == True

