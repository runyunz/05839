#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# standard imports you should have already been using
import webapp2
from webapp2_extras import jinja2
import logging
import urllib

# this library is for decoding json responses
from webapp2_extras import json
# this is used for constructing URLs to google's APIS
from apiclient.discovery import build
# this library is for making http requests and so on
import httplib2
# this library helps with statistical calculations
import numpy


# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyBC3xSAbpqAIdYC_OrZP_FtwfkF_XbkR0Q'
# This is the table id for the fusion table
TABLE_ID = '1l8GVeoIMH5ggV-UF3khJ5SDMT7RN4H9wwzRLsr4'
# This uses discovery to create an object that can talk to the 
# fusion tables API using the developer key
service = build('fusiontables', 'v1', developerKey=API_KEY)


# we are adding a new class that will 
# help us to use jinja. MainHandler will sublclass this new
# class (BaseHandler), and BaseHandler is in charge of subclassing
# webapp2.RequestHandler  
class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)
    
    # lets jinja render our response
    def render_response(self, _template, context):
        values = {'url_for': self.uri_for}

        logging.info(context)
        values.update(context)
        self.response.headers['Content-Type'] = 'text/html'

        # Renders a template and writes the result to the response.
        try: 
            rv = self.jinja2.render_template(_template, **values)
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write(rv)
        except TemplateNotFound:
            self.abort(404)

# This is changed from Byte1 to subclass basehandler 
class MainHandler(BaseHandler):
    
    # Once again, get is responsible for returning the appropriate
    # information for display to the user (specifically for the default
    # landing page
    def get(self):
        """default landing page"""

        data = self.get_all_data()
        context = {}

        # and render the response
        self.render_response('index.html', context)
        
    # collect the data from google fusion tables
    # pass in the name of the file the data should be stored in
    def get_all_data(self):
        """ collect data from the server. """
        # limited to 10 rows
        query = "SELECT * FROM " + TABLE_ID + " WHERE  AnimalType = 'DOG' LIMIT 2"
        # response = service.query().sql(sql=query).execute()
		logging.info(response['columns'])
	    logging.info(response['rows'])        
        logging.info(response)
        return response

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
