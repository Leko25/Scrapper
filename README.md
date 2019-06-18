# Project Title: 
Preprocessing_Scrapper 

## Prequisites: 
-- install xlrd (pip3 install xlrd) 
-- install BeautifulSoup (pip3 install beautifulsoup4)
-- Ensure that the file Breaker_Neutral.xlsx is in current working directory 


# Information: 
This file converts commit ID and Project names found in excel file Neutral_Breaker.xlsx to urls and 
scraps the urls for path names with the key words -- test, util, build. 
It then creates a two pandas data frames neutral and breaker with the columns
1. Project_Name
2. Commit_ID
3. Commit_URL
4. Testing -- Binary
5. Build -- Binary
6. Maintenance -- BInary


### Author: 
Kelechi Ogudu 
kogudu@usc.edu 