import subprocess
from subprocess import check_output
import time
import os 
from ..services.gitlab import (
    gitlabGetResetPasswordToken, 
    gitlabPostResetPassword,
    gitlabCreatePersonalAccessToken,
    gitlabCreateProject,
    gitlabMakeProjectPublic,
    gitlabProjectAddDeployKey,
    gitlabProjectAddWebhook,
    gitlabProjectAllowOutbound
)
from ..services.jenkins import (
    jenkinsConnectGitlab,
    jenkinsCreateJob,
    jenkinsCredentialsAddSSHPrivateKey,
    jenkinsInstallPlugin,
    jenkinsRestartServer,
    jenkinsAddShellCommand
)
from ..infrastructure.docker import (
    dockerGetContainerId,
    dockerCreateSSHKeypair,
    dockerGetSSHPublicKey,
    dockerGetSSHPrivateKey
)
from ..infrastructure.kubernetes import (
    kubernetesGetPodId,
    kubernetesGetPodStatus,
    kubernetesGenerateIngressYaml,
    kubernetesGenerateAuthenticationYaml,
    kubernetesManageAuthenticationPod,
    kubernetesDeleteAuthenticationYaml,
    kubernetesGeneratePodsYaml,
    kubernetesGenerateServicesYaml,
    kubernetesDeleteIngressYaml,
    kubernetesDeleteServicesYaml,
    kubernetesManageIngressPod,
    kubernetesCreatePersistentVolumes,
    kubernetesManagePods,
    kubernetesManageServicesPod,   
)
from ..services.nginx import (
    nginxGenerateConfig,   
)
from ..services.modsecurity import (
    modsecuritySetup
)
from ..services.splunk import (
    splunkUniversalForwarderGenerateConfig,
    splunkUniversalForwarderDeleteConfig,
    splunkSetupUserPreferences,
    splunkSetupMasterServer,
    splunkSetupPortForwarding,
    splunkSetupAddons,
    splunkSetupForwarderLogging,
)
from ..red_team.attacker_kali_linux import (
    attackerSetupKaliLinux
)
from ..utilities.utilities_cloudcmd import (
    utilitiesSetupCloudcmd
)

import requests
import json 

import google.auth
from google.auth.transport.requests import AuthorizedSession
import google.oauth2.credentials
from google.oauth2 import service_account
from google.auth import impersonated_credentials
import google.auth.crypt
import google.auth.jwt
import time
import os

googleClientId = os.getenv("GOOGLE_CLIENT_ID")
googleClientSecret = os.getenv("GOOGLE_CLIENT_SECRET")

def generate_jwt(sa_keyfile='./app_controllers/secrets/serviceAccount.json',
                 sa_email='service-account@securethebox.iam.gserviceaccount.com',
                 audience='https://www.googleapis.com/oauth2/v4/token',
                 expiry_length=3600):

    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        'iss': sa_email,
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        'aud':  audience,
        # sub and email should match the service account's email address
        'sub': sa_email,
        'email': sa_email
    }

    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)

    return jwt


