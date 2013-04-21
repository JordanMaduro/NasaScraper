#UI module for interacting with scrapers

class jUI():
    def __init__(self):
        print "Setting up new UI"
    
    def setup(self, settings):
        self.title = settings['title']
        self.welcome = settings['welcome']
        
    def show_setup(self):
        print self.title
        print self.welcome
        