import streamlit as st
from datetime import time
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.graph_objs  as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
import numpy as np
import altair as alt
import pickle
from io import BytesIO
import requests

model_link = 'https://github.com/josers18/MSDS498/blob/main/Regressor.pkl?raw=true'
mfile = BytesIO(requests.get(model_link).content)
regressor = pickle.load(mfile)

sns.set_style("darkgrid")


# st.image('https://github.com/josers18/MSDS498/raw/main/a51.png')
# st.title("Home Pricing Analysis Tool")

# st.markdown("""
#	The data set contains information about money spent on advertisement and their generated sales. Money
#	was spent on TV, radio and newspaper ads.
#	## Problem Statement
#	Sales (in thousands of units) for a particular product as a function of advertising budgets (in thousands of
#	dollars) for TV, radio, and newspaper media. Suppose that in our role as statistical consultants we are
#	asked to suggest.
#	Here are a few important questions that you might seek to address:
#	- Is there a relationship between advertising budget and sales?
#	- How strong is the relationship between the advertising budget and sales?
#	- Which media contribute to sales?
#	- How accurately can we estimate the effect of each medium on sales?
#	- How accurately can we predict future sales?
#	- Is the relationship linear?
#	We want to find a function that given input budgets for TV, radio and newspaper predicts the output sales
#	and visualize the relationship between the features and the response using scatter plots.
#	The objective is to use linear regression to understand how advertisement spending impacts sales.

#	### Data Description
#	TV
#	Radio
#	Newspaper
#	Sales
# """)


@st.cache()
# defining the function which will make the prediction using the data which the user inputs
def get_data():
	return pd.read_csv("https://github.com/josers18/MSDS498/raw/main/Autin_Report_Set.csv")


dfr = get_data()


def prediction(lotSizeSqFt, livingAreaSqFt, avgSchoolDistance, avgSchoolRating, avgSchoolSize, MedianStudentsPerTeacher,
			   Bathrooms, Bedrooms, zip, Stories, BuiltAfter2k, HasPatioPorch, hasGarage, hasAssociation,
			   hasSecurityFeatures):
	# Pre-processing user input
	if BuiltAfter2k == "Yes":
		BuiltAfter2k = 1
	else:
		BuiltAfter2k = 0

	if HasPatioPorch == "Yes":
		HasPatioPorch = 1
	else:
		HasPatioPorch = 0

	if hasGarage == "Yes":
		hasGarage = 1
	else:
		hasGarage = 0

	if hasAssociation == "Yes":
		hasAssociation = 1
	else:
		hasAssociation = 0

	if hasSecurityFeatures == "Yes":
		hasSecurityFeatures = 1
	else:
		hasSecurityFeatures = 0

	# Making predictions
	prediction = regressor.predict(
		[[lotSizeSqFt, livingAreaSqFt, avgSchoolDistance, avgSchoolRating, avgSchoolSize, MedianStudentsPerTeacher,
		  Bathrooms, Bedrooms, zip, Stories, BuiltAfter2k, HasPatioPorch, hasGarage, hasAssociation,
		  hasSecurityFeatures]])

	return prediction


