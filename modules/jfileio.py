import os
import re
import zipfile
class FIOManager():
    
    '''FIOManager takes folder names and allows easy access to
    basic IO functions'''
    
    JPG_RE  = '^.*jpg$'
    HTML_RE  = '^.*html$'
    PNG_RE  = '^.*png$'
    GIF_RE  = '^.*gif$'
    
    ZIP_RE  = '^.*zip$'
    RAR_RE  = '^.*rar$'
    
    folders = []
   
    
    def my_purpose(self):
        print "FIOManager takes folder names and allows easy access to basic IO functions"
    
    def __init__(self):
        print "Creating File IO Manager..."
    
    def set_folders(self, folders_to_set, debug):
        print "Trying to add the following folders:"
        #print self.print_folders(folders_to_set)
        to_add = []
        not_add = []
        
        for folder in folders_to_set:
            if self.folder_exist(folder):
                to_add.append(folder)
                self.folders.append(folder)
                if debug == False:
                    print folder
            else:
                not_add.append(folder)
        
        if len(to_add) > 0 :
                if debug == False:
                    print "Managing these folders:"
                    self.print_folders(to_add)
        if len(not_add) > 0:
                if debug == False:
                    print "Could not add these folders:"
                    self.print_folders(not_add)
            
    def print_folders(self, folders):
        for folder in folders:
            print folder
            
    def folder_exist(self, path):
        return os.path.isdir(path)

    def list_dir(self, dir):
        return  os.listdir(dir)
    
    def find_files(self, dir, extension):
         files_match = []
         for f in os.listdir(dir):
            if re.search('^.*'+extension+'$', f):
                files_match.append(f)
    
         return files_match
        
    def purge(self, dir, files):
        for f in files:
            os.remove(os.path.join(dir, f))
            
   
    def purpose(self):
        print self.my_purpose()
        
    def printIndexList(self, list):
        for index, item in enumerate(list):
            print index, item
        
    def unzipFile(self, zipFileName, unZipTargetDir):
        if not os.path.exists(unZipTargetDir):
            os.makedirs(unZipTargetDir, 0777)
            
        zfObj = zipfile.ZipFile(zipFileName)
        for name in zfObj.namelist():
            if name.endswith(os.path.sep):
                os.makedirs(os.path.join(unZipTargetDir, name))
            else:
                ext_filename = os.path.join(unZipTargetDir, name)
                ext_dir= os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir) : os.mkdir(ext_dir,0777)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfObj.read(name))
                outfile.close()    