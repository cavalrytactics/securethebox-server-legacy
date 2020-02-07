import subprocess
from subprocess import check_output
import time
from ..infrastructure.kubernetes import (
    kubernetesGetPodId
)
from ..infrastructure.docker import (
    dockerGetContainerId
)

class SplunkController():
    def __init__(self):
        self.userName = ""
        self.serviceName = ""
        self.clusterName = ""
        self.containerId = ""

    def splunkUniversalForwarderGenerateConfig(self):
        print("Generating Splunk Config")
        subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/splunk-universal-forwarder/04_configuration.py {self.clusterName} {self.serviceName} {self.userName}"],shell=True).wait()

    def splunkUniversalForwarderDeleteConfig(self):
        print("Deleting Splunk Universal Forwarder Config")
        subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{self.clusterName}-{self.serviceName}-{self.userName}-inputs.conf"],shell=True).wait()
        subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{self.clusterName}-{self.serviceName}-{self.userName}-inputs-2.conf"],shell=True).wait()
        subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{self.clusterName}-{self.serviceName}-{self.userName}-inputs-3.conf"],shell=True).wait()
        # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

    def splunkSetupUserPreferences(self):
        # doc
        # /opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf
        # tz = America/Los_Angeles
        # docker exec -it 0f0b570de296 /bin/sh
        # need to login as admin first
        print("Setting up Splunk User Preferences",self.containerId[:12])
        try:
            subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/splunk/check_login.py"],shell=True).wait()
            # mkdir -p /opt/splunk/etc/users/admin/user-prefs/local/
            subprocess.Popen([f"docker exec -u root "+self.containerId+" mkdir -p /opt/splunk/etc/users/admin/user-prefs/local/"],shell=True).wait()
            subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/user-prefs.conf "+self.containerId[:12]+":/opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf"],shell=True).wait()
            subprocess.Popen([f"docker exec -u root "+self.containerId+" cat /opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf"],shell=True).wait()
            subprocess.Popen([f"docker exec -u root "+self.containerId+" /opt/splunk/bin/splunk restart"],shell=True).wait()
        except:
            print("Trying again...")
            splunkSetupUserPreferences(self.containerId)

        # docker cp ./kubernetes-deployments/services/splunk/user-prefs.conf 24d56f0c7156:/opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf

    def splunkSetupPortForwarding(self):
        pod_id = kubernetesGetPodId("splunk",self.userName)
        subprocess.Popen([f"kubectl port-forward "+pod_id+" 8000:8000"],shell=True).wait()
        # kubectl port-forward splunk-charles-c76dd785b-f6z5l 8000:8000
        # kubectl port-forward wazuh-elasticsearch-0 9200:9200
        # os.spawnl(os.P_DETACH, "kubectl port-forward "+pod_id+" 8000:8000")
        # subprocess.Popen([f"kubectl port-forward "+pod_id+" 8089:8089"],shell=True).wait()

    def splunkSetupAddons(self):
        print("Setting up splunk addons")
        pod_id = kubernetesGetPodId("splunk",self.userName)
        
        # 2. get self.containerId
        self.containerId = dockerGetContainerId(pod_id)
        # 3. Copy inputs
        subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/modsecurity-add-on-for-splunk.tgz "+self.containerId+":/opt/splunk/etc/apps/"],shell=True).wait()
        subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/suricata-add-on-for-splunk.tgz "+self.containerId+":/opt/splunk/etc/apps/"],shell=True).wait()
        subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/wazuh-add-on-for-splunk.tgz "+self.containerId+":/opt/splunk/etc/apps/"],shell=True).wait()
        # Unpack tgz addon
        subprocess.Popen([f"docker exec -u root "+self.containerId+" tar xvzf /opt/splunk/etc/apps/modsecurity-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+self.containerId+" tar xvzf /opt/splunk/etc/apps/suricata-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+self.containerId+" tar xvzf /opt/splunk/etc/apps/wazuh-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
        # Restart splunk service
        subprocess.Popen([f"docker exec -u root "+self.containerId+" /opt/splunk/bin/splunk restart"],shell=True).wait()

    # # Setup Addons
    #     splunkSetupSplunkAddons(self)
    #     # Setup User Preferences
    #     splunkSetupUserPreferences(self.containerId)

    def splunkSetupMasterServer(self):
        print("Setting up Splunk Master Setup")
        # 1. get splunk-universal-forwarder pod_id
        pod_id = kubernetesGetPodId("splunk",self.userName)
        
        # 2. get self.containerId
        self.containerId = dockerGetContainerId(pod_id)
        splunkSetupAddons(self.clusterName,"splunk",self.userName)
        splunkSetupUserPreferences(self.containerId)
        splunkSetupPortForwarding(self.userName)

    def splunkSetupForwarderLogging(self):
        """
        0. enable splunk receving
        1. get splunk-universal-forwarder pod_id
        2. get self.containerId
        3. Run copy inputs over to container
        4. Add Splunk server to forward logs
        5. Restart splunk-universal-forwarder service

        kubectl describe pod splunk-universal-forwarder-oppa-747d54cb-wtlzg
        docker exec -u root 4c35ca0d76dccc84e93896d7c953da8bb119c08fbd4af50dc7842682198a41ef whoami
        """

        splunkUniversalForwarderGenerateConfig(self)
        print("Sleeping 30 Seconds for splunk to get ready")
        time.sleep(30)

        # 1. get splunk-universal-forwarder pod_id
        pod_id = kubernetesGetPodId("splunk-universal-forwarder",self.userName)
        
        # 2. get self.containerId
        self.containerId = dockerGetContainerId(pod_id)
        
        # 3. Copy inputs
        subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk-universal-forwarder/04_{self.clusterName}-{self.serviceName}-{self.userName}-inputs-2.conf "+self.containerId+":/opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()
        # docker cp ./kubernetes-deployments/services/splunk-universal-forwarder/04_us-west1-a-splunk-universal-forwarder-oppa-inputs.conf 482a82302dfbc874d6baae8c12066c6bcc73ba25d8bda506f435ee1f942d96fc:/opt/splunkforwarder/etc/system/local/inputs.conf
        # Check file is copied
        subprocess.Popen([f"docker exec -u root "+self.containerId+" cat /opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()
        # docker exec -u root 482a82302dfbc874d6baae8c12066c6bcc73ba25d8bda506f435ee1f942d96fc cat /opt/splunkforwarder/etc/system/local/inputs.conf
        
        try:
            # 4. point Universal forwarder to splunk server
            # This command should show a FATAL error, its supposed to happend in order for splunk to login
            subprocess.Popen([f"docker exec -u root "+self.containerId+" /opt/splunkforwarder/bin/splunk search 'index=_internal | fields _time | head 1 ' -auth 'admin:Changeme'"],shell=True).wait()
            subprocess.Popen([f"docker exec -u root "+self.containerId+" /opt/splunkforwarder/bin/splunk add forward-server splunk-"+userName+":9997"],shell=True).wait()
            subprocess.Popen([f"docker exec -u root "+self.containerId+" /opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/nginx-"+userName+".log"],shell=True).wait()
            subprocess.Popen([f"docker exec -u root "+self.containerId+" /opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/modsecurity-"+userName+".log"],shell=True).wait()

            # 5. Restart splunk-universal-forwarder service
            subprocess.Popen([f"docker exec -u root "+self.containerId+" /opt/splunkforwarder/bin/splunk restart"],shell=True).wait()
            
            # 6. Clean up inputs files on host
            splunkUniversalForwarderDeleteConfig(self.clusterName,"splunk-universal-forwarder",self.userName)
        except:
            print("Failed to setup Splunk Forwarder... retrying in 10 seconds")
            time.sleep(10)
            splunkSetupForwarderLogging(self)