def checkStatus(serviceName, userName, clusterName):
    print("Checking status....")
    serviceStatus = True
    while serviceStatus:
        time.sleep(1)
        if serviceName == 'traefik':
            credentials = service_account.Credentials.from_service_account_file('./app_controllers/secrets/serviceAccount.json')
            # scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email'])
            target_credentials = impersonated_credentials.Credentials(
                source_credentials=credentials,
                target_principal='service-account@securethebox.iam.gserviceaccount.com',
                target_scopes = ['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email'],
                lifetime=3600)
            # subject_credentials = credentials.with_subject('service-status@securethebox.iam.gserviceaccount.com')
            # print("CREDENTIALS:",subject_credentials)
            authed_session = AuthorizedSession(target_credentials)
            print("AUTHORIZED:", authed_session)
            print("URL:",'http://'+str(serviceName)+'.'+str(clusterName)+'.securethebox.us:8080/')
            response = authed_session.get(
                'http://'+str(serviceName)+'.'+str(clusterName)+'.securethebox.us:8080/')
            # print("RESPONSE:",response.text)
            # signed_jwt = generate_jwt(audience='http://'+str(serviceName)+'.'+str(clusterName)+'.securethebox.us:8080/')
            # print(signed_jwt)
            # headers = {
            #     'Authorization': 'Bearer {}'.format(signed_jwt.decode('utf-8')),
            #     'content-type': 'application/json'
            # }
            # response = requests.get('http://'+str(serviceName)+'.'+str(clusterName)+'.securethebox.us:8080/', headers=headers, allow_redirects=True)
            # response.raise_for_status()
            # print("RESPONSE:",response.url)
            if response.status_code == 200:
                serviceStatus = False
                print(response.status_code,"out of loop")
                pass
        else:
            credentials = service_account.Credentials.from_service_account_file('./app_controllers/secrets/serviceAccount.json')
            # scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email'])
            target_credentials = impersonated_credentials.Credentials(
                source_credentials=credentials,
                target_principal='service-account@securethebox.iam.gserviceaccount.com',
                target_scopes = ['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email'],
                lifetime=3600)
            # print("CREDENTIALS:",target_credentials)
            authed_session = AuthorizedSession(target_credentials)
            print("AUTHORIZED:", authed_session)
            print("URL:",'http://'+str(serviceName)+'-'+str(userName)+'.'+str(clusterName)+'.securethebox.us/')
            response = authed_session.request("GET",
                'http://'+str(serviceName)+'-'+str(userName)+'.'+str(clusterName)+'.securethebox.us/')
            # print("RESPONSE:",response.text)
            # signed_jwt = generate_jwt(audience='http://'+str(serviceName)+'-'+str(userName)+'.'+str(clusterName)+'.securethebox.us/')
            # print(signed_jwt)
            # headers = {
            #     'Authorization': 'Bearer {}'.format(signed_jwt.decode('utf-8')),
            #     'content-type': 'application/json'
            # }
            # response = requests.get('http://'+str(serviceName)+'-'+str(userName)+'.'+str(clusterName)+'.securethebox.us/', headers=headers, allow_redirects=True)
            # response.raise_for_status()
            # print("RESPONSE:",response.url)
            if response.status_code == 200:
                serviceStatus = False
                print(response.status_code,"out of loop")
                pass
        

def checkStatusDocker(serviceName, userName, clusterName):
    serviceStatus = True
    while serviceStatus:
        time.sleep(1)
        print("CHECKING STATUS", serviceName)
        try:
            if serviceName == 'traefik':
                time.sleep(10)
                serviceStatus = False
                pass
            else:
                pod_id = kubernetesGetPodId(serviceName,userName)
                container_id = dockerGetContainerId(pod_id)
                status = dockerCurlStatus(container_id, serviceName)
                if status == True:
                    print("SERVICE IS UP",serviceName)
                    serviceStatus = False
                    pass
        except:
            print("Pod not up yet...")

