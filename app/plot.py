import pandas as pd
import sys
import os
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.models import LinearAxis, Range1d

class gPlot:
	# def __int__(self,crime,district):
	# 	self.crime = crime
	# 	self.district = district

	def bdplot(self, crime, district, norm_crime='neither', freq = '6M'):
		norm_crime = str(norm_crime)
		frq = freq
		print frq

		district = district
		crime = list(crime)
		#Pull district file
		fname = 'app/static/data/perd/{}-{}.csv'.format(district.upper(),frq.upper())
		df = pd.read_csv(fname)
		dsdf = df.set_index(pd.to_datetime(df['Unnamed: 0']))
		dsdf.index.rename('Date', inplace=True)
		dsdf.drop('Unnamed: 0', axis=1, inplace=True)

		#Pull all city file
		fname = 'app/static/data/perd/{}-{}.csv'.format('ALL',frq.upper())
		df = pd.read_csv(fname)
		sfdf = df.set_index(pd.to_datetime(df['Unnamed: 0']))
		sfdf.index.rename('Date', inplace=True)
		sfdf.drop('Unnamed: 0', axis=1, inplace=True)

		color_list = ['blue','red','green','orange','purple','teal','brown']
		ccl = zip(crime[:6],color_list)
		x = dsdf.index

		y2 = dsdf['averageListingPrice'].divide(1000000)
		p = figure(plot_width=1000,
		           plot_height=600,
		           title='Plot of Crimes and Housing Cost in {} District'.format(district.title()),
		              x_axis_label='Date',
		              x_axis_type='datetime'
		              )

		#Crime plots
		for i in ccl:
			if norm_crime=='crime_ind':
				print "plotting crime dist"
				dc = dsdf[i[0]]
				y = (dc - dc.mean()) / (dc.max() - dc.min())
				p.yaxis.axis_label = "Crime Normalized Within Distrcit / {}".format(frq)
			if norm_crime=='crime_sf':
				print "plotting crime sf"
				dc = dsdf[i[0]]
				cc = sfdf[i[0]]
				#this finds the crime in a district normalized by occurances of that crime in the city
				y = (dc / cc)
				p.yaxis.axis_label = "Percentage of Crimes Occuring in Dist. / {}".format(frq)
			if norm_crime=='crime_deal':
				print "plotting crime deal"
				dc = dsdf[i[0]]
				cc = sfdf[i[0]]
				dh = dsdf['averageListingPrice']
				ch = sfdf['averageListingPrice']
				y = 1/((dc*dh)/(cc*ch))
				p.yaxis.axis_label = "Deal Index for Crimes / {}".format(frq)
			if norm_crime=='neither':
				print "plotting neither"
				y = dsdf[i[0]]
				p.yaxis.axis_label = "Count of Crimes / {}".format(frq)
			p.line(x, y, line_width=4, color=i[1], alpha = .7, legend="{}".format(str(i[0]).title()))

		#House plots
		minh = dsdf['averageListingPrice'].min()/1000000
		maxh= dsdf['averageListingPrice'].max()/1000000
		p.extra_y_ranges = {"foo": Range1d(start=minh-.03, end=maxh+.03)}
		p.add_layout(LinearAxis(y_range_name="foo", axis_label='Mean Price for 2 Bedroom (Millions USD)'), 'right', )
		p.line(x, y2, line_width=5, color="black", line_dash=[4, 4], y_range_name="foo", legend="{} Home Value".format(district.title()))
		
		p.legend.orientation = "bottom_left"
		# create the HTML elements to pass to template
		figJS,figDiv = components(p,CDN)
		script, div = components(p)
		return script, div
		#return render_template('plot.html', script=script, div=div)

	def bcplot(self, crime, dist, norm_dist='neither', freq = '6M'):
		frq = freq
		nd = norm_dist
		districts = list(dist)
		crime = crime
		fname = 'app/static/data/perc/{}-{}.csv'.format(crime.upper(),frq.upper())
		df = pd.read_csv(fname)
		dsdf = df.set_index(pd.to_datetime(df['Unnamed: 0']))
		dsdf.index.rename('Date', inplace=True)
		dsdf.drop('Unnamed: 0', axis=1, inplace=True)
		color_list = ['blue','red','green','orange','purple','teal','brown']
		dcl = zip(districts[:6],color_list)

		x = dsdf.index

		#Pull all city crime and house file
		fname = 'app/static/data/perd/{}-{}.csv'.format('ALL',frq.upper())
		df = pd.read_csv(fname)
		sfdf = df.set_index(pd.to_datetime(df['Unnamed: 0']))
		sfdf.index.rename('Date', inplace=True)
		sfdf.drop('Unnamed: 0', axis=1, inplace=True)

		#Pull all district house file
		fname = 'app/static/data/AllDistHouse-{}.csv'.format(frq.upper())
		df = pd.read_csv(fname)
		adh = df.set_index(pd.to_datetime(df['weekEndingDate']))
		adh.index.rename('Date', inplace=True)
		#adh.drop('Unnamed: 0', axis=1, inplace=True)

		p = figure(plot_width=1000,
	               plot_height=600,
	               title='Plot of {} in District(s)'.format(crime.title()),
	                  x_axis_label='Date',
	                  x_axis_type='datetime'
	                  #y_axis_label='Count of {} / 6mo'.format(crime.title())
	                  )

		for i in dcl:
			if nd=='dist_deal':
				print "plotting dist deal"
				district_crime = dsdf[i[0]]
				city_crime = sfdf[crime.upper()]
				dh = adh[i[0]]
				ch = sfdf['averageListingPrice']
				y = 1/((district_crime*dh)/(city_crime*ch))
				p.yaxis.axis_label = "Deal Index for {} / {}".format(crime.title(),frq)
			if nd=='neither':
				print "plotting neither"
				y = dsdf[i[0]]
				p.yaxis.axis_label = "Count of {} / {}".format(crime.title(),frq)
				#p.y_axis_label='Count of {} / {}'.format(crime.title(),frq)
			p.line(x, y, line_width=4, color=i[1], alpha = .7, legend="{}".format(i[0].title()))

		p.legend.orientation = "bottom_left"
	    # create the HTML elements to pass to template
		figJS,figDiv = components(p,CDN)
		script, div = components(p)
		return script, div