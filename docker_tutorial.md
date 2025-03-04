# Docker Tutorial for Students

## Introduction to Docker

Docker is a platform that simplifies the process of developing, shipping, and running applications using containers. Containers are lightweight, portable, and self-contained units of software that package an application along with its dependencies, ensuring it runs consistently across different computing environments.

This tutorial will guide students through the essential Docker concepts and commands with practical examples to help them get started. The labs assume you are running a Linux environment.

---

## Setting Up Docker

### Installation

**For Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

**For RHEL/CentOS:**
```bash
sudo yum install docker-ce docker-ce-cli containerd.io
```

### Starting Docker

Start and enable Docker service:
```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker
```

---

## Working with Docker Images

Docker images are blueprints for containers. Below are key commands:

### Listing Downloaded Images
```bash
docker images
```

### Download an Image from Docker Hub
```bash
docker pull <image-name>:<tag>
```
Example:
```bash
docker pull nginx:latest
docker pull ubuntu:20.04
```

### Removing an Image
```bash
docker rmi <image-id>
```
Example:
```bash
docker rmi nginx
docker rmi -f nginx
```

---

## Running Containers

Containers are instances of images. Below are different ways to run them:

### Run a Container Interactively
```bash
docker run -it <image-name> <command>
```
Example:
```bash
docker run -i ubuntu /bin/bash
```

### Run a Container in Detached Mode
```bash
docker run -d <image-name>
```
Example:
```bash
docker run -d nginx
```

### Map Container Ports to the Host
```bash
docker run -p <host-port>:<container-port> <image-name>
```
Example:
```bash
docker run -p 8080:80 nginx
```

### Setting Environment Variables
```bash
docker run -e MYSQL_ROOT_PASSWORD=mypassword mysql:5.7
```

---

## Managing Containers

### List All Containers
```bash
docker ps -a
```

### Start, Stop, and Remove Containers
```bash
docker start <container-id>
docker stop <container-id>
docker rm <container-id>
```

### Clean Up Unused Resources
```bash
docker container prune
docker image prune
docker system prune -a
```

---

## Docker Volumes

### Create a Persistent Volume
```bash
docker run -v <volume-name>:<container-path> <image-name>
```
Example:
```bash
docker run -v mysql_data:/var/lib/mysql mysql:5.7
```

### List and Remove Volumes
```bash
docker volume ls
docker volume rm <volume-name>
```

---

## Networking in Docker

Docker provides multiple networking options:

### List Networks
```bash
docker network ls
```

### Create a Bridge Network
```bash
docker network create my_bridge
```

### Run Containers in the Same Network
```bash
docker run --name container1 --network my_bridge nginx
docker run --name container2 --network my_bridge alpine ping container1
```

### Remove a Network
```bash
docker network rm <network-name>
```

---

## Building Custom Docker Images

### Example Dockerfile
```dockerfile
FROM ubuntu:20.04
WORKDIR /usr/src/app
COPY requirements.txt .
RUN apt-get update && apt-get install -y curl
COPY . .
CMD ["bash"]
```

### Build and Run the Docker Image
```bash
docker build -t my-app .
docker run -it my-app
```

---

## Uploading Images to Docker Hub

### Tag and Push an Image
```bash
docker tag my-app <dockerhub-username>/my-app:v1
docker push <dockerhub-username>/my-app:v1
```

---

## Deploying an App to Azure Using ACI

### Set Up Azure CLI and ACR
```bash
az login
az group create --name myResourceGroup --location eastus
az acr create --resource-group myResourceGroup --name myRegistry --sku Basic
az acr login --name myRegistry
```

### Tag and Push the Image
```bash
docker tag my-app myRegistry.azurecr.io/my-app:v1
docker push myRegistry.azurecr.io/my-app:v1
```

### Deploy to ACI
```bash
az container create --resource-group myResourceGroup --name myContainer --image myRegistry.azurecr.io/my-app:v1 --dns-name-label my-app --ports 80
```

---

## Deploying a Multi-Container Application with Docker Compose

### Example `docker-compose.yml`
```yaml
version: '3'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
```

### Start the Multi-Container Application
```bash
docker-compose up -d
```

---

## Conclusion

This tutorial covered:
- Installing Docker
- Managing images and containers
- Networking and volumes
- Building custom images
- Deploying applications using Docker Compose and Azure ACI

Continue practicing to build your Docker expertise!
