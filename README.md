# Rock Climb Visualizer 
## An Ran 

[Demo](http://mtnproj.herokuapp.com/) of visualizer on Heroku. 


This projects uses data from Mountain Project (popular website in the U.S. to rate rock climbs) to visualize climbs 
by stars and difficulty. The heat map allows the user to visualize the density of highly rated climbs at each location. 
The slider lets the user to set of the diffculty range, and the check box lets the user to filter for protection ratings (X, R, PG13).

The climbing diffculty/grading is in Yosemite Decimal System (YDS). 


## Technical Information
The visualization is done in plotly, the app development is done in dash, and the deployment on Heroku. 

For demostration, I have collected data for all routes in Joshua Tree national park. The data is collected from the mountain project website.
Since every climb in the same area has the same longitude/latitude, I slightly perturbed the location of each climbing so they roughly spread evenly
in a solid circle around the area location. 


## To dos:
This app is a work in progress. Features to come:
* more climbing data! maybe even getting data from thecrag, nzclimb etc....
* more filters - by ratings, sport vs trad ...
* ability to filter out climbs already done by importing user mountain project account
* integrating with mountain project climb recommender



