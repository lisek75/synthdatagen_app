# Use a Python 3.10 slim image as the base
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements.txt first (for better caching)
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Now, copy the rest of the project files into the container
COPY . .

# Expose the port where Gradio will run (default: 7860)
EXPOSE 7860

# Set the default command to run the app
CMD ["python", "app.py"]
