import subprocess
from subprocess import check_output

def dockerGetContainerId(podId):
    command = ["kubectl","describe","pod",podId]
    command_output = check_output(command).split()
    container_id = ''
    for i in command_output:
        # print(i)
        if 'docker://' in str(i):
            container_id = i.decode("utf-8").replace('\'','').split("docker://",1)[1]
            print("FOUND CONTAINER_ID:",container_id)
    return container_id

def dockerCreateSSHKeypair(containerId):
    subprocess.Popen([f"docker exec -i {containerId} bash -c \"ssh-keygen -f id_rsa -t rsa -N ''\""],shell=True).wait()

def dockerGetSSHPublicKey(containerId):
    public = check_output(["docker", "exec", "-i", containerId, "bash", "-c", "cat id_rsa.pub"])
    ssh_public_key = public.decode("utf-8")
    print("PUBLIC KEY:",ssh_public_key)
    return ssh_public_key

def dockerGetSSHPrivateKey(containerId):
    private = check_output(["docker", "exec", "-i", containerId, "bash", "-c", "cat id_rsa"])
    ssh_private_key = private.decode("utf-8")
    print("PRIVATE KEY", ssh_private_key)
    return ssh_private_key

def dockerCurlStatus(containerId, serviceName):
    print("DOCKER CURL STATUS", containerId)
    portNumberList = [8080, 80, 8000, 3000, 9000]
    if serviceName == "gitlab":
        check = check_output(["docker", "exec", "-i", containerId, "bash", "-c", "curl -o /dev/null -s -w \"%{http_code}\" http://localhost:8080"])
        print("CHECK ->>>",check)
        statusCode = check.decode("utf-8")
        print("Status Code:",statusCode)
        if "302" in str(statusCode):
            print("Status Code:",statusCode)
            return True
        else:
            return False
    if serviceName == "jenkins":
        check = check_output(["docker", "exec", "-i ", containerId, "bash", "-c", "curl -o /dev/null -s -w \"%{http_code}\" http://localhost:8080"])
        print("CHECK ->>>",check)
        statusCode = check.decode("utf-8")
        print("Status Code:",statusCode)
        if "200" in str(statusCode):
            print("Status Code:",statusCode)
            return True
        else:
            return False
    
