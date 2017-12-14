from bs4 import BeautifulSoup
import re
import urllib2
import lxml
import pandas as pd
import os

def scrape_listing(url):
    '''
    This method is used to pull data from html tags. It scrapes from the html file
    to compile into lists which are then passed to a pandas DatFrame and returned
    '''

#take url and spit out a df with labels and values from the listing
    page = open(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    

    #find tags
    listing_labels = soup.findAll('strong', 
        { "class" : "col-lg-6 col-sm-6 col-md-6 col-xs-6"})
    listing_values = soup.findAll('span', 
        { "class" : "col-lg-6 col-sm-6 col-md-6 col-xs-6"})
    

    #pull out text into lists
    label_list = []
    value_list = []
    listing_name = []
    for i, tag in enumerate(listing_labels):
        label_list.append(listing_labels[i].text)
        value_list.append(listing_values[i].text)
        listing_name.append('{0}'.format(os.path.splitext(url)[0]))
    #make listing DatFrame
    list_data = {'labels': label_list, 'values': value_list, 'address': listing_name}    
    listing_df = pd.DataFrame(data = list_data)
    listing_df = listing_df.drop_duplicates() #html file has keys and values listed twice for some reason
    listing_df.to_csv('{0}.csv'.format(os.path.splitext(url)[0]), index=True)
    return listing_df
        
def merge_data(dir):
    '''
    This method nests "scrape_listing" and loops through every .html file in a given directory to scrape the
    listing data and merge them in a dataframe
    '''
    #initialize empty dataframe
    merged_df = pd.DataFrame({'A' : []})
    #loop through all listings in given directory
    for listing in os.listdir(dir):
        if listing.endswith('.html'):
            listing_df = scrape_listing(listing)
            if merged_df.empty: #if empty, set to first listing scrape df
                merged_df = listing_df 
            else: #otherwise, attach the new listing
                merged_df = pd.concat([merged_df, listing_df])
                
        else:
            continue
    #merged_df.to_csv('merged_df.csv') #for debugging
    merged_pivot = merged_df.pivot(index='labels',
                    columns='address', values = 'values')
    #merged_pivot.to_csv('merged_pivot.csv') #for debugging
    
    return merged_pivot

def main():
    cwd = os.getcwd()
    dir = os.path.join(cwd, "listings")
    os.chdir(dir)
    merge_data(dir)
    os.chdir(cwd)
    

if __name__ == "__main__":
   main()