def challengesManageChallenge1(clusterName, userName, action, emailAddress):
    print(action,"Challenge 1",clusterName,userName)
    currentPath  = os.getcwd()
    if action == 'apply':
        try:
            # print("cwd:",os.getcwd())
            print("cwd:",os.getcwd())
            start = time.time()
            # 1. Generate Yaml Ingress Files
            kubernetesGenerateIngressYaml(clusterName, 'traefik')
            # 2. Deploy Ingress Pods
            kubernetesManageIngressPod(clusterName, 'traefik', action)
            # 3. Generate Yaml Service Files
            checkStatus("traefik", userName, clusterName)
        
            # AUTH PROXY
            print("Trying authentication proxy")
            print(clusterName, 'auth', userName, emailAddress, googleClientId, googleClientSecret)
            kubernetesGenerateAuthenticationYaml(clusterName, 'auth', userName, emailAddress, googleClientId, googleClientSecret)
            kubernetesManageAuthenticationPod(clusterName,'auth',userName, action)

            # SETUP GITLAB (takes about 100 seconds for gitlab server to start)
            kubernetesGenerateServicesYaml(clusterName, 'gitlab',userName)
            kubernetesManageServicesPod(clusterName,'gitlab',userName, action)
            kubernetesGenerateServicesYaml(clusterName, 'jenkins',userName)
            kubernetesManageServicesPod(clusterName,'jenkins',userName, action)

            # Check that jenkins service is up
            print("Waiting for jenkins service")
            checkStatus("jenkins",userName, clusterName)

            # Check that gitlab service is up
            print("Waiting for gitlab service")
            checkStatus("gitlab",userName, clusterName)
                    
            print("Finished sleeping ...")
            reset_token,session_cookie = gitlabGetResetPasswordToken(clusterName,userName)
            gitlabPostResetPassword(reset_token,session_cookie,clusterName,userName)
            print("Gitlab reset password")
            gitlabCreateProject(clusterName, userName)
            print("Gitlab created project")
            gitlabMakeProjectPublic(clusterName, userName)
            print("Gitlab make project public")
            gitlabProjectAllowOutbound(clusterName, userName)
            print("Gitlab allow outbound")
            gitlabProjectAddWebhook(clusterName, userName)
            print("Gitlab add webhook")

            # # SETUP APP SERVER
            kubernetesGenerateServicesYaml(clusterName, 'juice-shop',userName)
            kubernetesManageServicesPod(clusterName,'juice-shop', userName, action)
        
            # # # SETUP JENKINS
            jenkinsInstallPlugin(clusterName,userName)
            for i in range(60,0,-1):
                time.sleep(1)
                print(i)
                
            api_token = gitlabCreatePersonalAccessToken(userName, clusterName)
            print("Created api Token", api_token)

            jenkinsConnectGitlab(api_token,clusterName,userName)
            for i in range(60,0,-1):
                time.sleep(1)
                print(i)
            print("Jenkins should be connected to Gitlab")
            jenkinsRestartServer(clusterName,userName)
            checkStatus("jenkins", userName, clusterName)
            print("Jenkins server finished restarting")
            
            jenkins_pod_id = kgl = gitlab.Gitlab('http://10.0.0.1', private_token='JVNSESs8EwWRx5yDxM5q')


            juiceshop_pod_id = kubernetesGetPodId('juice-shop',userName)
            juiceshop_container_id = dockerGetContainerId(juiceshop_pod_id)

            print("Jenkins Pod Id",jenkins_pod_id)
            print("Jenkins Container Id",jenkins_container_id)

            print("Juice-Shop Pod Id",juiceshop_pod_id)
            print("Juice-Shop Container Id",juiceshop_container_id)

            dockerCreateSSHKeypair(jenkins_container_id)
            print("Created Jenkins SSH Keypair")
            dockerGetSSHPublicKey(jenkins_container_id)
            jenkins_sshPrivateKey = dockerGetSSHPrivateKey(jenkins_container_id)
            print("Jenkins SSH Private Key", jenkins_sshPrivateKey)
            jenkins_sshPublicKey = dockerGetSSHPublicKey(jenkins_container_id)
            print("Jenkins SSH Public Key", jenkins_sshPublicKey)
            jenkinsCreateJob(userName, clusterName)
            jenkinsCredentialsAddSSHPrivateKey(userName,clusterName,jenkins_sshPrivateKey)
            jenkinsAddShellCommand(userName,clusterName,juiceshop_container_id)
            print("Created Jenkins Job")
            gitlabProjectAddDeployKey(jenkins_sshPublicKey,clusterName,userName)
            print("Gitlab Added Deploy Key")
            kubernetesGenerateServicesYaml(clusterName, 'nginx-modsecurity',userName)
            
            # kubernetesGenerateServicesYaml(clusterName, 'splunk',userName)
            # kubernetesGenerateServicesYaml(clusterName, 'splunk-universal-forwarder',userName)
            
            # kubernetesGeneratePodsYaml(clusterName, 'kali-linux',userName)
            # 4. Deploy Service pods
            kubernetesManageServicesPod(clusterName,'nginx-modsecurity', userName, action)
            
            # kubernetesManageServicesPod(clusterName,'splunk', userName, action)
            # kubernetesManageServicesPod(clusterName,'splunk-universal-forwarder',userName, action)
            
            # kubernetesManagePods(clusterName,'kali-linux',userName, action)
            # kubernetesManageServicesPod(clusterName,'wireshark',userName, action)

            print("WAF setup")
            modsecuritySetup(clusterName, 'juice-shop', userName)
            
            # print("Splunk Universal Forwarder Setup")
            # splunkSetupForwarderLogging(clusterName, 'splunk-universal-forwarder', userName)

            # Setup Cloudcmd
            print("Cloudcmd Setup")
            nginx_modsecurity_pod_id = kubernetesGetPodId('nginx-modsecurity',userName)
            nginx_modsecurity_container_id = dockerGetContainerId(nginx_modsecurity_pod_id)
            utilitiesSetupCloudcmd(clusterName, 'nginx-modsecurity', userName, nginx_modsecurity_container_id)

            juice_shop_pod_id = kubernetesGetPodId('juice-shop',userName)
            juice_shop_container_id = dockerGetContainerId(juice_shop_pod_id)
            utilitiesSetupCloudcmd(clusterName, 'juice-shop', userName, juice_shop_container_id)

            # Setup Attacker
            # setupAttacker(clusterName,'kali-linux',userName)

            # Setup Port Forwarding
            # splunkSetupMasterServer(clusterName,userName)

            print("EVERYTHING SHOULD BE DONE!")
            # os.chdir(currentPath)
        except:
            os.chdir(currentPath)
        

    elif action == 'delete':
        # 1. Delete Ingress Pods
        kubernetesManageIngressPod(clusterName,'traefik', action)
        # 2. Generate Yaml Ingress Files
        kubernetesDeleteIngressYaml(clusterName,'traefik')
        # 3. Delete Service Pod2s
        kubernetesManageServicesPod(clusterName, 'nginx-modsecurity',userName, action)
        kubernetesManageServicesPod(clusterName, 'juice-shop', userName, action)
        kubernetesManageServicesPod(clusterName, 'splunk', userName, action)
        kubernetesManageServicesPod(clusterName, 'splunk-universal-forwarder', userName, action)
        kubernetesManageServicesPod(clusterName, 'jenkins', userName, action)
        kubernetesManageServicesPod(clusterName, 'gitlab', userName, action)

        kubernetesManageAuthenticationPod(clusterName, 'auth', userName, action)

        # 4. Delete Yaml Files
        kubernetesDeleteServicesYaml(clusterName, 'nginx-modsecurity',userName)
        kubernetesDeleteServicesYaml(clusterName, 'juice-shop',userName)
        kubernetesDeleteServicesYaml(clusterName, 'splunk',userName)
        kubernetesDeleteServicesYaml(clusterName, 'splunk-universal-forwarder',userName)
        kubernetesDeleteServicesYaml(clusterName, 'jenkins',userName)
        kubernetesDeleteServicesYaml(clusterName, 'gitlab',userName)

        kubernetesDeleteAuthenticationYaml(clusterName, 'auth',userName)
        
        # 5. Delete Persist Volumes
        subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True)
        subprocess.Popen([f"kubectl {action} -f ./app_controllers/infrastructure/kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True)
        # 6. Clean up the rest of environment (note this will close everything... do not do this in production)
        subprocess.Popen([f"kubectl delete po,svc,pv,pvc,deployment,configmap,replicaset,serviceaccounts,statefulset,ingress,secrets --all"],shell=True)
        os.chdir(currentPath)
