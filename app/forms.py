from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired
import pickle
import os

class gForm(Form):
	#load districts pickle
	#['BAYVIEW', 'CENTRAL', 'MISSION', 'NORTHERN', 'SOUTHERN', 'TENDERLOIN']
	ctypes = [('KIDNAPPING', 'Kidnapping'), ('WEAPON LAWS', 'Weapon Laws'), ('SECONDARY CODES', 'Secondary Codes'), ('WARRANTS', 'Warrants'), ('PROSTITUTION', 'Prostitution'), ('EMBEZZLEMENT', 'Embezzlement'), ('SEX OFFENSES, NON FORCIBLE', 'Sex Offenses, Non Forcible'), ('LOITERING', 'Loitering'), ('SUICIDE', 'Suicide'), ('DRIVING UNDER THE INFLUENCE', 'Driving Under The Influence'), ('ROBBERY', 'Robbery'), ('BURGLARY', 'Burglary'), ('SUSPICIOUS OCC', 'Suspicious Occ'), ('FAMILY OFFENSES', 'Family Offenses'), ('ASSAULT', 'Assault'), ('FORGERY/COUNTERFEITING', 'Forgery/Counterfeiting'), ('BAD CHECKS', 'Bad Checks'), ('DRUNKENNESS', 'Drunkenness'), ('GAMBLING', 'Gambling'), ('OTHER OFFENSES', 'Other Offenses'), ('RECOVERED VEHICLE', 'Recovered Vehicle'), ('FRAUD', 'Fraud'), ('ARSON', 'Arson'), ('SEX OFFENSES, FORCIBLE', 'Sex Offenses, Forcible'), ('DRUG/NARCOTIC', 'Drug/Narcotic'), ('TRESPASS', 'Trespass'), ('LARCENY/THEFT', 'Larceny/Theft'), ('VANDALISM', 'Vandalism'), ('NON-CRIMINAL', 'Non-Criminal'), ('EXTORTION', 'Extortion'), ('PORNOGRAPHY/OBSCENE MAT', 'Pornography/Obscene Mat'), ('LIQUOR LAWS', 'Liquor Laws'), ('TREA', 'Trea'), ('VEHICLE THEFT', 'Vehicle Theft'), ('STOLEN PROPERTY', 'Stolen Property'), ('BRIBERY', 'Bribery'), ('MISSING PERSON', 'Missing Person'), ('DISORDERLY CONDUCT', 'Disorderly Conduct'), ('RUNAWAY', 'Runaway')]
	with open('app/static/data/perd/dist.pickle', 'rb') as f:
		dist_list = pickle.load(f)
	crime = SelectField('crime',choices=ctypes)
	district = SelectField('district',choices=[('BAYVIEW','Bayview'),('CENTRAL', 'Central'), ('MISSION', 'Mission'), ('NORTHERN', 'Northern'),('SOUTHERN', 'Southern'),('TENDERLOIN','Tenderloin')])
	house_data = BooleanField('house_data', default=False)