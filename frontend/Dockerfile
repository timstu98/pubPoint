# Use a Node.js image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json .
RUN npm install

# Copy the rest of the code
COPY . .

# Build the React app
# RUN npm run build 
# RUN npm run start

# Expose the port for the React app
EXPOSE 3000

# Start the React app
CMD ["npm", "run","dev"]