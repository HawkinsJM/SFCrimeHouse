#SF Crime + Housing

##Goal
The goal of this project was to develop a website that allowed users to explore the interpaly between crime and housing cost in several different districts of San Fransisco. Crime incluences housing costs and this tool will allow users to make smart real-estate purchasing decisions.

##Interacivity
Users can generate plots to investigate the crime in a single district or compare crime across districts. The data can also be normalized, or the "Deal Index" can be used to determine which districts have the best deal on crime. A higher Deal Index is better.

##Website
The website was created using Flask. Bokeh and Bootstrap were used to make the website and plots look nice. Heroku is used to host the site.

##Data Sources
The housing data was gathered from Trulia's API, the crime data was downloaded from data.sfgov.org. These are cleaned and combined in Python/Pandas.