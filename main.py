import datetime
import webapp2
import wsgiref
from google.appengine.ext import db
from google.appengine.api import users

class Ingredient(db.Model):
    
    name = db.StringProperty(required = True)
    quantity = db.IntegerProperty()  #should be number or string?
    date = db.DateTimeProperty(auto_now_add=True)

def user_key(name = None):
	return db.Key.from_path('Ingredient',name)
	
class UserPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            self.redirect("/list")
        else:
            self.redirect(users.create_login_url(self.request.uri))


# Ingred0 = Ingredient(name = 'water', quantity = 2)
# Ingred1 = Ingredient(name = 'flour', quantity = 3)

# Ingred0.put()
# Ingred1.put()

class MainPage(webapp2.RequestHandler):

    def get(self):
		
		ingredList = db.GqlQuery("SELECT * "
								"FROM Ingredient"
								" ORDER BY when DESC")
								
	
		self.response.write("<b>Ingredient List:</b> <br></br>")
		for item in ingredList:
			if item.name:
				self.response.write('Ingredient: %s Quantity: %s Date: %s <br></br>' %(item.name ,item.quantity ,item.date))
			else:
				self.response.write('ERROR no name entered')

# i = Ingredient.all()
# for x in i:
	# x.delete()

app = webapp2.WSGIApplication([('/', UserPage),
                               ('/list', MainPage)],
                              debug=True)
wsgiref.handlers.CGIHandler().run(app)
