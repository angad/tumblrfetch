#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#					Version 2, December 2004
#
#Copyright (C) 2011 Angad Singh <angad@anagd.sg>
#
#Everyone is permitted to copy and distribute verbatim or modified
#copies of this license document, and changing it is allowed as long
#as the name is changed.
#
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.
#

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from urllib import urlopen

content = 0

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(content)
        self.response.out.write("""
                  <html>
                    <body>
                      <form action="/fetch" method="post">
                        <div>Name of Tumblr Blog: <input type ="text" name="url"/></div>
                        <div>Get upto (pages): <input type = "text" name = "pages"/></div>
                        <div><input type="submit" value="Get"></div>
                      </form>
                    </body>
                      </html>""")


class fetch(webapp.RequestHandler):
    def post(self):
        page_count = 0
        pages = int(self.request.get('pages'))
        look_for = '<img src="'

        while (page_count!=pages):
            url = 'http://' + self.request.get('url') + '.tumblr.com/page/' + str(page_count+1)
            content = urlopen(url).read()
            page_count+=1
            start = 1
            while (start != -1 ):
                start = content.find(look_for)
                extract = content[start+10:len(content)]
                stop = extract.find('png')
                img = extract[:stop+3]
                if (len(img)>20):
                    self.response.out.write('<img src = "')
                    self.response.out.write(img)
                    self.response.out.write('"/>')
                    self.response.out.write('\n')
                content = extract

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/fetch', fetch)],
                                     debug=True)
def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
