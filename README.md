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

1. docker build . -t ripe-atlas-halo
1. docker run --rm -d -P ripe-atlas-halo
1. Open a browser and point it at http://localhost:8000/

## Colophon

This project was named *"Halo"* after the video game by the same name.  It's a
reference to heads-up display (as one has in any FPS), which is synonym for a
dashboard... which is what this is.

Give us a break, we had limited time and more important things to do than pick
a name ;-)

