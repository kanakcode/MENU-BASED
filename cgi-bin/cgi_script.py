#!/usr/bin/env python3
import cgi
import cgitb
import os
import docker
from kubernetes import client, config

cgitb.enable()

def build_and_push_image(image_name, dockerfile_dir):
    client = docker.from_env()
    image = client.images.build(path=dockerfile_dir, tag=image_name)
    client.images.push(image_name)
    return image.tags[0]

def deploy_to_kubernetes(image_name, deployment_name):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    
    container = client.V1Container(
        name=deployment_name,
        image=image_name,
        ports=[client.V1ContainerPort(container_port=80)]
    )
    
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
        spec=client.V1PodSpec(containers=[container])
    )
    
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {'app': deployment_name}}
    )
    
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=spec
    )
    
    v1.create_namespaced_deployment(namespace="default", body=deployment)

def main():
    form = cgi.FieldStorage()
    image_name = form.getvalue("image_name")
    dockerfile_dir = form.getvalue("dockerfile_dir")
    deployment_name = form.getvalue("deployment_name")

    if image_name and dockerfile_dir and deployment_name:
        image_tag = build_and_push_image(image_name, dockerfile_dir)
        deploy_to_kubernetes(image_tag, deployment_name)
        print("Content-Type: text/html")
        print()
        print(f"<html><body><h2>Deployment {deployment_name} created with image {image_tag}</h2></body></html>")
    else:
        print("Content-Type: text/html")
        print()
        print("<html><body><h2>Error: Missing parameters</h2></body></html>")

if __name__ == "__main__":
    main()
