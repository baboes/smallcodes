import webapp2

from execcode import *


app = webapp2.WSGIApplication(
    [('/', TypeAndRun),
    ('/(\d+)', RunFile), ],
    debug=True)
