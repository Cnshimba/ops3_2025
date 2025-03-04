# Chapter-9 Lab01: Getting Started with docker run

## Objective:

- Learn how to use the docker run command to run pre-built container images.
- Understand basic Docker concepts like containers, images, and volumes.
- Practice running and managing containers.

## Prerequisites:

1. A PC or Virtual Machine running a Linux distribution with Docker installed (e.g., Ubuntu or Rocky Linux).
2. Internet access to pull images from Docker Hub.
3. Basic knowledge of the command line.

## Lab Tasks:

### 1. Verifying Docker Installation

Check if Docker is installed by running:

```bash
$ docker --version
```

Start the Docker service (if required):

```bash
$ sudo systemctl start docker
$ sudo systemctl enable docker
```

### Pulling a Pre-built Image

- Pull the official hello-world image:

  ```bash
  $ docker pull hello-world
  ```

- Verify that the image is downloaded:

  ```bash
  $ docker images
  ```

**Side Note:**

The images that we are using in this lab are downloaded from the cloud, on Docker Hub.

#### What is Docker Hub?

Docker Hub is a public registry where developers and organizations store and share container images. It's like a repository for Docker images that you can pull and use to run containers.

#### Why Use Docker Hub?

- It contains a vast library of **pre-built images** for popular applications (e.g., Nginx, MySQL, Ubuntu).
- Saves time: You don't have to create images from scratch for commonly used applications.
- It supports versioning, so you can specify a particular version of an image.

#### How Docker Hub Works with docker run:

When you run a command like docker run ubuntu, Docker:

1. Checks if the ubuntu image exists locally.
2. If not, it automatically downloads it from Docker Hub.
3. Once downloaded, Docker uses it to create a container.

#### Key Components of Docker Hub:

- **Official Images:** Verified and maintained by Docker or trusted organizations (e.g., nginx, mysql, redis).
- **User-contributed Images:** Custom images shared by the Docker community.
- **Private Repositories:** You can also create private repositories for your projects (with a Docker Hub account).

#### How to Search for Images:

Use the docker search command to find images directly from your terminal

```bash
$ docker search ubuntu
```

### 2. Running a Simple Container

Now that the image is downloaded let us use it to create a container and run it.

Run the hello-world container:

```bash
$ docker run hello-world
```

Observe the output and explain the workflow:

- Docker checks for the image locally.
- If not found, it pulls the image from Docker Hub.
- It creates and runs a container from the image.

### 3. Running an Interactive Container

- Run the ubuntu container interactively:

  ```bash
  $ docker run -it ubuntu
  ```

- The -it flags provide an interactive terminal that we can run commands in.

- Inside the container, run a few basic Linux commands, like:

  ```bash
  $ ls
  $ pwd
  $ echo "Hello from inside the container!"
  ```

- Exit the container using:

  ```bash
  $ exit
  ```

### 4. Running a Detached Container

**What is Detached Mode?** Detached mode allows you to run a container in the background without attaching your terminal to its output. This is useful for running long-lived services, such as web servers or databases, where you don't need to actively monitor the container logs in real-time.

- Run an Nginx web server in detached mode:

  ```bash
  $ docker run -d --name my-nginx -p 8080:80 nginx
  ```

- Verify the container is running:

  ```bash
  $ docker ps
  ```

- Access the Nginx default page by opening a browser and navigating to http://localhost:8080.

### 5. Stopping and Removing Containers

- Stop the running Nginx container:

  ```bash
  $ docker stop my-nginx
  ```

- Remove the container:

  ```bash
  $ docker rm my-nginx
  ```

### 6. Mounting Volumes

- Run an nginx container with a volume:

  ```bash
  docker run -d --name nginx-with-vol -p 8080:80 -v $(pwd)/html:/usr/share/nginx/html nginx
  ```

#### Command Breakdown:

- **docker run:** This is the Docker command to create and run a new container.
- **-d:** Runs the container in **detached mode** (in the background).
- **--name nginx-with-vol:** Assigns a name (nginx-with-vol) to the container for easier identification and management.
- **-p 8080:80:** Maps port **80** of the container (default port for Nginx) to port **8080** on the host machine.
  1. This allows you to access the web server by visiting http://localhost:8080 in a browser.
  2. Format: host-port:container-port.
- **-v $(pwd)/html:/usr/share/nginx/html:**
  - Mounts a volume (a directory from your host system) into the container.
  - **$(pwd)/html:** Refers to the html directory in your current working directory (on the host).
  - **/usr/share/nginx/html:** This is the directory inside the container where Nginx serves its HTML files by default.
  - The volume ensures that any changes you make to the files in $(pwd)/html on your host will immediately reflect in the container. This is useful for development or content updates.
- **nginx:** Specifies the **image** to use. Docker will pull the official Nginx image from Docker Hub if it isn't already available locally.

- Create a sample HTML file in the host directory:

  ```bash
  $ mkdir html
  $ echo "<h1>Hello from Docker!</h1>" > html/index.html
  ```

- Access the modified web page at http://localhost:8080.

### 7. Exploring Container Logs

- Check the logs of the nginx-with-vol container:

  ```bash
  $ docker logs nginx-with-vol
  ```

### 8. Cleaning Up

- Stop and remove all containers:

  ```bash
  $ docker stop $(docker ps -aq)
  $ docker rm $(docker ps -aq)
  ```

- Remove all images (optional):

  ```bash
  $ docker rmi $(docker images -q)
  ```

## Discussion Points:

1. What is the difference between an image and a container?
2. Why do we use detached mode for some containers?
3. How do volumes help in containerized applications?
