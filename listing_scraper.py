from bs4 import BeautifulSoup
import re
import urllib2
import lxml
import pandas as pd
import os
from mapstest import get_latlong
def scrape_listing(url):

#take url and spit out a df with labels and values from the listing
    page = open(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    
    #print soup.prettify()[0:1000]
    #find tags
    listing_labels = soup.findAll('strong', 
        { "class" : "col-lg-6 col-sm-6 col-md-6 col-xs-6"})
    listing_values = soup.findAll('span', 
        { "class" : "col-lg-6 col-sm-6 col-md-6 col-xs-6"})
    

    #pull out text into lists
    label_list = []
    value_list = []
    for i, tag in enumerate(listing_labels):
        label_list.append(listing_labels[i].text)
        value_list.append(listing_values[i].text)
       # print label_list[i], ":", value_list[i]
    
    list_data = {'labels': label_list, 'values': value_list}    
    listing_df = pd.DataFrame(data = list_data)
    listing_df = listing_df.drop_duplicates()
    #listing_df.index = listing_df['labels']
    #listing_df.drop('labels')
    listing_df.to_csv('{0}.csv'.format(os.path.splitext(url)[0]), index=True)
    return listing_df
        
# def merge_data(dir):

    # merged_df = pd.DataFrame({'A' : []})
    # for listing in os.listdir(dir):
        
        # if listing.endswith('.html'):
            # print listing
            # listing_df = scrape_listing(listing)
            # if merged_df.empty:
                # print "EMPTY"
                # merged_df = listing_df 
            # if len(merged_df.columns)<2:
                ## merged_df = pd.concat([merged_df, listing_df], 
                 #   # axis=1, join_axes=[merged_df.index])
                ## merged_df = pd.merge(merged_df, listing_df, on=['labels', 'values'] , how='outer')
                ## merged_df = merged_df.drop_duplicates()
                
                # merged_df = merged_df.set_index('labels').join(
                    # listing_df.
                    # set_index('labels'),how='outer', lsuffix='_merged', 
                    # rsuffix='_listing')
                # print 'merged'
            
            # else:  
                # merged_df = merged_df.join(
                    # listing_df.
                    # set_index('labels'),how='outer', lsuffix='_merged', 
                    # rsuffix='_listing')
            # continue

    # merged_df.to_csv('merged_df.csv')

def merge_data2(dir):
    
    merged_df = pd.DataFrame({'A' : []})
    for listing in os.listdir(dir):
        
        if listing.endswith('.html'):
            print listing
            listing_df = scrape_listing(listing)
            listing_df.set_index('labels', inplace=True)

            if merged_df.empty:
                print "EMPTY"
                merged_df = listing_df 
                #merged_df.set_index('labels')
            else:
                merged_df = pd.concat([merged_df, listing_df], axis=1)
    #latlong = pd.DataFrame({'Lat/Long':merged_df.loc['Address'].apply(get_latlong)})
    #print latlong
    #merged_df = merged_df.append(merged_df.loc['Address'].apply(get_latlong))
    #merged_df = merged_df.append(latlong)
    merged_df.to_csv('merged_df.csv')
def main():
    #listing_url = r"archstreet.html"
    dir = 'C:\Users\Tom\Desktop\mls_scraper\listings'
    cwd = os.getcwd()
    os.chdir(dir)
    merge_data2(dir)
    #latlong = get_latlong("466 Ontario Street, Albany, New York")
    #print latlong
    os.chdir(cwd)
    
if __name__ == "__main__":
    main()



