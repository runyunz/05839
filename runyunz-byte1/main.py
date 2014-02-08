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
import webapp2
from webapp2_extras import jinja2
import feedparser
import logging
import urllib


# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


class MainHandler(BaseHandler):
    def get(self):
        # feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=1nWYbWm82xGjQylL00qv4w&_render=rss&textinput1=dogs" )
        feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=5506c160ff35901c6c603eebbe8e7eb4&_render=rss&Movie=American+Hustle")
      #   for item in feed["items"]:  
		    # logging.info(item.published_parsed)
		    # logging.info(item.link)
		    # logging.info(item.title)
		    # logging.info(item.description)

        feed = [{"link": item.link, "title":item.title, "description" : item.description} for item in feed["items"]]
        # this will eventually contain information about the RSS feed
        context = {"feed" : feed, "search" : urllib.quote('American&Hustle'), "count": len(feed)}
		# here we call render_response instead of self.response.write.
        self.render_response('index.html', **context)

    def post(self):
        # logging.info("post")
        terms = self.request.get('search_term')
        terms = urllib.quote(terms)

        # feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=1nWYbWm82xGjQylL00qv4w&_render=rss&textinput1=" + terms )
        feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=5506c160ff35901c6c603eebbe8e7eb4&_render=rss&Movie=" + terms)
        feed = [{"link": item.link, "title":item.title, "description" : item.description} for item in feed["items"]]

        context = {"feed": feed, "search": terms, "count": len(feed)}
        self.render_response('index.html', **context)

app = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)
