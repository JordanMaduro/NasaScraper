from modules import spider
from modules import utils
import mechanize, sys, math, os, re
from urllib2 import HTTPError, URLError
import urllib2,urllib
from time import sleep
from urlparse import urlparse, parse_qs

class NasaSpider(spider.Spider):
    
    main_url = "http://eol.jsc.nasa.gov/sseop/technical.htm/"
    baseU = "http://eol.jsc.nasa.gov/scripts/sseop/"
    browser = None
    country_to_scrape = None
    number_of_files_to_get = 0
    country_list = []
    result_links = []
    download_links = []
    number_pages = 0
    rate_of_request = 0.5
    
    
    def __init__(self, debug):
        print "Nasa Spider"
        if debug == False:
            return
        self.browser = mechanize.Browser()
        response = None
        try:
            response = self.browser.open(self.main_url)
           
            
        except URLError, ue:
            print utils.bcolors.FAIL + "Error message args: "+str(ue.args)+ " while connecting to: "+self.main_url + utils.bcolors.ENDC
            sys.exit(0)
        except HTTPError, e:
            print utils.bcolors.FAIL + "Error code: "+e.code+ " while connecting to: "+self.main_url + utils.bcolors.ENDC
            sys.exit(0)
        if response != '' and response.code == 200:
            print utils.bcolors.OKGREEN + "Connected to: "+self.browser.title()+ utils.bcolors.ENDC
        #print utils.bcolors.WARNING + "Warning: No active frommets remain. Continue?" + utils.bcolors.ENDC
        #print self.browser.title()
        
    def crawl(self):
        country = self.country_list[int(self.country_to_scrape)]
        print "Find all images for: "+ country
        self.browser["geoncb"] = ["on"]
        self.browser["geon"] = [country]
        response = self.browser.submit()
        #print response.read()
        #return response
        for f in self.browser.forms():
            if f.name == "GoToPage":
                self.browser.select_form(name="GoToPage")
                form = self.browser.form
                control = form.find_control("pagesize", type="hidden")
                control2 = form.find_control("records", type="hidden")
                #print control.name, control.value, control.type
                #print control2.name, control2.value, control2.type
                np = int(math.ceil(float(control2.value) / float(control.value)))
                print "Number of results: " + control2.value
                self._custom_possible_number_results(np)
                print "Possible number of pages: " + str(np)
        if self.number_pages == 0:
            self.number_pages = 1
            
  
    def crawl_all_results(self):
       for i in range(0,self.number_pages):
            self._custom_nextPage()
            self.result_links.extend(list(self.browser.links(url_regex="photo.pl")))
            print len(self.result_links)
    
    def _custom_get_search_form(self, num):
        print "Getting search form"
        self.browser.form = list(self.browser.forms())[num]
        return self.browser.form
        
    def show_options(self):
        print "Here are the options"
        technicalForm = self._custom_get_search_form(1)
        #for form in self.browser.forms():
        #    print "Form name:", form.name
        #    print form
        technicalFormItems = technicalForm.find_control("geon", type="select").items
        op = []
        for item in technicalFormItems:
            op.append(item.name)
        self.country_list = op
        self._list_options(op)
    
    def _list_options(self, list_options):
        for index, item in enumerate(list_options):
            print index, item
    
    def get_option(self):
        self.country_to_scrape = raw_input("Choose a country by number(only), ex: 221 = Netherlands: ")
        
    def _custom_nextPage(self):
        print "Checking for next page"
        for f in self.browser.forms():
            if f.name == "NextPage":
                form = self.browser.select_form(name="NextPage")
                self.browser.submit()

    def _custom_possible_number_results(self, nb):
        self.number_pages = nb
        
    def crawl_download_links(self):
        for i in range(0,len(self.result_links)):
        #for i in range(0,3):
            print "Searching for download link on page number:",i
            
            try :
                self.browser.follow_link(self.result_links[i])
                self.download_links.extend(list(self.browser.links(url_regex="PhotoInfoZip.pl",nr=0)))
                self.browser.back()
            except :
                pass
           
            
    
    def process_downloads(self, directory_path):
        if len(self.download_links) > 0:
            directory = directory_path+"/"+self.country_list[int(self.country_to_scrape)].replace(' ', "_")
            if not os.path.exists(directory):
                os.makedirs(directory)
            for dLink in self.download_links:
                url = self.baseU+dLink.url
                urlParts = parse_qs(urlparse(url)[4])
                fname = urlParts['mission'][0] +'-'+urlParts['roll'][0]+'-'+urlParts['frame'][0]
                print fname
                downloadTarget = directory+'/'+fname+".zip"
                print downloadTarget
                if not os.path.isfile(downloadTarget):
                    print "Activate zip generation on server..."
                    res = urllib2.urlopen(url)
                    print "Downloading with urllib"
                    print "Real download url is in javascript ugh!"
                    #/sseop/temp/ISS022-E-13478.zip"
                    realUrl = "http://eol.jsc.nasa.gov/sseop/temp/"+fname+".zip"
                    try :
                        urllib.urlretrieve(realUrl, downloadTarget)
                    except :
                        pass
                    
                    
                    #f = urllib2.urlopen(realUrl)
                    #chunk_read(f, report_hook=chunk_report)
                    #with open(downloadTarget, "wb") as code:
                       #    code.write(f.read())
                    print "Done downloading:"+ fname + ".zip"
                   
                else:
                    print fname+ ".zip already exists"
    
        
    