import Image
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
import ImageOps
import ImageEnhance
#Set debug state application wide
debug = True


ui  = jui.jUI()
ui.setup({'welcome':'Welcome to jZip v1.0....', 'title':'Unzip v1.0'})
ui.show_setup()
fm = jfileio.FIOManager()
#fm.my_purpose()

#Set folder and set files to clear
folders = ["/var/www/space/images/","/var/www/space/images/processed"]

fm.printIndexList(fm.list_dir(folders[0]))
fm.set_folders(folders,debug)


num = int(raw_input("Choose folder to process:"))
print fm.list_dir(folders[0])[num]
location = folders[0]+"/"+fm.list_dir(folders[0])[num]
print location
imagefiles = fm.find_files(location,fm.JPG_RE)
print imagefiles


do_view = raw_input('Create viewport or processsed!')
if do_view == 'viewport':
    do_view = True
else:
    do_view = False

for zip in imagefiles:
    ziploc = location+"/"+zip
    zipdest = ziploc
    print location+"/"+os.path.splitext(zip)[0]
    if do_view == True:
        outfile = os.path.splitext(zipdest)[0] + ".jpg:viewport"
    else:
        outfile = os.path.splitext(zipdest)[0] + ".jpg:processed"
    if zipdest != outfile:
        try:
            
            im = Image.open(zipdest)
            MAXWIDTH = 800
            s= im.size
            print s
            if do_view == True:
            
                ratio = float(MAXWIDTH) / s[0]
                print ratio
                wi = s[0]*ratio
                print wi
                hi = s[1]*ratio
                print int(hi)
                im.thumbnail((int(wi), int(hi)), Image.ANTIALIAS)
                
            brightness = 1.15
            enhancer = ImageEnhance.Brightness(im)
            bright = enhancer.enhance(brightness)
            contrast = 1.7
            enhancer = ImageEnhance.Contrast(bright)
            im = enhancer.enhance(contrast)
            #im = ImageOps.autocontrast(im)
         
            im.save(outfile, "JPEG")
        except IOError:
            print "cannot create thumbnail for '%s'" % zipdest
    #fm.unzipFile(ziploc, location_to+"/"+os.path.splitext(zip)[0])
    



print "done!"
print fm.list_dir(location)

sys.exit(0)


for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, "JPEG")
        except IOError:
            print "cannot create thumbnail for '%s'" % infile