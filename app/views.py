import os
from flask import render_template, flash, redirect
from app import app
from .forms import bcForm, bdForm
from .plot import gPlot
#from bokeh.embed import file_html, components

# index view function suppressed for brevity
# imports for Bokeh plotting


@app.route('/')
def main():
	return redirect('/welcome')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/welcome')
def welcome():
	stitle = "Welcome"
	return render_template('welcome.html',stitle=stitle)

@app.route('/about')
def about():
	stitle = "About"
	return render_template('about.html')

@app.route('/contact')
def contact():
	stitle = "Contact"
	return render_template('Contact.html')

@app.route('/plot1')
def plot1():
	title1 = "All Crimes in All Districts"
	plot1 = gPlot().bdplot(['ALL'], 'ALL', 'neither', '6M')
	script1, div1 = plot1
	return render_template('plots.html', t1 = title1, script =script1, p1=div1)

@app.route('/plot2')
def plot2():
	title1 = "Some Crimes Change with Housing Cost"
	plot1 = gPlot().bdplot(['LARCENY-THEFT','NON-CRIMINAL'], 'NORTHERN', 'crime_ind', '6M')
	script1, div1 = plot1

	return render_template('plots.html', t1 = title1, script =script1, p1=div1)

@app.route('/plot3')
def plot3():
	title1 = "Some Crimes Don't Change with Housing Cost"
	plot1 = gPlot().bdplot(['DRUNKENNESS','FRAUD','MISSING PERSON','WARRANTS','ROBBERY'], 'NORTHERN', 'crime_ind', '6M')
	script1, div1 = plot1
	return render_template('plots.html', t1 = title1, script =script1, p1=div1)

@app.route('/bdist', methods=['GET', 'POST'])
def bdist():
	form = bdForm()
	try:
		if form.validate_on_submit():
			crime = form.crime_m.data
			dist = str(form.district_o.data)
			nc = str(form.norm_crime_house.data)
			frq = str(form.freq.data)
			plot = gPlot().bdplot(crime, dist, norm_crime=nc, freq=frq)
			script, div = plot
			return render_template('bdist.html',
	                           form=form,script=script, div=div)
	except Exception as ex:
		print "ERROR: index failed"
		print ex
		pass
	return render_template('bdist.html',form=form)

@app.route('/bcrime', methods=['GET', 'POST'])
def bcrime():
	form = bcForm()
	try:
		if form.validate_on_submit():
			crime = str(form.crime_o.data)
			dist = form.district_m.data
			nd = str(form.norm_dist.data)
			frq = str(form.freq.data)
			plot = gPlot().bcplot(crime, dist, nd, freq=frq)
			script, div = plot
			return render_template('bcrime.html',
	                           form=form,script=script, div=div)
		else:
			pass
	except Exception as ex:
		print "ERROR: index failed"
		print ex
		pass
	return render_template('bcrime.html',form=form)