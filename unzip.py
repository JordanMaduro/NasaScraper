import zipfile
import os.path
#Get Supporting modules
import  re, math, sys, os
#Get URL and HTTP Modules
import urlparse, urllib, urllib2

#Get UI module and ImageDownload modules
from modules import jui
from modules import jfileio
from modules import utils

import os

#Set debug state application wide
debug = True


ui  = jui.jUI()
ui.setup({'welcome':'Welcome to jZip v1.0....', 'title':'Unzip v1.0'})
ui.show_setup()
fm = jfileio.FIOManager()
#fm.my_purpose()

#Set folder and set files to clear
folders = ["temp","temp/downloads","temp/processed"]

fm.printIndexList(fm.list_dir(folders[1]))
fm.set_folders(folders,debug)
num = int(raw_input("Choose folder to unzip: "))
print fm.list_dir(folders[1])[num]
location = folders[1]+"/"+fm.list_dir(folders[1])[num]
print location
location_to = folders[2]+"/"+fm.list_dir(folders[1])[num]
print location_to
zipfiles = fm.find_files(location,fm.ZIP_RE)
print zipfiles
for zip in zipfiles:
    ziploc = location+"/"+zip
    zipdest = location_to
    print location_to+"/"+os.path.splitext(zip)[0]
    fm.unzipFile(ziploc, location_to+"/"+os.path.splitext(zip)[0])



print "done!"
print fm.list_dir(location_to)




