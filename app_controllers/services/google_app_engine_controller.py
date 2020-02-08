import subprocess
import json
import os
import subprocess
from subprocess import check_output
from os import path
import yaml
from kubernetes import client, config
import re
import shutil

class GoogleAppEngineController():
    def __init__(self):
        self.podId = ""
        self.currentDirectory = ""
        self.serviceName = ""
        self.userName = ""
        self.fileName = ""
        self.encryptedEnvironmentVariables = {}
        self.googleProjectId = ""
        self.googleCredentials = ""
        self.googleServiceAccountEmail = ""
        self.region = ""

    def setFileName(self, fileName):
        try:
            self.fileName = fileName
            return True
        except:
            return False

    def setTravisEncryptFile(self):
        try:
            fullUncryptedFilePath = f"{self.currentDirectory}/app_controllers/secrets/"
            unencryptedFileName = self.fileName
            encryptedFileName = f"{unencryptedFileName}.enc"
            fileExists = path.exists(
                f"{fullUncryptedFilePath}{unencryptedFileName}")
            encryptedFileExists = path.exists(
                f"{fullUncryptedFilePath}{encryptedFileName}")

            if shutil.which("travis") is None:
                print("Travis command does not exist!")
                return True

            elif fileExists == True:
                process = subprocess.Popen(
                    [f"echo 'yes' | travis encrypt-file --org -f -p ./app_controllers/secrets/{self.fileName}"], stdout=subprocess.PIPE, shell=True)
                finished = True
                keyVariableKEY = ""
                keyVariableVALUE = ""
                ivVariableKEY = ""
                ivVariableVALUE = ""
                decryptCommand = ""
                keyEnvironmentVariable = ""
                ivEnvironmentVariable = ""
                while finished:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        finished = True
                    if "openssl" in output.strip().decode("utf-8"):
                        decryptCommand = str(output.strip().decode("utf-8"))
                        dep = ""
                        with open("./.travis.yml", "r") as f:
                            dep = yaml.safe_load(f)
                            finalDecryptCommand = decryptCommand.replace(
                                f"./app_controllers/secrets/{self.fileName} -d", f"{self.fileName} -d")
                            if finalDecryptCommand not in dep["jobs"]["include"][0]["before_install"]:
                                dep["jobs"]["include"][0]["before_install"].append(
                                    finalDecryptCommand)
                        with open("./.travis.yml", "w") as f:
                            yaml.dump(dep, f)
                        os.rename(f"{self.currentDirectory}/{encryptedFileName}",
                                  f"{self.currentDirectory}/app_controllers/secrets/{encryptedFileName}")
                        keyEnvironmentVariableMatch = re.finditer(
                            "(([$]encrypted.)(.*[_]key))", str(decryptCommand), re.MULTILINE)
                        ivEnvironmentVariableMatch1 = re.finditer(
                            "([-]iv.)([$]encrypted.)(.*[_]iv)", str(decryptCommand), re.MULTILINE)
                        for matchNum, match in enumerate(keyEnvironmentVariableMatch, start=1):
                            keyEnvironmentVariable = str(match.group())
                        for matchNum, match in enumerate(ivEnvironmentVariableMatch1, start=1):
                            ivEnvironmentVariable = str(match.group())
                        ivEnvironmentVariableMatch2 = re.finditer(
                            "([$]encrypted.)(.*[_]iv)", str(ivEnvironmentVariable), re.MULTILINE)
                        for matchNum, match in enumerate(ivEnvironmentVariableMatch2, start=1):
                            ivEnvironmentVariable = str(match.group())
                        setattr(self, keyEnvironmentVariable, "")
                        keyVariableKEY = keyEnvironmentVariable
                        setattr(self, ivEnvironmentVariable, "")
                        ivVariableKEY = ivEnvironmentVariable

                    if "key:" in output.strip().decode("utf-8"):
                        setattr(self, keyVariableKEY,
                                output.strip().decode("utf-8"))
                        self.encryptedEnvironmentVariables[keyVariableKEY] = output.strip().decode(
                            "utf-8").replace("key:", "").strip()

                    if "iv:" in output.strip().decode("utf-8"):
                        setattr(self, ivVariableKEY,
                                output.strip().decode("utf-8"))
                        self.encryptedEnvironmentVariables[ivVariableKEY] = output.strip().decode(
                            "utf-8").replace("iv:", "").strip()
                        return True
            else:
                print("Unencrypted File does not EXIST!",
                      f"{fullUncryptedFilePath}{unencryptedFileName}")
                return True
        except:
            print("You may need to login to Travis")
            return False

    def setTravisUnencryptFile(self):
        try:
            fullencryptedFilePath = f"{self.currentDirectory}/app_controllers/secrets/"
            encryptedFileName = f"{self.fileName}.enc"
            unencryptedFileName = f"{self.fileName}"
            fileCreated = path.exists(
                f"{fullencryptedFilePath}{encryptedFileName}")
            if shutil.which("travis") is None:
                print("Travis command does not exist!")
                return True
            elif fileCreated == True:
                keyVariableKEY = ""
                keyVariableVALUE = ""
                ivVariableKEY = ""
                ivVariableVALUE = ""
                for variable in self.encryptedEnvironmentVariables.keys():
                    if "key" in variable:
                        keyVariableKEY = variable
                        keyVariableVALUE = self.encryptedEnvironmentVariables[variable]
                    elif "iv" in variable:
                        ivVariableKEY = variable
                        ivVariableVALUE = self.encryptedEnvironmentVariables[variable]
                os.chdir(fullencryptedFilePath)
                subprocess.Popen(
                    [f"openssl aes-256-cbc -K {keyVariableVALUE} -iv {ivVariableVALUE} -in {encryptedFileName} -out {unencryptedFileName} -d"], shell=True).wait()
                os.chdir(self.currentDirectory)
                return True
            else:
                print("Encrypted File does not EXIST!",
                      f"{fullUncryptedFilePath}{unencryptedFileName}")
            return True
        except:
            print("You may need to login to Travis")
            return False

    def setCurrentDirectory(self):
        try:
            self.currentDirectory = os.getcwd()
            return True
        except:
            return False

    def setGoogleRegion(self, region):
        try:
            self.region = region
            return True
        except:
            return False

    def setGoogleServiceAccountEmail(self, googleServiceAccountEmail):
        try:
            self.googleServiceAccountEmail = googleServiceAccountEmail
            return True
        except:
            return False

    def loadGoogleServiceAccount(self):
        try:
            subprocess.Popen(
                [f"gcloud auth activate-service-account --key-file {self.currentDirectory}/app_controllers/secrets/{self.fileName} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set account {self.googleServiceAccountEmail} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set compute/region us-west2 >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set compute/zone us-west2-a >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def createApp(self):
        try:
            subprocess.Popen(
                [f"gcloud app create --region=us-west2 --project=securethebox-server"], shell=True).wait()
            return True
        except:
            return False

    def deployApp(self):
        try:
            subprocess.Popen(
                [f"echo y | gcloud app deploy"], shell=True).wait()
            return True
        except:
            return False

    def readAppLogs(self):
        try:
            subprocess.Popen(
                [f"gcloud app logs read"], shell=True).wait()
            return True
        except:
            return False