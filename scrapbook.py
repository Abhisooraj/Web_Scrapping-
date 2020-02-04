from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://online.ulbharyana.gov.in/eforms/PropertyTax.aspx'

req = requests.post(url)
data=req.text

soup = BeautifulSoup(data, "html.parser")
final=[]
get_list  = soup.find_all('option')   #gets list of all <option> tag
for element in get_list :
    cities = element.select("option")
    final.append(cities)
print(final)


