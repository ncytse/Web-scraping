import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.worldometers.info/coronavirus/"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# this is the html from the given url
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

column_headers = [th.getText() for th in 
                  soup.findAll('tr', limit=2)[0].findAll('th')] #[0] means first row of table

table = soup.find('table', id='main_table_countries_today')
data_rows = table.findAll('tr')[1:] #[1:] means 2nd row of table onward
type(data_rows)  # now we have a list of table rows

country_data = []  # create an empty list to hold all the data

for i in range(len(data_rows)):  # for each table row
    country_row = []  #create an empty list for each country

    # for each table data element from each table row
    for td in data_rows[i].findAll('td'):        
        # get the text content and append to the player_row 
        country_row.append(td.getText())        

    # then append each pick/player to the player_data matrix
    country_data.append(country_row)

df = pd.DataFrame(country_data, columns=column_headers)
df.shape

df.columns = [w.replace('\n', '') for w in df.columns]
#df = df.dropna(how='all')
df['TotalCases']=df['TotalCases'].str.replace(',', '').astype(int)
#df.drop_duplicates(subset ='Country,Other', keep = 'first', inplace = True)
df = df[~df['Country,Other'].str.contains('Total')]
world_index=df.index[df['Country,Other'] == 'World'].tolist()[0] 
df['Country,Other'].replace(r'\n', '', regex=True, inplace=True)
df = df.iloc[world_index+1:]
df.sort_values(by='TotalCases', axis=0, ascending=False, inplace=True)
df.head()

top10_country=df.iloc[:11]['Country,Other']
top10_country
