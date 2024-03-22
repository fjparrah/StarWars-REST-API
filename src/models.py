from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique= True)
    password = db.Column(db.String(250),unique=False, nullable=False)
    subscription_date = db.Column(db.Integer, nullable=False)


    def serialize_user(self):
        return {
        "id": self.id,
        "name": self.name,
        "last_name": self.last_name,
        "email": self.email,
        "subscription_date": self.subscription_date
    }
    

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.db.String(250), unique=True)
    height = db.Column(db.Integer(250), nullable=False)   
    gender = db.Column(db.String(250), nullable=False)    
    
    def serialize_people(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,        
            "gender": self.gender  
            }

class Planet(db.Model):
    __tablename__ = 'planet'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)
    
    def serialize_planet(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,        
            "population": self.population  
            }    

class Favoritepeople(db.Model):   
   __tablename__ = 'favoritepeople'
   id = db.Column(db.Integer, primary_key=True)
   id_user =db.Column(db.Integer, db.ForeignKey('user.id')) # Marca el id del usuario que selecciona un personaje como favorito
   user = db.relationship(User)
   id_people = db.Column(db.Integer,db.ForeignKey('people.id')) # Marca el id del personaje que ha sido seleccionado como favorito
   people = db.relationship(People)

   def serialize_favoritepeople(self):
         return {

            "id": self.id,
            "id_user": self.user.id,
            "id_people": self.people.id,
            "people_name": self.people.name
        }
  
class Favoriteplanet(db.Model):   
   __tablename__ = 'favoriteplanet'
   id = db.Column(db.Integer, primary_key=True)
   id_user =db.Column(db.Integer, db.ForeignKey('user.id')) # Marca el id del usuario que selecciona un personaje como favorito
   user = db.relationship(User)
   id_planet = db.Column(db.Integer,db.ForeignKey('planet.id')) # Marca el id del personaje que ha sido seleccionado como favorito
   planet = db.relationship(Planet)

   def serialize_favoriteplanet(self):
         return {

            "id": self.id,
            "id_user": self.user.id,
            "id_ planet": self.planet.id,
            "planet_name": self.planet.name
        }
      