# Node.js base image
FROM node:latest

# Install Python 3.9 and other required tools
RUN apt-get update && \
    apt-get install -y python3.9 python3-pip && \
    python3.9 -m pip install --upgrade pip && \
    python3.9 -m pip install pillow && \
    apt-get clean

# Set working directory
WORKDIR /usr/src/app

# Copy Node.js files
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the Node.js application
COPY . .

# Expose your Node.js app's port
EXPOSE 3001

# Start Node.js application
CMD ["npm", "start"]
