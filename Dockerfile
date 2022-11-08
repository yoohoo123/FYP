
#decide what type of software we are dealing with. In this case, python
FROM python:3.10

#what file are we dockerising, in the case app.py
ADD app.py .
# this code copy the requirement, this is to install any libraries and dependencies. 
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt



CMD [ "python","./app.py" ,"--host" ,"0.0.0.0","--port","80"]

#Here are some commands that can prove useful

# Code to create the docker image
# docker build -t python-fyp .
# docker run python-fyp