# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /usr/src/app/

# Copy application files
COPY . ./
# Run apt-get in non-interactive mode
ARG DEBIAN_FRONTEND=noninteractive
#Install networking tools such as the ip command
RUN apt-get update && apt-get install net-tools -y
RUN apt install iproute2 -y
# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port. This is just for documentation purposes. When running the container make sure 
# to use -p with docker run to implent this. 
 EXPOSE 5000

# Run the application
ENTRYPOINT [ "python3","app.py"]

