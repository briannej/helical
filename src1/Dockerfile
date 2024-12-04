# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables for AWS credentials (replace with your credentials)
ENV DATASET=your_dataset
ENV MODEL=your_model
ENV APPLICATION=your_application

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the training and model publishing script
CMD ["python", "prepare_image.py"]
#WORKDIR /app/notebooks
#CMD ["papermill", "Quick-Start-Tutorial.ipynb", "output_notebook.ipynb"]
