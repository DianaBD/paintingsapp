# Using official python runtime base image
FROM python:2.7-alpine

# Install our requirements.txt
ADD requirements.txt /
RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
ADD app.py /
ADD templates/index.html /templates/
ADD static/stylesheets/style.css /static/stylesheets/

# Make port 80 available for links and/or publish
EXPOSE 80

# Define our command to be run when launching the container
CMD ["python","app.py"]
