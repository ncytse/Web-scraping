from urllib.request import urlopen
import urllib.parse, urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
import math
from openpyxl import load_workbook
import xlrd
import os
import numpy as np
import glob

#https://stackoverflow.com/questions/27115803/urllib-error-urlerror-urlopen-error-unknown-url-type-https
#https://stackoverflow.com/questions/28376506/urllib-https-request-urlopen-error-unknown-url-type-https
#https://stackoverflow.com/questions/51038268/python3-6-5-urllib-error-urlerror-urlopen-error-unknown-url-type-https
#https://blacksaildivision.com/how-to-install-openssl-on-centos

today_date = datetime.date.today()
d = datetime.timedelta(1)
end_date = today_date - d*2

quarter_dict = {'Q1': datetime.date(end_date.year,3,31),
                'Q2': datetime.date(end_date.year,6,30),
                'Q3': datetime.date(end_date.year,9,30),
                'Q4': datetime.date(end_date.year-1,12,31)
               }

def find_prev_quarter(dt):
    prev_quarter_map = ((4, -1), (1, 0), (2, 0), (3, 0))
    quarter, yd = prev_quarter_map[(dt.month - 1) // 3]
    return (str(dt.year + yd) + '_Q'+ str(quarter))

def get_quarter(d):
    
    prev_quarter = find_prev_quarter(d)
    current_quarter = "%d_Q%d" % (d.year, math.ceil(d.month/3))
        
    return prev_quarter, current_quarter

prev_quarter, current_quarter = get_quarter(end_date)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
        
def create_df(quarter, start_date, end_date, file_exist):

    #Update current file(if any) or create a new file
    if file_exist == True:
    
        file = 'FX Rate '+quarter+'.xlsx'
        book = load_workbook(file)
        writer = pd.ExcelWriter(file, engine = 'openpyxl')
        writer.book = book
        
    else:
        
        writer = pd.ExcelWriter('FX Rate '+quarter+'.xlsx')
        
    #create df
    for date in daterange(start_date, end_date+d):
    
        str_date = str(date.year)+'-'+'{:02d}'.format(date.month)+'-'+'{:02d}'.format(date.day)
        url_1 = 'https://www.xe.com/currencytables/?from=USD&date='
        
        #url = urllib.parse.urljoin(url_1, str_date)
        url = url_1+str_date
        
        # this is the html from the given url
        html = urlopen(url)

        soup = BeautifulSoup(html, 'html.parser')

        column_headers = [th.getText() for th in 
                          soup.findAll('tr', limit=1)[0].findAll('th')] #[0] means first row of table
        column_headers = [re.sub("[^ \w]"," ",x).strip() for x in column_headers]

        data_rows = soup.findAll('tr')[1:] #[1:] means 2nd row of table onward
        type(data_rows)  # now we have a list of table rows

        country_data = []  # create an empty list to hold all the data

        for i in range(len(data_rows)):  # for each table row
            country_row = []  # create an empty list for each country

            # for each table data element from each table row
            for td in data_rows[i].findAll('td'):        
                # get the text content and append to the country_row 
                country_row.append(td.getText())        

            # then append each country to the country_data matrix
            country_data.append(country_row)

        df = pd.DataFrame(country_data, columns=column_headers)
    
        df = df[df['Currency code'].str.len() == 3]
        df = df.drop(['Units per USD'], axis=1)
        df['Date'] = str(date.year) + '{:02d}'.format(date.month) + '{:02d}'.format(date.day)
        df = df[['Date', 'Currency code', 'Currency name', 'USD per Unit']]
        df['Date']=df['Date'].astype('int')
        df['USD per Unit']=df['USD per Unit'].astype('float')
    
        df.to_excel(writer,str(date.year) + '{:02d}'.format(date.month) + '{:02d}'.format(date.day), index=False)

    writer.save()
    
#Check if file exist  
if os.path.isfile('FX Rate '+current_quarter+'.xlsx') == True:
    
    #Check for max date in excel
    xls = xlrd.open_workbook('FX Rate '+current_quarter+'.xlsx', on_demand=True)
    max_date_tab = xls.sheet_names()[-1]
    excel_max_date = datetime.date(int(max_date_tab[0:4]),int(max_date_tab[4:6]),int(max_date_tab[-2:]))
    
    #Create start date
    if end_date - excel_max_date > d:
        start_date = excel_max_date + d
    else:
        start_date = end_date
        
    create_df(current_quarter, start_date, end_date, True)

else:
    
    start_date = quarter_dict[prev_quarter[-2:]]+d
    create_df(current_quarter, start_date, end_date, False)
           
    #Check if previous quarter excel done
    xls = xlrd.open_workbook('FX Rate '+prev_quarter+'.xlsx', on_demand=True)
    max_date_tab = xls.sheet_names()[-1]
    excel_max_date = datetime.date(int(max_date_tab[0:4]),int(max_date_tab[4:6]),int(max_date_tab[-2:]))
        
    #check previous excel_max_date equals to quarter end
    if excel_max_date < quarter_dict[prev_quarter[-2:]]:
        
        print('Previous file',prev_quarter, 'also need to update for period ',excel_max_date+d, 'to',quarter_dict[prev_quarter[-2:]])
        
        #finish the previous excel
        create_df(prev_quarter, excel_max_date+d, quarter_dict[prev_quarter[-2:]], True)
        
####################################create monthly average file####################################
df_avg = pd.DataFrame(columns=['Date', 'Currency code', 'Currency name', 'USD per Unit'])

for filename in glob.iglob('FX Rate '+str(end_date.year)+'_Q*.xlsx', recursive=True):

    tabs = pd.ExcelFile(filename).sheet_names
    
    for tab in tabs:
        df_daily = pd.read_excel(filename, sheet_name=tab)
        df_avg = df_avg.append(df_daily)

df_avg['Month'] =  df_avg['Date'].map(lambda x: str(x)[:-2])

result = pd.pivot_table(df_avg, values='USD per Unit', index=['Currency code', 'Currency name'], columns=['Month'], aggfunc=np.mean)

writer = pd.ExcelWriter('FX Rate Monthly Average.xlsx')
result.to_excel(writer)
writer.save()
