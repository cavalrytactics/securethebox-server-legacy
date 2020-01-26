import sys

def writeConfig(**kwargs):
    template = """
kind: ConfigMap
apiVersion: v1
metadata:
  name: traefik-config
  namespace: default
data:
  traefik.toml: |
    defaultEntryPoints = ["http", "https"]
    [entryPoints]
      [entryPoints.http]
      address = ":80"
        [entryPoints.http.auth.forward]
        address = "http://eas.us-west1-a.securethebox.us:8080/verify?config_token=tsUdAn%2FpNXvl58Uon2IzBS%2FZdbKZnQzXMlgba9f6ZbDAmz1CJqXLscmXN9bJze27bkP30K5FpW4EKiOaEHjM%2BEWbwpjMIeU%2BzKuR%2BXKIMlW83uZVFu1XGIAoP%2Fl8PvmmFwXEs0v9lyGVMpXBWRfq4IupiGTxXgMFdXKzWWSOdBdYF337AxnedtN8xxmev%2FdNattpsSqFfpNqk7MZpCJZnupolIL4u9yf5yzF1JCIFWg%2FCgfyifMWiODB9Zc311V8XqXrcJT6t%2FjoPRO%2BLrXnmwcV2ReB57rk%2FOz2Z4%2FaTettjaVZo8ZfDcbePBBSdEmYMjvHbxs2D%2FklB%2BWU2S7kAw8ZXhBLF4z7dxlmAqNt%2FtLOsfZ3LtEF%2FIym3%2FsMlKkjQlkHcXIimvn5FxCtfmAbqc96RlIGaIt9louJJn9f7gzS0xmmAg4fcQV2krDCdbLfl2Nybz4H%2F9ZNJ%2Bf6mqyV0EedSgkiq36V1a4ujvG4AJlxxa0%2BlkBHXBQKa9TV5YmixzTOff4h9OLIUKZTYkiFsm9Fav%2FEs2ZVXONAZrlmAFOuzj%2BrFDiiyGrx0LZ15pLfxLxwhjOTm6N%2BKoN02eudUg0FKI%2FBbvl5qVd2ZM4BHlaHAxNIwVCL8k%2BnEp3phjcKGTJbKmX6q4F85V2a5GAp8A%3D%3D"
        authResponseHeaders = ["X-Userinfo", "X-Id-Token", "X-Access-Token"]
      [entryPoints.api]
      address = ":8080"
    [api]
    entryPoint = "api"
    [kubernetes]
    [respondingTimeouts]
      idleTimeout = "620s"
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/ingress/'+str(sys.argv[2])+'/03_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-config.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]), serviceName=str(sys.argv[2]))