# Use an official Python runtime as a parent image
FROM python:3.11
FROM pytorch/pytorch:2.5.0-cuda12.4-cudnn9-runtime

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install build-essential \
        wget \
        git \
        curl \
        gcc \
        gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# RUN pip install --upgrade helical
RUN pip install git+https://github.com/helicalAI/helical.git@main
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility 
ENV NVIDIA_DRIVER_CAPABILITIES=all
RUN pip install lightning wandb


# Set environment variables for AWS credentials (replace with your credentials)
ENV DATASET=your_dataset
ENV MODEL=your_model
ENV APPLICATION=your_application

# Set the working directory in the container
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip to the latest version
#RUN pip install --upgrade pip


# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the training and model publishing script
CMD ["python", "prepare_image.py"]
#WORKDIR /app/notebooks
#CMD ["papermill", "Quick-Start-Tutorial.ipynb", "output_notebook.ipynb"]
