# Use a base image with Python 3.9
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only the necessary files to reduce build context size
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Install system dependencies and clean up apt-get cache to reduce image size
RUN apt-get clean && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
    curl \
    libpoppler-cpp0v5 \
    poppler-utils \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application files into the container
COPY . /app/

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit-app.py"]