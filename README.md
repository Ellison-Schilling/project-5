# UOCIS322 - Project 5 Brevets, but with Mongo Now


# Descriptions


## Application


This project involves the development of hosting a website that allows user input for the duration of a bike ride, and brevet locations in terms of distance. In return for such information, the program will automatically fill in the brevet times that should be put in place based on the standards given. The program relies heavily on JQuery, Python, JavaScript, HTML, and Docker for testing in a more controlled enviorment. Now, however the program is improved by providing the ability to save a race and the associated table using a submit button, and the ability to display the last submitted table using the display button. The tables are saved via mongodb.



## Algorithm


In this project we take information from the user using JQuery in the html file and send it to our main python file called flask_brevets.py that then parses the information as needed as well as handles the webpage directing. From their flask_brevets sends a request to acp_times.py that handles ensuring the validity of the entries, as well as determing how much time should be allocated to the open and close times of the given brevet and sends such information back to flask_brevets.py. After that flask_brevets.py uses json to send the information back over to the html file that then formats and redirects the information to the webpage to fill in the boxes associated with the opening and closing time brevets.Beyond all this when the submit button is clicked all of the associated information on the page is stored with MongoDB in the flask app using a route case and jquery, then the page is cleared of all entries. When a user clicks on the display button, provided they have submitted at least one entry, the most recent entry is then fetched on the flask app from the mongo database and returned to the table via json. 



UPDATED UP TO HERE
# Instructions For Use


## Docker
To run docker for this application first ascertain that you are in the correct directory, specifically the one that contains the Dockerfile. From there proceed to make your Docker image by executing the command:


docker build -t brevets .   



After the image is successfully built you will want to run the image by executing the command or a command similar to:


docker run  -p5001:5000 --rm brevets 



Supposing everything went smoothly, your web application should now be up and running. 



## Web App



In the web application there are three main important fields to fill:


* The first is the distance of the brevet which you can select from the Distance selector. You may select from the provided options of 200, 300, 400, 600, 1000.


* The second is the date and time selector for the start of your brevet labeled as "Begins at". There you may select the proper day, month, year, and time that you wish for your brevet to begin.


* The third field to fill in is where you wish to place your control brevets in the race. You may choose to either type in the miles or kilometers field and rest assured that no matter which you choose all else will be filled in. After you type in your control brevet distance the rest of the row should fill in aside from the location which you may set. However, if you enter an invalid number according to ACP, then no automatic entries will appear until you correct it.




# Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani. Completed by Ellison Schilling.

## Contact Address

ellisons@uoregon.edu









# UOCIS322 - Project 5 #
Brevet time calculator with MongoDB!

## Overview

You'll add a storage to your previous project using MongoDB and `docker-compose`.
As we discussed, `docker-compose` makes it easier to create, manage and connect multiple container to create a single service comprised of different sub-services.

Presently, there's only a placeholder directory for your Flask app, and a `docker-compose` configuration file. You will copy over `brevets/` from your completed project 4, add a MongoDB service to docker-compose and your Flask app. You will also add two buttons named `Submit` and `Display` to the webpage. `Submit` must store the information (brevet distance, start time, checkpoints and their opening and closing times) in the database (overwriting existing ones). `Display` will fetch the information from the database and fill in the form with them.

Recommended: Review [MongoDB README](MONGODB.md) and[Docker Compose README](COMPOSE.md).

## Tasks

1. Add two buttons `Submit` and `Display` in the ACP calculator page.

	- Upon clicking the `Submit` button, the control times should be inserted into a MongoDB database, and the form should be cleared (reset) **without** refreshing the page.

	- Upon clicking the `Display` button, the entries from the database should be filled into the existing page. ONLY NEEDS TO SUBMIT THE LATEST ONES

	- Handle error cases appropriately. For example, Submit should return an error if no control times are input. One can imagine many such cases: you'll come up with as many cases as possible.

2. An automated `nose` test suite with at least 2 test cases: at least one for for DB insertion and one for retrieval.

3. Update README.md with brevet control time calculation rules (you were supposed to do this for Project 4), and additional information regarding this project.
	- This project will be peer-reviewed, so be thorough.

## Grading Rubric

* If your code works as expected: 100 points. This includes:
	* Front-end implementation (`Submit` and `Display`).
	
	* Back-end implementation (Connecting to MongoDB, insertion and selection).
	
	* AJAX interaction between the frontend and backend (AJAX for `Submit` and `Display`).
	
	* Updating `README` with a clear specification (including details from Project 4).
	
	* Handling errors correctly.
	
	* Writing at least 2 correct tests using nose (put them in `tests`, follow Project 3 if necessary), and all should pass.

* If DB operations do not work as expected (either submit fails to store information, or display fails to retrieve and show information correctly), 60 points will be docked.

* If database-related tests are not found in `brevets/tests/`, or are incomplete, or do not pass, 20 points will be docked.

* If docker does not build/run correctly, or the yaml file is not updated correctly, 5 will be assigned assuming README is updated.

## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.
