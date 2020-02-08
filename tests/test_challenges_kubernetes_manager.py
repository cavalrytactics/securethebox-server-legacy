from app_controllers.challenges.kubernetes_manager import KubernetesManager
import os
import json
import pytest

pytest.globalData = []

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

km = KubernetesManager()

def test_setVariables():
    if os.getenv("APPENV") == "DEV":
        assert km.setVariables(pytest.globalData["localKubernetesCluster"],pytest.globalData["userName"],"apply",pytest.globalData["emailAddress"]) == True
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        assert km.setVariables(pytest.globalData["testProdKubernetesCluster"],pytest.globalData["userName"],"apply",pytest.globalData["emailAddress"]) == True
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "YES":
        assert km.setVariables(pytest.globalData["testProdKubernetesCluster"],pytest.globalData["userName"],"apply",pytest.globalData["emailAddress"]) == True

def test_manageKubernetesCluster_apply():
    if os.getenv("APPENV") == "DEV":
        km.setVariables(pytest.globalData["localKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
        assert km.manageKubernetesCluster() == True

def test_manageKubernetesDns_apply():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesDns() == True

def test_manageKubernetesIngress_apply():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesIngress() == True

def test_manageKubernetesStorage_apply():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesStorage() == True

def test_manageKubernetesAuthentication_apply():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesAuthentication() == True

def test_manageKubernetesServices_apply():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    assert km.manageKubernetesServices() == True

def test_manageKubernetesServices_delete():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesServices() == True

def test_manageKubernetesAuthentication_delete():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesAuthentication() == True
    
def test_manageKubernetesStorage_delete():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesStorage() == True

def test_manageKubernetesIngress_delete():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesIngress() == True

def test_manageKubernetesDns_delete():
    km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
    assert km.manageKubernetesDns() == True

def test_manageKubernetesCluster_delete():
    if os.getenv("APPENV") == "DEV":
        km.setVariables(pytest.globalData["localKubernetesCluster"],"charles","apply","jidokaus@gmail.com")
    elif os.getenv("APPENV") == "PROD" and os.getenv("SKIPKUBE") == "NO":
        km.setVariables(pytest.globalData["testProdKubernetesCluster"],"charles","delete","jidokaus@gmail.com")
        assert km.manageKubernetesCluster() == True