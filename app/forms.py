from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired
import pickle
import os

class bdForm(Form):
	#load districts pickle
	#['BAYVIEW', 'CENTRAL', 'MISSION', 'NORTHERN', 'SOUTHERN', 'TENDERLOIN']
	ctypes = sorted([('WEAPON LAWS', 'Weapon Laws'),
	 ('SECONDARY CODES', 'Secondary Codes'),
	 ('WARRANTS', 'Warrants'),
	 ('ROBBERY', 'Robbery'), ('BURGLARY', 'Burglary'),
	 ('SUSPICIOUS OCC', 'Suspicious Occ'),
	 ('ASSAULT', 'Assault'),
	 ('DRUNKENNESS', 'Drunkenness'),
	 ('OTHER OFFENSES', 'Other Offenses'),
	 ('FRAUD', 'Fraud'),
	 ('DRUG-NARCOTIC', 'Drug-Narcotic'),
	 ('TRESPASS', 'Trespass'),
	 ('LARCENY-THEFT', 'Larceny-Theft'),
	 ('VANDALISM', 'Vandalism'),
	 ('NON-CRIMINAL', 'Non-Criminal'),
	 ('VEHICLE THEFT', 'Vehicle Theft'),
	 ('MISSING PERSON', 'Missing Person'),
	 ('DISORDERLY CONDUCT', 'Disorderly Conduct'),
	 ]) + [('ALL', "All - Don't Normalize.")]
	# with open('app/static/data/perd/dist.pickle', 'rb') as f:
	# 	dist_list = pickle.load(f)
	crime_m = SelectMultipleField('crime_m',choices=ctypes)
	district_o = SelectField('district_o',choices=[('BAYVIEW','Bayview'),('CENTRAL', 'Central'), ('MISSION', 'Mission'), ('NORTHERN', 'Northern'),('SOUTHERN', 'Southern'),('TENDERLOIN','Tenderloin'),('ALL', 'All of SF')])
	norm_crime_house = SelectField('norm_crime_house',choices=[('neither','None'),('crime_ind', 'By Crime in District'), ('crime_sf', 'By Percent. Occur in City'),('crime_deal','By Deal')])
	freq = SelectField('freq',choices=[('1M','1 Month'),('3M', '3 Months'), ('6M', '6 Months')], default='6M')

class bcForm(Form):
	ctypes = sorted([
	 ('WEAPON LAWS', 'Weapon Laws'),
	 ('SECONDARY CODES', 'Secondary Codes'),
	 ('WARRANTS', 'Warrants'),
	 ('ROBBERY', 'Robbery'), ('BURGLARY', 'Burglary'),
	 ('SUSPICIOUS OCC', 'Suspicious Occ'),
	 ('ASSAULT', 'Assault'),
	 ('DRUNKENNESS', 'Drunkenness'),
	 ('OTHER OFFENSES', 'Other Offenses'),
	 ('FRAUD', 'Fraud'),
	 ('DRUG-NARCOTIC', 'Drug-Narcotic'),
	 ('TRESPASS', 'Trespass'),
	 ('LARCENY-THEFT', 'Larceny-Theft'),
	 ('VANDALISM', 'Vandalism'),
	 ('NON-CRIMINAL', 'Non-Criminal'),
	 ('VEHICLE THEFT', 'Vehicle Theft'),
	 ('MISSING PERSON', 'Missing Person'),
	 ('DISORDERLY CONDUCT', 'Disorderly Conduct'),
	 ]) + [('ALL', "All")]
	# with open('app/static/data/perd/dist.pickle', 'rb') as f:
	# 	dist_list = pickle.load(f)
	crime_o = SelectField('crime_o',choices=ctypes)
	district_m = SelectMultipleField('district_m',choices=[('BAYVIEW','Bayview'),('CENTRAL', 'Central'), ('MISSION', 'Mission'), ('NORTHERN', 'Northern'),('SOUTHERN', 'Southern'),('TENDERLOIN','Tenderloin'),('ALL', 'All of SF')])
	norm_dist = SelectField('norm_dist',choices=[('neither','None'),('dist_deal','By Deal')])
	freq = SelectField('freq',choices=[('1M','1 Month'),('3M', '3 Months'), ('6M', '6 Months')], default='6M')
