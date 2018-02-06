import os
import runpy

import webapp2
from google.appengine.ext.webapp import template

from redirect import redirect_stdout, outbuf


def error_page(rh, error, code):
    rh.response.headers['Content-Type'] = 'text/plain'
    rh.response.write('Error:\n')
    rh.response.write(str(error))
    rh.response.write('\n')
    rh.response.write('Code:\n')
    rh.response.write(code)


# Type code and run online.
class TypeAndRun(webapp2.RequestHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/codeform.html')
        self.response.write(template.render(path, dict()))


    def post(self):
        try:
            @redirect_stdout
            def run_code(code, exec_input):
                exec(code)

            code = self.request.get('code')
            exec_input = self.request.get('input')
            run_code(code, exec_input)
            path = os.path.join(os.path.dirname(__file__), 'templates/ps.html')
            values = {
                'problem_definition': 'tbd',
                'code': code,
                'input': exec_input,
                'output': outbuf.read(),
            }
            self.response.write(template.render(path, values))
        except Exception as e:
            error_page(self, e, self.request.get('code'))


# Read a file and run online.
class RunFile(webapp2.RequestHandler):

    def get(self, number):
        try:
            @redirect_stdout
            def run_file(f):
                path = os.path.join(os.path.dirname(__file__), f)
                runpy.run_path(path, run_name = '__main__')

            problem_definition = 'No problem definition'
            with open('p' + str(number)) as f:
                problem_definition = str.join(f.readlines())
            code = 'No code'
            with open('p' + str(number) + '.py') as f:
                code = str.join(f.readlines())

            run_file('p' + str(number) + '.py')
            path = os.path.join(os.path.dirname(__file__), 'templates/ps.html')
            values = {
                'problem definition': problem_definition,
                'code': code,
                'input': 'tbd',
                'output': outbuf.read(),
            }
            self.response.write(template.render(path, values))
        except Exception as e:
            error_page(self, e, '')
