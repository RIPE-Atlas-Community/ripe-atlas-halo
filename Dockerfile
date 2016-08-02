FROM python:3.4

# Install the dependencies before copying the source code
# as this prevents frequent docker  build commands from having
# to keep re-installing the same dependencies over and over
COPY /requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


# Copy the local directory into the app directory
COPY / /app

# All subsequent docker commands will use this path as its root
WORKDIR /app/src

# As per the install instructions - run the migration task
RUN ./manage.py migrate



# This allows the container to be started with the current source
# code mounted into it by using
#   docker run -it --rm -p 8000:8000 -v .:/app ripe-atlas-halo
VOLUME /app

# Ensure that the django port is presented to the user
EXPOSE 8000


# Run the application by default
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
