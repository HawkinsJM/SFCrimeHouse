import os
from flask import render_template, flash, redirect
from app import app
from .forms import gForm
from .plot import gPlot
#from bokeh.embed import file_html, components

# index view function suppressed for brevity
# imports for Bokeh plotting


@app.route('/')
def main():
	return redirect('/index')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

@app.route('/index', methods=['GET', 'POST'])
def login():
	stitle = "Select Plot Attributes"
	gtitle = ''
	form = gForm()
	try:
		if form.validate_on_submit():
			crime = str(form.crime.data)
			dist = str(form.district.data)
			plot = gPlot().cdplot(crime,dist)
			gtitle = "Housing Cost and {} in the {} District".format(crime.title(),dist.title())
			script, div = plot
			print "Hello"
			return render_template('index.html',
	                           stitle=stitle,gtitle = gtitle,
	                           form=form,script=script, div=div)
		else:
			pass
	except Exception as ex:
		print "ERROR: index failed"
		print ex
		pass
	return render_template('index.html',stitle=stitle,form=form)

@app.route('/plot')
def plot():
	return render_template('index.html', distr = dist, title=tip, form=form)