import subprocess
import os
import requests
from lxml import html
import urllib
import gitlab
import datetime

class GitlabController():
    def __init__(self):
        self.clusterName = ""
        self.userName = ""
        self.currentDirectory = ""
        self.gitlabHost = ""
        self.gitlabPrivateToken = ""
        self.gitlabConnection = gitlab.Gitlab(self.gitlabHost, private_token=self.gitlabPrivateToken)
        self.httpSessionCookie = ""
        self.httpUrl = ""
        self.httpHeadersHost = ""
    
    def setClusterName(self, clusterName):
        try:
            self.clusterName = clusterName
            return True
        except:
            return False

    def setUserName(self, userName):
        self.userName = userName

    def setCurrentDirectory(self, currentDirectory):
        self.currentDirectory = os.getcwd()
    
    def setHttpUrl(self, httpUrl):
        self.httpUrl = httpUrl

    def setHttpSessionCookie(self, httpSessionCookie):
        self.httpSessionCookie = httpSessionCookie

    def setHttpHeaderHost(self, httpHeadersHost):
        self.httpHeadersHost = httpHeadersHost

    def gitlabGetResetPasswordToken(self):
        url = "http://gitlab-"+self.userName+"."+self.clusterName+".securethebox.us"
        headers = {
            'Host': "gitlab-"+self.userName+"."+self.clusterName+".securethebox.us"
            }
        response = requests.request("GET", url, headers=headers, allow_redirects=True)
        response_url = response.url
        password_token = response_url.split('=')
        session_cookie = response.request.headers['Cookie']
        return password_token[1],session_cookie
