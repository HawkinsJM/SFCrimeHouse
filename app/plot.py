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

	def cdplot(self, crime,district):
		print os.getcwd()
		district = district
		crime = crime
		df = pd.read_csv('app/static/data/perd/{}.csv'.format(district.title()))
		tend = df.set_index(pd.to_datetime(df['Unnamed: 0']))
		tend.index.rename('Date', inplace=True)
		tend.drop('Unnamed: 0', axis=1, inplace=True)
		x = tend.index
		y = tend[crime]
		y2 = tend['averageListingPrice'].divide(1000000)
		p = figure(plot_width=800,
		           plot_height=500,
		           title='Plot of {} and Housing Cost in {} District'.format(crime.title(),district.title()),
		              x_axis_label='Date',
		              x_axis_type='datetime',
		              y_axis_label='Count of {} / 6mo'.format(crime.title())
		              )

		minh = tend['averageListingPrice'].min()/1000000
		maxh= tend['averageListingPrice'].max()/1000000

		p.extra_y_ranges = {"foo": Range1d(start=minh-.03, end=maxh+.03)}
		p.add_layout(LinearAxis(y_range_name="foo", axis_label='Mean Price for 2 Bedroom (Millions USD)'), 'right', )
		p.line(x, y, line_width=2, color="red", alpha = .5, legend="{}".format(crime.title()))
		p.line(x, y2, line_width=2, color="blue", line_dash=[4, 4], y_range_name="foo", legend="{} Home Value".format(district))
		p.legend.orientation = "bottom_left"
		# create the HTML elements to pass to template
		figJS,figDiv = components(p,CDN)
		script, div = components(p)
		return script, div
	    #return render_template('plot.html', script=script, div=div)


