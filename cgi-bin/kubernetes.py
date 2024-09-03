#!/usr/bin/python3

import cgi
import subprocess
import logging

# Set up logging
logging.basicConfig(filename="/var/log/cgi_errors.log", level=logging.DEBUG)

print("Content-Type: text/html")
print()

try:
    f = cgi.FieldStorage()
    cmd = f.getvalue("x")
    logging.debug(f"Command received: {cmd}")
    if cmd:
        ins = cmd.split()
        if ins[0] == "1":
            img_name = ins[1]
            deployment_name = ins[2]
            command = f"kubectl create deployment {deployment_name} --image={img_name}"
        elif ins[0] == "2":
            pod_name = ins[2]
            img_name = ins[1]
            command = f"kubectl run {pod_name} --image={img_name}"
        elif ins[0] == "3":
            pod_name = ins[1]
            command = f"kubectl delete pod {pod_name}"
        elif ins[0] == "4":
            deployment_name = ins[1]
            command = f"kubectl delete deployment {deployment_name}"
        elif ins[0] == "5":
            deployment_name = ins[1]
            port_no = ins[2]
            expose_type = ins[3]
            command = f"kubectl expose deployment {deployment_name} --port={port_no} --type={expose_type}"
        elif ins[0] == "6":
            deployment_name = ins[1]
            replica = ins[2]
            command = f"kubectl scale deployment {deployment_name} --replicas={replica}"
        elif ins[0] == "7":
            command = "kubectl get pods"
        elif ins[0] == "8":
            command = "kubectl get svc"
        elif ins[0] == "9":
            command = "kubectl delete all --all"
        
        logging.debug(f"Running command: {command}")
        output = subprocess.getoutput(f"sudo {command} --kubeconfig /root/admin.conf")
        logging.debug(f"Command output: {output}")
        print(output)
    else:
        logging.error("No command received.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
    print(f"An error occurred: {e}")
