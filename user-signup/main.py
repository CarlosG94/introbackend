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
import os

import jinja2
import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
USER_PASS = re.compile(r"^.{3,20}$")
USER_EM = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def valid_username(username):
		return USER_RE.match(username)

def valid_password(password):
		return USER_PASS.match(password)

def valid_verify(v, p):
	if v == p:
		return USER_PASS.match(p)

def valid_email(email):
		return USER_EM.match(email)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
		def get(self):
			self.render("signup.html")

		def post(self):
			user_name = self.request.get("username")
			user_passwd = self.request.get("password")
			user_verify = self.request.get("verify")
			user_email = self.request.get("email")

			name = valid_username(user_name)
			passwd = valid_password(user_passwd)
			verify = valid_verify(user_verify, user_passwd)
			email = valid_email(user_email)

			if (name and passwd and verify and email):
				self.redirect("/welcome?username=" + user_name)
			elif not email:
				self.render("signup.html", error4="Wrong email")
			elif (name and passwd and verify):
				self.redirect("/welcome?username=" + user_name)
			elif (user_passwd != user_verify):
				self.render("signup.html", error3="Passwords don't match")
			elif not name:
				self.render("signup.html", error1="Incorrect Username")
			elif not passwd:
				self.render("signup.html", error2="Incorrect password")

class WelcomeHandler(Handler):
    def get(self):
        user = self.request.get('username')
        if valid_username(user):
        	self.render("success.html", username = user)

app = webapp2.WSGIApplication([
		('/', MainHandler),
		('/welcome', WelcomeHandler)
], debug=True)
