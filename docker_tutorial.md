# Docker Tutorial for Students

## OPERATING SYSTEMS 3

### EIOSY3A

## DOCKER PRIMER

---

## Introduction to Docker

Docker is a platform that simplifies the process of developing, shipping, and running applications using containers. Containers are lightweight, portable, and self-contained units of software that package an application along with its dependencies, such as libraries and configurations, ensuring it runs consistently across different computing environments. Unlike virtual machines, which emulate an entire operating system, containers share the host OS kernel, making them much more efficient in terms of resource usage and performance.

This tutorial will guide students through the essential Docker concepts and commands with practical examples to help them get started. In this tutorial, we assume the environment you will be running the labs is Linux.

---

## 1. Setting Up Docker

Docker must be installed before it can be used. Below are instructions for different Linux distributions.

### Installation

#### For Debian/Ubuntu:
To install Docker on Debian-based distributions like Ubuntu, run the following commands:
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

#### For RHEL/CentOS:
For Red Hat-based distributions like CentOS, use the following commands:
```bash
sudo yum install docker-ce docker-ce-cli containerd.io
```

### Starting Docker
Once installed, Docker must be started and enabled to run at boot.

#### Start Docker:
```bash
sudo systemctl start docker
```

#### Enable Docker to start on boot:
```bash
sudo systemctl enable docker
```

#### Check the status of Docker:
```bash
sudo systemctl status docker
```

If Docker is running correctly, the status command should indicate that the service is active.

---

## 2. Working with Docker Images

Docker images are the foundation of containers. Images contain the software, libraries, and dependencies required to run applications inside containers.

### Listing Downloaded Images
To list all the images stored locally on your system, run:
```bash
docker images
```
Example Output:
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    605c77e22612   2 weeks ago    133MB
ubuntu       20.04     ba6acccedd29   3 weeks ago    72.8MB
```

### Downloading an Image from Docker Hub
Docker Hub is a public registry where images are stored. To download an image, use:
```bash
docker pull <image-name>:<tag>
```
Example:
```bash
docker pull nginx:latest
docker pull ubuntu:20.04
```

### Removing an Image
If an image is no longer needed, it can be removed to free up space:
```bash
docker rmi <image-id>
```
Example:
```bash
docker rmi nginx
docker rmi -f nginx
```

---

## 3. Running Containers

Once an image is downloaded, you can create and run containers from it.

### Running a Container Interactively
The `-it` option allows you to interact with a running container:
```bash
docker run -it <image-name> <command>
```
Example:
```bash
docker run ubuntu echo "Hello"
docker run -i ubuntu /bin/bash
```

### Running a Container in Detached Mode
Detached mode (`-d`) allows a container to run in the background:
```bash
docker run -d <image-name>
```
Example:
```bash
docker run -d nginx
docker run -d -e MYSQL_ROOT_PASSWORD=mypassword mysql
```

---

## 4. Managing Containers

Containers can be stopped, restarted, or removed when needed.

### Listing All Containers
```bash
docker ps -a
```

### Starting, Stopping, and Removing a Container
```bash
docker start <container-id>
docker stop <container-id>
docker rm <container-id>
```

### Cleaning Up Unused Containers
To remove all stopped containers:
```bash
docker container prune
```

---

## 5. Docker Volumes

Containers are ephemeral, meaning data inside them is lost when they stop. Docker volumes allow persistent storage outside the container lifecycle.

### Creating a Persistent Volume
```bash
docker run -v <volume-name>:<container-path> <image-name>
```
Example:
```bash
docker run -v mysql_data:/var/lib/mysql mysql:5.7
```

### Managing Volumes
To list and remove volumes:
```bash
docker volume ls
docker volume rm <volume-name>
```

---

## 6. Networking in Docker

Docker networking allows containers to communicate with each other and the outside world.

### Listing Available Networks
```bash
docker network ls
```

### Creating a Custom Bridge Network
```bash
docker network create my_bridge
```

### Connecting Containers to the Same Network
```bash
docker run --name container1 --network my_bridge nginx
docker run --name container2 --network my_bridge alpine ping container1
```

### Removing a Network
```bash
docker network rm <network-name>
```

---

## 7. Building Custom Docker Images

Users can create their own Docker images using a Dockerfile.

### Example Dockerfile
```dockerfile
FROM ubuntu:20.04
WORKDIR /usr/src/app
COPY requirements.txt .
RUN apt-get update && apt-get install -y curl
COPY . .
CMD ["bash"]
```

### Building and Running a Custom Image
```bash
docker build -t my-app .
docker run -it my-app
```

---

## 8. Uploading Images to Docker Hub

### Tagging and Pushing an Image
```bash
docker tag my-app <dockerhub-username>/my-app:v1
docker push <dockerhub-username>/my-app:v1
```

---

## 9. Deploying an App to Azure Using ACI

### Steps to Deploy a Container
```bash
az login
az group create --name myResourceGroup --location eastus
az acr create --resource-group myResourceGroup --name myRegistry --sku Basic
az acr login --name myRegistry
```

### Pushing the Image to ACR
```bash
docker tag my-app myRegistry.azurecr.io/my-app:v1
docker push myRegistry.azurecr.io/my-app:v1
```

### Deploying the Container in Azure
```bash
az container create --resource-group myResourceGroup --name myContainer --image myRegistry.azurecr.io/my-app:v1 --dns-name-label my-app --ports 80
```

---

## Conclusion

This tutorial covered the fundamental concepts of Docker, including:
- Installing Docker
- Managing images and containers
- Networking and volumes
- Creating custom images
- Deploying applications using Azure and Docker Compose


