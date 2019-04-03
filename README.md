This file capture the daily FX rate from the web to dataframe

#Web crawling for FX rate
#'https://www.xe.com/currencytables/?from=USD&date=YYYY-MM-DD'
# the (T-2) day figure will be update
# first check if the file in previous quarter exist
  #if Yes
    #max date is the previous day (date diff = 1), update current day only
    #max date is the not previous day (date diff > 1), update since file max date +1
  #if No
    #Check if max date of previous quarter file equals to previous quarter end date
        #if Yes
          #work for current day
        #if No
          #work from "file max date +1" to quarter end, and then open file for current quarter and update current day    
    #save file as YYYY_Qx
