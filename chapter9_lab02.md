# Chapter-9 Lab02: Building Your Own Docker Image

This lab will guide you through the basics of working with Docker by containerizing a simple Flask application. By the end of this lab, you will have learned how to build, run, and interact with a Docker container running a Python web application.

## Objective

- Understand how to use a Dockerfile to containerize a Python application.
- Build and run Docker containers.
- Interact with a containerized web application.

## Prerequisites

- Basic knowledge of Python and Flask.
- Docker installed on your machine.
- A working terminal (Linux/MacOS) or PowerShell (Windows).

## Lab Files

### Directory Structure:

```
.
├── app.py
├── Dockerfile
└── requirements.txt
```

### 1. app.py

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, and welcome to intro to Docker for OPS3!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

### 2. requirements.txt

```
flask>=2.2.0
```

### 3. Dockerfile

```dockerfile
# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /usr/src/app

# Step 3: Copy the dependencies file
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the application code
COPY . .

# Step 6: Expose the application port
EXPOSE 5000

# Step 7: Define the default command to run the app
CMD ["python", "app.py"]
```

## Lab Instructions

### Step 1: Setup the Lab Directory

1. Create a directory named working_with_dockerfile.

2. Copy the app.py, Dockerfile, and requirements.txt files into this directory.

Your directory structure should look like this:

```
working_with_dockerfile/
├── app.py
├── Dockerfile
└── requirements.txt
```

### Step 2: Build the Docker Image

1. Open a terminal and navigate to the working_with_dockerfile directory:

```bash
$ cd working_with_dockerfile
```

2. Build the Docker image using the docker build command:

```bash
$ docker build -t ops3-flask-app .
```

- The -t flag tags the image with a name (ops3-flask-app).
- The . specifies the current directory as the build context.

3. Verify that the image has been created:

```bash
$ docker images
```

You should see an entry for ops3-flask-app in the list of images.

### Step 3: Run the Docker Container

1. Start a container from the image using the docker run command:

```bash
$ docker run -p 5000:5000 ops3-flask-app
```

- The -p flag maps port 5000 in the container to port 5000 on your host machine.

2. Open a browser and visit: http://localhost:5000

   You should see the message:
   "Hello, and welcome to intro to Docker for OPS3!"

3. Stop the container by pressing Ctrl+C in the terminal.

### Step 4: Experiment with Docker Commands

1. Run on a Different Host Port

```bash
$ docker run -p 8080:5000 ops3-flask-app
```

Visit http://localhost:8080.

2. List Running Containers

```bash
$ docker ps
```

Use this to see the container ID and status.

3. Stop a Running Container If you have a running container, stop it using:

```bash
$ docker stop <container-id>
```

4. View Build History

```bash
$ docker history ops3-flask-app
```

This shows the layers created during the image build process.

5. Inspect the Container

```bash
$ docker inspect <container-id>
```

View detailed information about the container.

### Step 5: Push the Image to Docker Hub (Optional)

1. Tag the image:

```bash
$ docker tag ops3-flask-app <dockerhub-username>/ops3-flask-app
```

2. Push the image to Docker Hub:

```bash
$ docker push <dockerhub-username>/ops3-flask-app
```

3. Verify the image is available on Docker Hub by logging into your account.

## Bonus Activity

**Create a Git Repository**:

Initialize a Git repository in the working_with_dockerfile directory and push the code to GitHub for version control.

## Learning Outcomes

By completing this lab, you should be able to:

- Understand the basics of Docker images and containers.
- Learn to write and use a Dockerfile.
- Gain hands-on experience with containerizing and running a Python Flask application.
- Explore common Docker commands for managing images and containers.
