# Use the official nginx image as base
FROM nginx:alpine

# Remove the default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf
ARG DEBIAN_FRONTEND=noninteractive

# Copy our custom configuration
COPY default.conf /etc/nginx/conf.d/

# Expose port 80
EXPOSE 80

# Start nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]