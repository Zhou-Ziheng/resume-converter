# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    poppler-utils \ 
    tesseract-ocr \
    tesseract-ocr-eng \
    libleptonica-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Install LaTeX
RUN apt-get update && apt-get install -y \
    texlive \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pdflatex
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["ddtrace-run", "gunicorn", "--timeout", "1000", "--bind", "0.0.0.0:5000", "-w", "2", "app:app"]