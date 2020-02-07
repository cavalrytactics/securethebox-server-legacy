import subprocess
import os
import requests
from lxml import html
import urllib
import datetime
import time


class GitlabController():
    def __init__(self):
        self.clusterName = ""
        self.serviceName = ""
        self.userName = ""
        self.currentDirectory = ""
        self.gitlabHost = ""
        self.gitlabPrivateToken = ""
        self.passwordToken = ""
        self.sessionCookie = ""
        self.serverURL = "http://gitlab-"+self.userName

    def setServerURL(self, serverURL):
        self.serverURL = serverURL

    def setCurrentDirectory(self):
        try:
            self.currentDirectory = os.getcwd()
            return True
        except:
            return False

    def setClusterName(self, clusterName):
        try:
            self.clusterName = clusterName
            return True
        except:
            return False

    def setServiceName(self, serviceName):
        try:
            self.serviceName = serviceName
            return True
        except:
            return False

    def setUserName(self, userName):
        try:
            self.userName = userName
            return True
        except:
            return False

    def setEmailAddress(self, emailAddress):
        try:
            self.emailAddress = emailAddress
            return True
        except:
            return False

    # def checkStatus(self):
    #     print("trying",self.serverURL)
    #     try:
    #         hostStatus = True
    #         while hostStatus:
    #             print("loops")
    #             try:
    #                 time.sleep(1)
    #                 response = requests.get(self.serverURL)
    #                 print(response.status_code)
    #                 if response.status_code == 302 or response.status_code == 200 or response.status_code == 201:
    #                     print("all good")
    #                     hostStatus = False
    #                     return True
    #             except:
    #                 print("host not up...")
                
    #     except:
    #         print("All false")
    #         return False

    def getResetPasswordToken(self):
        try:
            url = self.serverURL
            headers = {
                'Host': self.serverURL
            }
            response = requests.request(
                "GET", url, headers=headers, allow_redirects=True)
            response_url = response.url
            print(response_url)
            password_token = response_url.split('=')
            session_cookie = response.request.headers['Cookie']
            self.passwordToken = password_token
            self.sessionCookie = session_cookie
            return True
        except:
            return False

    def setResetPassword(self):
        try:
            url = self.serverURL + \
                "/users/password/edit?reset_password_token="+self.passwordToken
            headers = {
                'Host': self.serverURL,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': self.sessionCookie
            }
            page = requests.request("GET", url, headers=headers)
            tree = html.fromstring(page.content)
            authtoken = tree.xpath('//input[@name="authenticity_token"]')
            form_data = {
                "utf8": "✓",
                "_method": "put",
                "authenticity_token": authtoken[0].value,
                "user[reset_password_token]": token,
                "user[password]": "Changeme",
                "user[password_confirmation]": "Changeme",
            }
            submit_url = self.serverURL+"/users/password"
            submitform = requests.request(
                "POST", submit_url, headers=headers, data=form_data)
            return True
        except:
            return False

    def createProject(self):
        try:
            currentPath = self.currentDirectory()
            os.chdir(currentPath+'/app_controllers/repositories')
            subprocess.Popen(
                [f"rm -rf juice-shop-"+self.userName], shell=True).wait()
            subprocess.Popen(
                [f"git clone https://github.com/ncmd/juice-shop.git juice-shop-"+self.userName], shell=True).wait()
            os.chdir(
                currentPath+'/app_controllers/repositories/juice-shop-'+self.userName)
            subprocess.Popen([f"rm -rf .git"], shell=True).wait()
            subprocess.Popen([f"git init"], shell=True).wait()
            subprocess.Popen([f"git add ."], shell=True).wait()
            subprocess.Popen(
                [f"git commit -m 'production app'"], shell=True).wait()
            subprocess.Popen([f"git push --set-upstream http://gitlab-"+self.userName +
                              "/root/juice-shop-"+self.userName+".git master"], shell=True).wait()
            os.chdir(currentPath)
            return True
        except:
            return False

    def createPersonalAccessToken(self):
        try:
            # 1
            url1 = self.serverURL+"/users/sign_in"
            response1 = requests.request("GET", url1)
            session_cookie1 = response1.headers['Set-Cookie'].split(';')
            tree = html.fromstring(response1.content)
            authtoken = tree.xpath('//input[@name="authenticity_token"]')
            new_auth_token = urllib.parse.quote(authtoken[0].value)
            print("1 - new_auth_token", new_auth_token)
            # 2
            url2 = self.serverURL+"/users/sign_in"
            payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token + \
                "&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Host': self.serverURL,
                'Cookie': session_cookie1[0]
            }
            response2 = requests.request(
                "POST", url2, data=payload, headers=headers, allow_redirects=True)
            session_cookie2 = response2.request.headers['Cookie']
            tree2 = html.fromstring(response2.content)
            authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
            print("User authenticity_token2:", authtoken2)
            # 3
            url3 = self.serverURL+"/profile/personal_access_tokens"
            headers3 = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Host': self.serverURL,
                'Cookie': session_cookie2
            }
            response3 = requests.request("GET", url3, headers=headers3)
            session_cookie3 = response3.request.headers['Cookie']
            tree3 = html.fromstring(response3.content)
            authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')

            # 4
            now = datetime.datetime.now()
            year100 = now.year + 100
            print(year100)
            url4 = self.serverURL+"/profile/personal_access_tokens"
            payload = "utf8=%E2%9C%93&authenticity_token="+urllib.parse.quote(authtoken3[0].attrib['content'])+"&personal_access_token%5Bname%5D=jenkins-"+str(self.userName)+"-root&personal_access_token%5Bexpires_at%5D="+str(year100)+"-"+str(now.day)+"-"+str(
                now.month)+"&personal_access_token%5Bscopes%5D%5B%5D=api&personal_access_token%5Bscopes%5D%5B%5D=read_user&personal_access_token%5Bscopes%5D%5B%5D=read_repository&personal_access_token%5Bscopes%5D%5B%5D=write_repository&personal_access_token%5Bscopes%5D%5B%5D=sudo"
            headers4 = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Host': self.serverURL,
                'Cookie': session_cookie3,
                'accept-encoding': "gzip, deflate",
                'Connection': "keep-alive"
            }
            response4 = requests.request(
                "POST", url4, data=payload, headers=headers4, allow_redirects=True)
            print(response4.status_code)

            # 5
            url5 = self.serverURL+"/profile/personal_access_tokens"
            headers5 = {
                'Host': self.serverURL,
                'Cookie': session_cookie3
            }
            response5 = requests.request("GET", url5, headers=headers5)
            tree5 = html.fromstring(response5.content)
            authtoken5 = tree5.xpath(
                '//input[@name="created-personal-access-token"]')
            return True, authtoken5[0].value
        except:
            return False, "0"

    def setProjectPublic(self):
        try:
            url1 = self.serverURL+"/users/sign_in"
            response1 = requests.request("GET", url1)
            session_cookie1 = response1.headers['Set-Cookie'].split(';')
            tree = html.fromstring(response1.content)
            authtoken = tree.xpath('//input[@name="authenticity_token"]')
            new_auth_token = urllib.parse.quote(authtoken[0].value)

            # 2
            url2 = self.serverURL+"/users/sign_in"
            payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token + \
                "&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Host': self.serverURL,
                'Cookie': session_cookie1[0]
            }
            response2 = requests.request(
                "POST", url2, data=payload, headers=headers, allow_redirects=True)
            session_cookie2 = response2.request.headers['Cookie']
            tree2 = html.fromstring(response2.content)
            authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
            print("User authenticity_token2:", authtoken2)

            # 3
            url3 = self.serverURL+"/root/juice-shop-"+self.userName+"/edit"
            headers3 = {
                'Host': self.serverURL,
                'Cookie': session_cookie2
            }
            response3 = requests.request("GET", url3, headers=headers3)
            session_cookie3 = response3.request.headers['Cookie']
            tree3 = html.fromstring(response3.content)
            authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
            print("User csrf-token for personal_access_token page:",
                  authtoken3[0].attrib['content'])

            url4 = self.serverURL+"/root/juice-shop-"+userName
            headers4 = {
                "Cookie": session_cookie3,
                "X-CSRF-Token": authtoken3[0].attrib['content']
            }

            auth_token4 = urllib.parse.quote(authtoken3[0].attrib['content'])
            payload4 = "utf8=%E2%9C%93&_method=patch&authenticity_token="+auth_token4+"&update_section=js-shared-permissions&project%5Bvisibility_level%5D=20&project%5Brequest_access_enabled%5D=true&project%5Bproject_feature_attributes%5D%5Bissues_access_level%5D=20&project%5Bproject_feature_attributes%5D%5Brepository_access_level%5D=20&project%5Bproject_feature_attributes%5D%5Bmerge_requests_access_level%5D=20&project%5Bproject_feature_attributes%5D%5Bbuilds_access_level%5D=20&project%5Blfs_enabled%5D=true&project%5Bproject_feature_attributes%5D%5Bwiki_access_level%5D=20&project%5Bproject_feature_attributes%5D%5Bsnippets_access_level%5D=20&commit=Save+changes"

            response4 = requests.request(
                "POST", url4, headers=headers4, data=payload4)
            print("Response code:", response4.status_code)
            return True
        except:
            return False

    def setProjectAllowOutbound(self):
        try:
            url1 = self.serverURL+"/users/sign_in"
            response1 = requests.request("GET", url1)
            session_cookie1 = response1.headers['Set-Cookie'].split(';')
            tree = html.fromstring(response1.content)
            authtoken = tree.xpath('//input[@name="authenticity_token"]')
            new_auth_token = urllib.parse.quote(authtoken[0].value)

            # 2
            url2 = self.serverURL+"/users/sign_in"
            payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token + \
                "&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Host': self.serverURL,
                'Cookie': session_cookie1[0]
            }
            response2 = requests.request(
                "POST", url2, data=payload, headers=headers, allow_redirects=True)
            session_cookie2 = response2.request.headers['Cookie']
            tree2 = html.fromstring(response2.content)
            authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
            print("User authenticity_token2:", authtoken2)

            # 3
            url3 = self.serverURL+"/admin/application_settings/network"
            headers3 = {
                'Host': self.serverURL,
                'Cookie': session_cookie2
            }
            response3 = requests.request("GET", url3, headers=headers3)
            session_cookie3 = response3.request.headers['Cookie']
            tree3 = html.fromstring(response3.content)
            authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
            print("User csrf-token for personal_access_token page:",
                  authtoken3[0].attrib['content'])

            url4 = self.serverURL+"/admin/application_settings"
            headers4 = {
                "Cookie": session_cookie3,
                "Content-Type": "application/x-www-form-urlencoded"
            }

            auth_token4 = urllib.parse.quote(authtoken3[0].attrib['content'])
            payload4 = "utf8=%E2%9C%93&_method=patch&authenticity_token="+auth_token4 + \
                "&application_setting%5Ballow_local_requests_from_hooks_and_services%5D=0&application_setting%5Ballow_local_requests_from_hooks_and_services%5D=1&application_setting%5Bdns_rebinding_protection_enabled%5D=0&application_setting%5Bdns_rebinding_protection_enabled%5D=0"

            response4 = requests.request(
                "POST", url4, headers=headers4, data=payload4)
            print("Response code:", response4.status_code)
            return True
        except:
            return False

    def addProjectDeployKey(jenkins_public_key):
        try:
            url1 = self.serverURL+"/users/sign_in"
            response1 = requests.request("GET", url1)
            session_cookie1 = response1.headers['Set-Cookie'].split(';')
            tree = html.fromstring(response1.content)
            authtoken = tree.xpath('//input[@name="authenticity_token"]')
            new_auth_token = urllib.parse.quote(authtoken[0].value)

            # 2
            url2 = self.serverURL+"/users/sign_in"
            payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token + \
                "&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Host': self.serverURL,
                'Cookie': session_cookie1[0]
            }
            response2 = requests.request(
                "POST", url2, data=payload, headers=headers, allow_redirects=True)
            session_cookie2 = response2.request.headers['Cookie']
            # print("User Session Cookie2:",session_cookie2)
            tree2 = html.fromstring(response2.content)
            authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
            print("User authenticity_token2:", authtoken2)

            # 3
            url3 = self.serverURL + \
                "/root/juice-shop-"+self.userName+"/settings/repository"
            headers3 = {
                'Host': self.serverURL,
                'Cookie': session_cookie2
            }
            response3 = requests.request("GET", url3, headers=headers3)
            session_cookie3 = response3.request.headers['Cookie']
            tree3 = html.fromstring(response3.content)
            authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
            print("User csrf-token for personal_access_token page:",
                  authtoken3[0].attrib['content'])

            url4 = self.serverURL + \
                "/root/juice-shop-"+self.userName+"/deploy_keys"
            headers4 = {
                "Cookie": session_cookie3,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            auth_token4 = urllib.parse.quote(authtoken3[0].attrib['content'])
            jenkins_public_key_urlencoded = urllib.parse.quote(
                jenkins_public_key)
            payload4 = "utf8=%E2%9C%93&authenticity_token="+auth_token4+"&deploy_key%5Btitle%5D=jenkins-"+self.userName+"-root-public-key\
                &deploy_key%5Bkey%5D="+jenkins_public_key_urlencoded+"\
                &deploy_key%5Bdeploy_keys_projects_attributes%5D%5B0%5D%5Bcan_push%5D=0\
                &deploy_key%5Bdeploy_keys_projects_attributes%5D%5B0%5D%5Bcan_push%5D=1"

            response4 = requests.request(
                "POST", url4, headers=headers4, data=payload4)
            print("Response code:", response4.status_code)
            return True
        except:
            return False

    def addProjectWebhookDisableSSL(self):
        try:
            url1 = self.serverURL+"/users/sign_in"
            response1 = requests.request("GET", url1)
            session_cookie1 = response1.headers['Set-Cookie'].split(';')
            tree = html.fromstring(response1.content)
            authtoken = tree.xpath('//input[@name="authenticity_token"]')
            new_auth_token = urllib.parse.quote(authtoken[0].value)

            # 2
            url2 = self.serverURL+"/users/sign_in"
            payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token + \
                "&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Host': self.serverURL,
                'Cookie': session_cookie1[0]
            }
            response2 = requests.request(
                "POST", url2, data=payload, headers=headers, allow_redirects=True)
            session_cookie2 = response2.request.headers['Cookie']
            tree2 = html.fromstring(response2.content)
            authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')

            # 3
            url3 = self.serverURL+"/root/juice-shop-" + \
                self.userName+"/settings/integrations"
            headers3 = {
                'Host': self.serverURL,
                'Cookie': session_cookie2
            }
            response3 = requests.request("GET", url3, headers=headers3)
            session_cookie3 = response3.request.headers['Cookie']
            tree3 = html.fromstring(response3.content)
            authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
            url4 = self.serverURL+"/root/juice-shop-"+self.userName+"/hooks"
            headers4 = {
                "Cookie": session_cookie3,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            auth_token4 = urllib.parse.quote(authtoken3[0].attrib['content'])
            payload4 = "utf8=%E2%9C%93&authenticity_token="+auth_token4+"&hook%5Burl%5D=http%3A%2F%2Fjenkins-"+self.userName + \
                "%3A8080%2Fproject%2Fupdate-production-app&hook%5Btoken%5D=&hook%5Bpush_events%5D=0&hook%5Bpush_events%5D=1&hook%5Bpush_events_branch_filter%5D=&hook%5Btag_push_events%5D=0&hook%5Bnote_events%5D=0&hook%5Bconfidential_note_events%5D=0&hook%5Bissues_events%5D=0&hook%5Bconfidential_issues_events%5D=0&hook%5Bmerge_requests_events%5D=0&hook%5Bjob_events%5D=0&hook%5Bpipeline_events%5D=0&hook%5Bwiki_page_events%5D=0&hook%5Benable_ssl_verification%5D=0"
            response4 = requests.request(
                "POST", url4, headers=headers4, data=payload4, allow_redirects=True)
            print("Response code:", response4.status_code)
            print("Response code:", response4.content)
            return True
        except:
            return False


if __name__ == "__main__":
    gc = GitlabController()
    gc.setUserName("charles")
    gc.checkStatus()