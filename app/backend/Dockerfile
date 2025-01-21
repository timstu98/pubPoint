# Use a Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5001

# Start the Flask app
CMD ["flask", "run", "--debug","--reload","--host=0.0.0.0", "--port=5001"]