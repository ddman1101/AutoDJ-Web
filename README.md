# AutoDJ-Web

The web is made a platform for the auto-dj. And the web is unfinished, so it still has some problem in it. But it still has some function :

1. Annotate the music online
2. Upload the music to local machine.

## Installing dependencies

The automatic-DJ web has been developed for python 3.7.7 and tested on Ubuntu 18.04 LTS. It depends on the following python packages:

* Django (3.0.8)
* colorlog (2.10.0)
* Essentia
* joblib (0.11)
* librosa (0.5.0)
* numpy (1.19.1)
* pyAudio (0.2.8)
* scikit-learn (0.18.1)
* scipy (0.19.0)
* yodel (0.3.0)
* madmom (0.17.dev0)

These packages can be installed using e.g. the `pip` package manager or using `apt-get` on Ubuntu. Installation instructions for the Essentia library can be found on [http://essentia.upf.edu/documentation/installing.html](http://essentia.upf.edu/documentation/installing.html).

You can also run 
`pip install -r requirements.txt`
to make the part of installing dependencies.

## How to use
You need to run the web on the server first. So you need to run this under the `AutoDJ-web/` first
* `python manage.py runserver`

Then
1. Click `Choose File` to upload your music.
2. After upload all your music (Suggest : more than 20 songs), click the `DJ start`
3. then input the command to control the Auto-DJ

* `annotate` : Annotate all the files in the pool of available songs that are not annotated yet. Note that this might take a while, and that in the current prototype this can only be interrupted by forcefully exiting the program

## Future work
- Build the function "play" in it. (Real-time)
- Save the set and provide the "download" function.



