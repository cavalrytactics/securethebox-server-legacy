from app_controllers.services.google_app_engine_controller import GoogleAppEngineController
import os
import time
import json
import pytest

pytest.globalData = []

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

gaec = GoogleAppEngineController()

def test_setCurrentDirectory():
    assert gaec.setCurrentDirectory() == True

def test_setFileName():
    for file in pytest.globalData["unencryptedFileNames"]:
        assert gaec.setFileName(file) == True

def test_setTravisEncryptDecryptFile():
    gaec.setCurrentDirectory()
    for file in pytest.globalData["unencryptedFileNames"]:
        gaec.setFileName(file)
        assert gaec.setTravisEncryptFile() == True
        assert gaec.setTravisUnencryptFile() == True

def test_setGoogleRegion():
    assert gaec.setGoogleRegion(pytest.globalData["googleKubernetesComputeRegion"]) == True

def test_setGoogleServiceAccountEmail():
    assert gaec.setGoogleServiceAccountEmail(pytest.globalData["googleAppEngineServiceAccountEmail"]) == True

def test_loadGoogleServiceAccount():
    gaec.setCurrentDirectory()
    gaec.setFileName(pytest.globalData["googleAppEngineServiceAccountFile"])
    gaec.setGoogleServiceAccountEmail(pytest.globalData["googleAppEngineServiceAccountEmail"])
    assert gaec.loadGoogleServiceAccount() == True

def test_createApp():
    gaec.setCurrentDirectory()
    gaec.setFileName(pytest.globalData["googleAppEngineServiceAccountFile"])
    gaec.setGoogleServiceAccountEmail(pytest.globalData["googleAppEngineServiceAccountEmail"])
    gaec.loadGoogleServiceAccount()
    gaec.createApp()

def test_deployApp():
    gaec.setCurrentDirectory()
    gaec.setFileName(pytest.globalData["googleAppEngineServiceAccountFile"])
    gaec.setGoogleServiceAccountEmail(pytest.globalData["googleAppEngineServiceAccountEmail"])
    gaec.loadGoogleServiceAccount()
    gaec.deployApp()

