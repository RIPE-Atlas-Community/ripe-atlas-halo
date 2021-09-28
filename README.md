# RIPE Atlas Halo

A heads-up display for your network

## How to Run It

It's a Django app, so if you're familiar with that, installation should be
easy.  Just do the following:

1. Create a virtualenv (Python 3.4+)
2. Enter that virtualenv
3. Check out the code from this repo
4. Run `pip install -r requirements.txt` (in the root of this project)
5. Change to the `src` directory in this project
6. Run `./manage.py migrate`
7. Run `./manage.py runserver`
8. Open a browser and point it at http://localhost:8000/

## Docker Version

You can build, and start the ripe-atlas-halo project as a docker container using
the following commands.

The first will command docker to execute the Dockerfile and create a new local
image on your workstation which contains the current src of the project, along
with the required dependencies based on requirements.txt

The second command starts the container for use.

    docker build -t ripe-atlas-halo .
    docker run -d --name my-ripe-atlas-halo -p 8000:8000 ripe-atlas-halo

Once the container has started, you can navigate to the interface on http://localhost:8000/

To stop the container, simply run

    docker stop my-ripe-atlas-halo

## Colophon

This project was named *"Halo"* after the video game by the same name.  It's a
reference to heads-up display (as one has in any FPS), which is synonym for a
dashboard... which is what this is.

Give us a break, we had limited time and more important things to do than pick
a name ;-)
