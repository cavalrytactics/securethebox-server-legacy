"""
Git Scripts to make life easier
"""
import json
import subprocess
import sys
import os
from subprocess import check_output

class GitControl():
    def __init__(self):
        self.git_user = ""
        self.git_fork_name = ""
        self.git_prod_name = "securethebox"
        self.git_url = ""
        self.git_current_branch = ""
        self.git_upstream = ""
        self.arguments = []
        self.pytest_result = False
        self.lint_travis_result = False

    def setArguments(self, args):
        self.arguments = args

    def setGithubProjectUser(self):
        with open('./package.json',"r") as f:
            data = json.load(f)
            self.git_user = data["repository"]["url"].split('/')[3]
    
    def setGithubProjectName(self):
        with open('./package.json',"r") as f:
            data = json.load(f)
            self.git_fork_name = data["repository"]["url"].split('/')[4][:-4]
    
    def setCurrentGitBranch(self):
        branchName = subprocess.Popen("git branch | grep \\* | cut -d ' ' -f2", stdout=subprocess.PIPE, shell=True)
        parsedBranch = os.environ["CURRENTBRANCH"] = str(branchName.communicate()[0].decode('utf-8')).split('\n', 1)[0]
        self.git_current_branch = parsedBranch
    
    def pytestCheck(self):
        failures = subprocess.Popen([f"export SKIPKUBE=NO && pytest -vs -x tests/"],shell=True).wait()
        if failures >= 1:
            self.pytest_result = False
        else:
            self.pytest_result = True

    def pytestCheckSkip(self):
        failures = subprocess.Popen([f"export SKIPKUBE=YES && pytest -vs -x tests/"],shell=True).wait()
        if failures >= 1:
            self.pytest_result = False
        else:
            self.pytest_result = True
    
    def lintTravisCheck(self):
        failures = subprocess.Popen([f"travis lint"],shell=True).wait()
        if failures >= 1:
            self.lint_travis_result = False
        else:
            self.lint_travis_result = True

    def interpretArgs(self):
        self.setGithubProjectName()
        self.setGithubProjectUser()
        self.setCurrentGitBranch()

        # Set environment type
        if self.arguments[0] == "dev":
            os.environ["APPENV"] = "DEV"
            subprocess.call("export APPENV=DEV && export SKIPKUBE=YES && ./venv/bin/python3.7 app.py",shell=True)
        elif self.arguments[0] == "prod":
            os.environ["APPENV"] = "PROD"
            subprocess.call("export APPENV=PROD && export SKIPKUBE=NO && ./venv/bin/python3.7 app.py",shell=True)

        # Pip Libraries
        elif self.arguments[0] == "pip-save":
            subprocess.call("./venv/bin/pip3 freeze > requirements.txt",shell=True)       
        
        # Pushing Master
        elif self.arguments[0] == "git-push-master":
            self.lintTravisCheck()
            self.pytestCheck()
            if self.pytest_result == True and self.lint_travis_result == True:
                subprocess.Popen([f"git checkout master && git add . && git cz ; git push"],shell=True).wait()
            else:
                print("PYTEST FAILED!")
        
        # Pushing Branch
        elif self.arguments[0] == "git-push-branch":
            self.lintTravisCheck()
            # self.pytestCheck()
            if self.pytest_result == True and self.lint_travis_result == True:
                if self.git_current_branch != "master":
                    subprocess.Popen([f"git add ."],shell=True).wait()
                    subprocess.Popen([f"git cz && git push --set-upstream origin "+self.git_current_branch+" && cross-var \"open https://github.com/"+self.git_user+"/"+self.git_fork_name+"/compare/master..."+self.git_user+":"+self.git_current_branch+"?expand=1\""],shell=True).wait()
                else:
                    print("YOU ARE NOT CHECKOUT TO A BRANCH! git checkout -b \"TICKET-ID\"")
            else:
                print("PYTEST FAILED!")

        elif self.arguments[0] == "git-push-branch-skip":
            self.lintTravisCheck()
            self.pytestCheckSkip()
            if self.pytest_result == True and self.lint_travis_result == True:
                if self.git_current_branch != "master":
                    subprocess.Popen([f"git add ."],shell=True).wait()
                    subprocess.Popen([f"git cz && git push --set-upstream origin "+self.git_current_branch+" && cross-var \"open https://github.com/"+self.git_user+"/"+self.git_fork_name+"/compare/master..."+self.git_user+":"+self.git_current_branch+"?expand=1\""],shell=True).wait()
                else:
                    print("YOU ARE NOT CHECKOUT TO A BRANCH! git checkout -b \"TICKET-ID\"")
            else:
                print("PYTEST FAILED!")
        
        # Sync Fork Master
        elif self.arguments[0] == "git-sync-local":
            subprocess.Popen([f"git checkout master ; git pull"],shell=True).wait()

        # Merge with Upstream
        elif self.arguments[0] == "git-merge-upstream":
            subprocess.Popen([f"git remote add upstream https://github.com/"+self.git_prod_name+"/"+self.git_fork_name+".git ; git fetch upstream ; git checkout master ; git merge upstream/master"],shell=True).wait()

        elif self.arguments[0] == "pytest-all":
            failures = subprocess.Popen([f"pytest -vs -x tests/"],shell=True).wait()
            if failures >= 1:
                return False
            else:
                return True
        
        elif self.arguments[0] == "pytest-dev":
            failures = subprocess.Popen([f"export APPENV=DEV && export SKIPKUBE=NO && pytest -vs -x tests/"],shell=True).wait()
            if failures >= 1:
                return False
            else:
                return True
        
        elif self.arguments[0] == "pytest-dev-skip":
            failures = subprocess.Popen([f"export APPENV=DEV && export SKIPKUBE=YES && pytest -vs -x tests/"],shell=True).wait()
            if failures >= 1:
                return False
            else:
                return True
        
        elif self.arguments[0] == "pytest-prod":
            failures = subprocess.Popen([f"export APPENV=PROD && export SKIPKUBE=NO && pytest -vs -x tests/"],shell=True).wait()
            if failures >= 1:
                return False
            else:
                return True

        elif self.arguments[0] == "pytest-prod-skip":
            failures = subprocess.Popen([f"export APPENV=PROD && export SKIPKUBE=YES && pytest -vs -x tests/"],shell=True).wait()
            if failures >= 1:
                return False
            else:
                return True
        
        elif self.arguments[0] == "lint-travis":
            failures = subprocess.Popen([f"travis lint"],shell=True).wait()
            if failures >= 1:
                return False
            else:
                return True

        elif self.arguments[0] == "docker-build":
            failures = subprocess.Popen([f"docker build . -t cavalrytactics/securethebox-server:latest"],shell=True).wait()
            if failures >= 1:
                return False
            else:
                return True

        elif self.arguments[0] == "docker-push":
            failures = subprocess.Popen([f"docker build . -t cavalrytactics/securethebox-server:latest && docker push cavalrytactics/securethebox-server"],shell=True).wait()
            if failures >= 1:
                return False
            else:
                return True

        elif self.arguments[0] == "pytest-staging":
            subprocess.Popen([f"docker build . -t cavalrytactics/securethebox-server:latest && docker push cavalrytactics/securethebox-server && pytest -vs -x tests/test_staging_gitlab.py"],shell=True).wait()
            
        
            
if __name__ == "__main__":
    gc = GitControl()
    gc.setArguments(sys.argv[1:])
    gc.interpretArgs()