# this is the main function in which we define our webpage
def main():
	# front end elements of the web page
	html_temp = """ 
	<div style="text-align: center;"><img src="https://github.com/josers18/MSDS498/raw/main/a51.png"/></div>
    <div> 
    <h1 style ="color:#333333;text-align:left;">Home Pricing Prediction Tool</h1> 
    </div> 
    """

	# display the front end aspect
	st.markdown(html_temp, unsafe_allow_html=True)

	# following lines create boxes in which user can enter data required to make prediction
	st.sidebar.image('https://github.com/josers18/MSDS498/raw/main/slack-imgs.com.png', width=200)
	st.sidebar.title("Model Prediction Options")
	zip = st.sidebar.selectbox("Property Zip Code", (
	'78617', '78619', '78652', '78653', '78660', '78701', '78702', '78703', '78704', '78705', '78717', '78719', '78721',
	'78722', '78723', '78724', '78725', '78726', '78727', '78728', '78729', '78730', '78731', '78732', '78733', '78734',
	'78735', '78736', '78737', '78738', '78739', '78741', '78742', '78744', '78745', '78746', '78747', '78748', '78749',
	'78750', '78751', '78752', '78753', '78754', '78756', '78757', '78758', '78759'))
	lotSizeSqFt = st.sidebar.number_input("Lot size of Property", min_value=300, max_value=1000000, format='%i')
	livingAreaSqFt = st.sidebar.number_input("Living Area of Property", min_value=300, max_value=1000000, format='%i')
	Bedrooms = st.sidebar.slider("Total Bedrooms", 1, 20, step=1)
	Bathrooms = st.sidebar.slider("Total Bathrooms", 1, 25, step=1)
	Stories = st.sidebar.slider("Total Stories", 1, 4, step=1)
	avgSchoolDistance = st.sidebar.slider("Avg. School Distance", 0, 9)
	avgSchoolRating = st.sidebar.slider("Avg. School Rating", 2, 10)
	avgSchoolSize = st.sidebar.slider("Avg. School Size", 400, 1900, step=50)
	MedianStudentsPerTeacher = st.sidebar.slider("Students Per Teacher", 10, 20, step=1)
	BuiltAfter2k = st.sidebar.radio('Was the Property built after 2000?', ("Yes", "No"))
	HasPatioPorch = st.sidebar.radio('Does the Property have a Patio or Porch?', ("Yes", "No"))
	hasGarage = st.sidebar.radio('Does the Property have a Garage?', ("Yes", "No"))
	hasAssociation = st.sidebar.radio('Does the property have an Association?', ("Yes", "No"))
	hasSecurityFeatures = st.sidebar.radio('Does the property have any Security Features?', ("Yes", "No"))
	result = ""

	# when 'Predict' is clicked, make the prediction and store it
	if st.sidebar.button("Predict"):
		result = prediction(lotSizeSqFt, livingAreaSqFt, avgSchoolDistance, avgSchoolRating, avgSchoolSize,
							MedianStudentsPerTeacher, Bathrooms, Bedrooms, zip, Stories, BuiltAfter2k, HasPatioPorch,
							hasGarage, hasAssociation, hasSecurityFeatures)
		predprice = 10 ** result
		# printprice = f"Your Optimal Home Listing Price is $**{float(predprice):,.0f}**"
		# st.markdown(printprice)
		st.subheader('Your Optimal Home Listing Price is $ {:,.0f}'.format(float(predprice)))
		report_title =f"Area Report for Zipcode **{zip}**"
		st.markdown(report_title)
		#st.write(zip)

		charts = dfr[dfr['zip'] == int(zip)]
		alt_area = alt.Chart(charts, title='Price Trends in the Area')\
			.mark_area(line={'color': 'darkorange'},	color=alt.Gradient(gradient='linear',stops=[alt.GradientStop(color='white', offset=0), alt.GradientStop(color='darkorange', offset=1)],x1=1,x2=1,y1=1,y2=0))\
			.encode(
			alt.X('latest_saledate:T', title='Sale Date'),
			alt.Y('price:Q', title='Sale Price'))\
		.properties(
			width=700
		)
		st.altair_chart(alt_area)

		alt_box = alt.Chart(charts, title='Price Distribution by Sales Year')\
			.mark_boxplot()\
			.encode(
			alt.X('latest_saleyear:O', title='Sale Year'),
			alt.Y('price:Q', title='Price Distribution')
		).properties(width=700)
		st.altair_chart(alt_box)
		map_chart = charts.filter(['price','latitude','longitude'],axis=1)
		st.map(map_chart)

	# st.success('Your upper bound is {}'.format((predprice) + (1.96*np.std(predprice))))
	# print(predprice)

if __name__ == '__main__':
	main()


# ('78617','78619','78652','78653','78660','78701','78702','78703','78704','78705','78717','78719','78721','78722','78723','78724','78725','78726','78727','78728','78729','78730','78731','78732','78733','78734','78735','78736','78737','78738','78739','78741','78742','78744','78745','78746','78747','78748','78749','78750','78751','78752','78753','78754','78756','78757','78758','78759')
