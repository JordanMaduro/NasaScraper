#Get Mechanize and  supporting modules
import mechanize, re, math, sys, os
#Get URL and HTTP Modules
import urlparse, urllib, urllib2

#Get UI module and ImageDownload modules
from modules import spider
from modules import jui
from modules import jfileio
from scrapers import gap
from modules import utils

import os

#Set debug state application wide
debug = True


ui  = jui.jUI()
ui.setup({'welcome':'Welcome to jScaper v1.0....', 'title':'Scraper v1.0'})
ui.show_setup()
fm = jfileio.FIOManager()
#fm.my_purpose()

#Set folder and set files to clear
folders = ["temp","temp/downloads","temp/processed"]
#print fm.list_dir("temp")
fm.set_folders(folders,debug)
location = folders[2]

#print fm.folders

#Setup Spider
nasa_spider = gap.NasaSpider(debug)

nasa_spider.show_options()
nasa_spider.get_option()
print nasa_spider.country_list[int(nasa_spider.country_to_scrape)]
nasa_spider.crawl()
#nasa_spider.number_pages = 1
nasa_spider.crawl_all_results()

print "Number of Links found:",len(nasa_spider.result_links)
nasa_spider.crawl_download_links()
print "Number of Zip Download links found:",len(nasa_spider.download_links)
nasa_spider.process_downloads(fm.folders[1])
#doSearch(options[int(get_option)])
#fm.purge(location,fm.find_files(location,'jpg'))







#Set up data structures

#Start app loop

#Get user info
