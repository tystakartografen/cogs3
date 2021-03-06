# Parent image
FROM python:3.8.3

# Enable log messages to be immediately sent to the output stream
ENV PYTHONBUFFERED 1

# Create a directory to store the application's source code
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Install the required software packages
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application's source code to the working directory
COPY . /app/

# Install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -xzf geckodriver-v0.26.0-linux64.tar.gz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin
RUN rm geckodriver-v0.26.0-linux64.tar.gz
