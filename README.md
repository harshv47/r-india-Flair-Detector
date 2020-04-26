# r-india-Flair-Detector

This is an application that can predict flairs for a reddit post in r/india

## Jupyter Notebooks

The whole journey of making this project is encapsulated in the [Experiment Log](https://github.com/harshv47/r-india-Flair-Detector/blob/master/Jupyter%20Notebooks/Experiment_log.ipynb)

The main well-commented Jupyter Notebook containing everthing from creation of dataset to prediction is [here](https://github.com/harshv47/r-india-Flair-Detector/blob/master/Jupyter%20Notebooks/r_india_flair_predictor.ipynb)

## Requirements

Ensure that Python3, pip and git are installed.

In Ubuntu, python is installed by default so you have to only install pip and git. You can use `sudo apt-get install python3-pip git`

To install all the requirements use:   `pip3 install -r requirements.txt`

Please use Python 3. `praw` has deprecated support for python 2.

## Usage

First clone the repository by using `git clone https://github.com/harshv47/r-india-Flair-Detector.git` command

Now run [app.py](https://github.com/harshv47/r-india-Flair-Detector/blob/master/app.py) by using `python3 app.py`. This let's you enter one reddit post url.
If you want to enter more than one url, you can send a post request to `http://127.0.0.1:5000//automated_testing` with a text file containing a url on each line.

## Deployment

The application is deployed [here](https://r-india-flair-detector-harsh.herokuapp.com/).
Though currently there are some issues, I'll iron them out soon.