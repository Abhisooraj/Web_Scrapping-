try:
	import pandas as pd 
	import numpy as np 
	import html
	from bs4 import BeautifulSoup
	import requests
	import pandas as pd
	import csv
except NameError:
	print("Something went wrong please check for importing libraries")
else:
	print("Nothing went wrong")

session=requests.session()

def parse_list_value(html_pages,id):

	"""
	Given a response object, parse the list
	of MC Names
	"""
	col = html_pages.find('select', id=id)
	col_all = col.select('option')
	list_values_mc_name=[]
	for link in col_all:
		list_values_mc_name.append(link['value'])
	# print(list_values_mc_name[1:])
	return(list_values_mc_name[1:])

def parse_list_options(html_pages, id):
	
	col = html_pages.find('select', id=id)
	col_all = col.select('option')
	list_options_mc_name=[]
	for link in col_all:
		list_options_mc_name.append(link.text)
	# print(list_options_mc_name[1:])
	return(list_options_mc_name[1:])


def response(url):
	url_get=session.get(url)
	# print(url_get)
	html_page = BeautifulSoup(url_get.content, 'lxml')
	return html_page 



# for values of Headers
def get_value (html_page, event_target,mc_type=None,mc_name=None,zone_name=None,colony_name=None):

	# dictionary
	form_data = {} 
	form_data['__VIEWSTATE']=view_state(html_page,'__VIEWSTATE')
	form_data['__EVENTTARGET']=event_target 
	if mc_type:
		form_data['ddlMcType'] = mc_type
	if mc_name:
		form_data['ddlMCCodeS'] = mc_name
	if zone_name:
		form_data['ddlZone'] = zone_name
	if colony_name:
		form_data['ddlColony']=colony_name
	# print(form_data[event_target])
	return(form_data)

def view_state(html_page,name):
	val= html_page.findAll("input", {"type": "hidden", "name": "__VIEWSTATE"})
	# print(val)
	data2=[]
	for link in val:
		data2.append(link['value'])
	return data2[0]


def main():
	final_list={}
	output_dict={}
	df_list=[]

	url1= 'https://online.ulbharyana.gov.in/eforms/PropertyTax.aspx'
	page1=response(url1)
	list_of_options_mc_type = parse_list_options(page1,'ddlMcType')
	list_of_mc_ty= parse_list_value(page1,'ddlMcType')
	list_of_mc_type= ['COMM','COUN']
	list_of_mc_type = [s for s in list_of_mc_type if any(xs in s for xs in list_of_mc_type)]

	for mc_ty in list_of_mc_type:

		db= get_value(page1,'ddlMcType',mc_ty)
		save=session.post(url1,data=db)
		list_of_mc_names_options = parse_list_options(BeautifulSoup(save.content, 'lxml'),'ddlMCCodeS')
		list_of_mc_names= parse_list_value(BeautifulSoup(save.content, 'lxml'),'ddlMCCodeS')

		## list_of_mc_names = [(23, Aasandh), (45, Something else), 51, 1]

		for mc_name in list_of_mc_names:
			html_page_zone_name = BeautifulSoup(save.content, 'lxml')
			db_new = get_value(html_page_zone_name, 'ddlMCCodeS',mc_ty,mc_name)
			final_zone_names = session.post(url1,data=db_new)
			list_of_zone_names_options = parse_list_options(BeautifulSoup(final_zone_names.content, 'lxml'),'ddlZone')
			list_of_zone_names= parse_list_value(BeautifulSoup(final_zone_names.content, 'lxml'),'ddlZone')

			for zone_name in list_of_zone_names:
				html_page_colony_name= BeautifulSoup(final_zone_names.content,'lxml')
				zone_new= get_value(html_page_colony_name,'ddlColony',mc_ty,mc_name,zone_name)
				final_colony_names=session.post(url1,data=zone_new)
				list_of_colony_names_options= parse_list_options(BeautifulSoup(final_colony_names.content,'lxml'),'ddlColony')
				list_of_colony_names= parse_list_value(BeautifulSoup(final_colony_names.content,'lxml'),'ddlColony')
				
				for colony in list_of_colony_names_options:
					row = {"mc_name":mc_name, "mc_type":mc_ty,"zone_name":zone_name,"colony_name":colony}
					df_list.append(row)

	df = pd.DataFrame(df_list)
	print(df.shape)
	print(df.head())


				

    				
main()

