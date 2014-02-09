#!/usr/bin/env python
#
# Byte 3 Version 2
# 
# Copyright 1/2014 Jennifer Mankoff
#
# Licensed under GPL v3 (http://www.gnu.org/licenses/gpl.html)
#

# standard imports (same as byte2)
import webapp2
from webapp2_extras import jinja2
from webapp2_extras import json
import logging
import httplib2
from apiclient.discovery import build
import urllib
import numpy
from django.utils import simplejson

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
        # logging.info(context)
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

    def post(self):
        if u'cat' in self.request.arguments():#self.request.get(u'cat'):    
            self.render_response('cat_pie.html', {})
        else:
            self.render_response('dog_pie.html', {})
        # logging.info(self.request.arguments())
        # logging.info(self.request)
        # logging.info(self.request.get('cat'))
    # Once again, get is responsible for returning the appropriate
    # information for display to the user (specifically for the default
    # landing page
    def get(self):
        """default landing page"""
        # logging.info("in get")
        
        data = self.get_all_data()
        columns = data['columns']
        rows = data['rows']

        # specify the ages we will search for
        # age_mapping = {u'Infant - Younger than 6 months':'<6mo',
        #                u'Youth - Younger than 1 year':'6mo-1yr',
        #                u'Older than 1 year':'1yr-6yr',
        #                u'Older than 7 years':'>7yr',
        #                u'':'Unspecified'}
        # create an 'empty' array storing the number of dogs in each outcome
        
        # specify the outcomes we will search for
        outcomes = ['Adopted', 'Euthanized', 'Foster', 'Returned to Owner', 'Transferred to Rescue Group', 'Other']
        animals = ['CAT', 'DOG']
        # ages = ['<6mo', '6mo-1yr', '1yr-6yr', '>7yr', 'Unspecified']

        outcome_by_animal = []
        for outcome in outcomes:
            res = {'OutcomeType': outcome}
            for animal in animals:
                res[animal] = 0
            outcome_by_animal = outcome_by_animal + [res]
        logging.info(outcome_by_animal)

        # find the column id for ages
        animalid = columns.index(u'AnimalType')
        
        # find the column id for outcomes
        outcomeid = columns.index(u'OutcomeType')

        # loop through each row
        for row in rows: 
            # get the age of the dog in that row
            animal = row[animalid]
            # get the outcome for the dog in that row
            outcome = row[outcomeid]
            # if the age is a known value (good data) find
            # out which of the items in our list it corresponds to
            if outcome in outcomes: outcome_position = outcomes.index(outcome)
            # otherwise we will store the data in the 'Other' age column
            else: outcome_position = outcomes.index('Other')

            # if the outcome is a bad value, we call it 'Other' as well
            if animal not in animals: animal = 'Other'

            # now get the current number of dogs with that outcome and age
            outcomes_for_animal = outcome_by_animal[outcome_position]
            # and increase it by one
            outcomes_for_animal[animal] = outcomes_for_animal[animal] + 1

        logging.info(outcome_by_animal)
        logging.info(outcomes)
        logging.info(animals)
    
        # add it to the context being passed to jinja
        variables = {'data':json.encode(outcome_by_animal),
                     'y_labels':animals,
                     'x_labels':outcomes}
       
        # and render the response
        self.render_response('index.html', variables)
        
    # collect the data from google fusion tables
    # pass in the name of the file the data should be stored in
    def get_all_data(self):
        """ collect data from the server. """

        # open the data stored in a file called "data.json"
        try:
            fp = open("data/data.json")
            response = simplejson.load(fp)
        # but if that file does not exist, download the data from fusiontables
        except IOError:
            logging.info("failed to load file")
            service = build('fusiontables', 'v1', developerKey=API_KEY)
            query = "SELECT * FROM " + TABLE_ID + " WHERE AnimalType IN ('DOG','CAT')"
            response = service.query().sql(sql=query).execute()
            
        return response
      
        
# This specifies that MainHandler should handle a request to 
# jmankoff-byte2.appspot.com/
# This is where you would add additional handlers if you 
# wanted to have more subpages on that website.
app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
