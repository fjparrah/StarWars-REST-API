"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Favoritepeople,Favoriteplanet, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#-----------------------USER METHODS-------------------------------------------------------------
  
#Create user 
@app.route('/user', methods=["POST"])
def create():
  get_from_body = request.json.get("email")
  user = User() 
  usuario_existente = User.query.filter_by(email=get_from_body).first()
  if usuario_existente is not None:
    return jsonify({'message': 'El usuario ya existe'})
  else:
    user.name = request.json.get("name")
    user.last_name = request.json.get("last_name")
    user.email = request.json.get("email")
    user.password = request.json.get("password")
    user.subscription_date =request.json.get("subscription_date")

    db.session.add(user)
    db.session.commit()  
    return jsonify({'message': 'User added'}), 201
   
#List Users 
@app.route('/users', methods=["GET"])
def home():
    users= User.query.all()
    users= list(map(lambda user: user.serialize_user(), users))
    return jsonify({
    "data": users,
    "status": 'success'
  }),200
    
#Update users 
@app.route('/user', methods=["PUT"])
def update():
  email_to_search = request.json.get("email")
  user = User.query.filter_by(email=email_to_search).first()
  if user is None:
     return jsonify({'message': 'The user does not exist'}), 401
  else:
    user.name = request.json.get("name")
    user.last_name = request.json.get("lastname")
    user.email = request.json.get("email")
    user.password = request.json.get("password")
  
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User updated'}), 201
 
#Delete users
@app.route("/user/<int:id>", methods=['DELETE'])
def delete_user(id):
  user = User.query.filter_by(id=id).first()
  print(user)
  if user is not None:
    db.session.delete(user)
    db.session.commit()
    return jsonify({
      "msg": "Usuario eliminado",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Usuario no encontrado"}),404
  
#-----------------------------USER METHOD´S END---------------------------------------------

#-----------------------------PEOPLE METHOD´S---------------------------------------------

 #Add Character
@app.route('/createpeople', methods=["POST"])
def createpeople():
 add_people = request.json.get("name")
 people = People() 
 people_exist= People.query.filter_by(name=add_people).first()
 if people_exist is not None:
    return "The character already exist"
 else:
    people.name = request.json.get("name")
    people.height = request.json.get("height")
    people.gender =request.json.get("gender")

    db.session.add(people)
    db.session.commit()  

    return f"Se creo el personaje", 201
  
  #Listo los personajes
@app.route('/people', methods=["GET"])
def people():
    people= People.query.all()
    peoples= list(map(lambda people: people.serialize_people(), peoples))
   
    return jsonify({
    "data": peoples,
    "status": 'success'
  }),200   

#Actualizo un Personaje
@app.route('/updatepeople', methods=["PUT"])
def updatepeople():
  name_to_search = request.json.get("name")
  peopletoupdate = People.query.filter_by(name=name_to_search).first()
  if peopletoupdate is None:
    return "The character does not exist", 401
  else:
    peopletoupdate.name = request.json.get("name")
    peopletoupdate.status = request.json.get("status")
    peopletoupdate.species = request.json.get("species")
    peopletoupdate.gender = request.json.get("gender")
  
    db.session.add(peopletoupdate)
    db.session.commit()
    return f"Se actualizo el personaje", 201

#Elimino personaje  
@app.route("/deletepeople/<int:id>", methods=['DELETE'])
def delete_people(id):
  people_delete = People.query.filter_by(id=id).first()
  if  people_delete is not None:
    db.session.delete( people_delete)
    db.session.commit()
    return jsonify({
      "msg": "Personaje eliminado",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Personaje no encontrado"}),404
  
#Muestro los personajes por su id
@app.route('/people/<int:id>', methods=["GET"])
def obtainig_people(id):
    peoplebyid= People.query.filter_by(id=id).first()
    if peoplebyid is not None:
         return jsonify(peoplebyid.serialize_people()), 200
    else:
         return jsonify({"error":"Character not found"}),404
    
 #----------------------------PEOPLE METHOD´S END---------------------------------------------   

#-----------------------------PLANET METHOD´S---------------------------------------------

 #Add planet
@app.route('/createplanet', methods=["POST"])
def createplanet():
 add_planet = request.json.get("name")
 planet = Planet() 
 planet_exist= Planet.query.filter_by(name=add_planet).first()
 if planet_exist is not None:
    return "The planet already exist"
 else:
    planet.name = request.json.get("name")
    planet.diameter = request.json.get("diameter")
    planet.population =request.json.get("population")

    db.session.add(planet)
    db.session.commit()  

    return f"Se creo el planeta", 201
  
  #List planets
@app.route('/´planet', methods=["GET"])
def planet():
    planet= Planet.query.all()
    planets = list(map(lambda planet: planet.serialize_planet(), planets))
   
    return jsonify({
    "data": planets,
    "status": 'success'
  }),200   

#Update a planet
@app.route('/updateplanet', methods=["PUT"])
def updateplanet():
  name_to_search = request.json.get("name")
  planettoupdate = Planet.query.filter_by(name=name_to_search).first()
  if  planettoupdate is None:
    return "The planet does not exist", 401
  else:
     planettoupdate.name = request.json.get("name")
     planettoupdate.diameter = request.json.get("diameter")
     planettoupdate.population =request.json.get("population")

  
     db.session.add(planettoupdate)
     db.session.commit()
    
     return f"Se actualizo el personaje", 201

#Delete planet  
@app.route("/deleteplanet/<int:id>", methods=['DELETE'])
def delete_planet(id):
  planet_delete = Planet.query.filter_by(id=id).first()
  if  planet_delete is not None:
    db.session.delete(planet_delete)
    db.session.commit()
    return jsonify({
      "msg": "Planeta eliminado",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Personaje no encontrado"}),404
  
#Show planets by id
@app.route('/planet/<int:id>', methods=["GET"])
def obtainig_planet(id):
    planetbyid= Planet.query.filter_by(id=id).first()
    if planetbyid is not None:
         return jsonify(planetbyid.serialize_people()), 200
    else:
         return jsonify({"error":"Character not found"}),404
    
 #----------------------------PLANET METHOD´S END---------------------------------------------   


# -----------------------------FAVORITES PEOPLE METHOD´S---------------------------------------------

# Crear people favorito para un usuario
@app.route('/createfavoritepeople', methods=["POST"])
def create_favorite_people():
    id_user = request.json.get("id_user")
    id_people = request.json.get("id_people")

    favorite_people = Favoritepeople(id_user=id_user, id_people=id_people)
    db.session.add(favorite_people)
    db.session.commit()

    return jsonify({"message": "Se agregó el personaje favorito"}), 201

# Listar los people favoritos de un usuario
@app.route('/favoritepeople', methods=["GET"])
def favorite_people():
    favorite_people = Favoritepeople.query.all()
    favorite_people_list = [favorite_people.serialize_favoritepeople() for favorite_people in favorite_people]

    return jsonify({
        "data": favorite_people_list,
        "status": 'success'
    }), 200

# Actualizar people favorito
@app.route('/updatefavoritepeople/<int:id>', methods=["PUT"])
def update_favorite_people(id):
    favorite_people_to_update = Favoritepeople.query.get(id)
    if favorite_people_to_update is None:
        return jsonify({"error": "Personaje favorito no encontrado"}), 404

    favorite_people_to_update.id_user = request.json.get("id_user")
    favorite_people_to_update.id_people = request.json.get("id_people")

    db.session.commit()
    return jsonify({"message": "Se actualizó el personaje favorito"}), 200

# Eliminar people de un usuario
@app.route("/deletefavoritepeople/<int:id>", methods=['DELETE'])
def delete_favorite_people(id):
    favorite_people_delete = Favoritepeople.query.get(id)
    if favorite_people_delete is None:
        return jsonify({"error": "Personaje favorito no encontrado"}), 404

    db.session.delete(favorite_people_delete)
    db.session.commit()

    return jsonify({"msg": "Personaje favorito eliminado", "status": "Success"}), 203

# -----------------------------FAVORITES PEOPLE METHOD´S END---------------------------------------------


# -----------------------------FAVORITE PLANETS METHOD´S---------------------------------------------

# Crear planeta favorito para un usuario
@app.route('/createfavoriteplanet', methods=["POST"])
def create_favorite_planet():
    id_user = request.json.get("id_user")
    id_planet = request.json.get("id_planet")

    favorite_planet = Favoriteplanet(id_user=id_user, id_planet=id_planet)
    db.session.add(favorite_planet)
    db.session.commit()

    return jsonify({"message": "Se agregó el planeta favorito"}), 201

# Listar los planetas favoritos de un usuario
@app.route('/favoriteplanet', methods=["GET"])
def favorite_planets():
    favorite_planets = Favoriteplanet.query.all()
    favorite_planets_list = [favorite_planet.serialize_favoriteplanet() for favorite_planet in favorite_planets]

    return jsonify({
        "data": favorite_planets_list,
        "status": 'success'
    }), 200

# Actualizar planeta favorito
@app.route('/updatefavoriteplanet/<int:id>', methods=["PUT"])
def update_favorite_planet(id):
    favorite_planet_to_update = Favoriteplanet.query.get(id)
    if favorite_planet_to_update is None:
        return jsonify({"error": "Planeta favorito no encontrado"}), 404

    favorite_planet_to_update.id_user = request.json.get("id_user")
    favorite_planet_to_update.id_planet = request.json.get("id_planet")

    db.session.commit()
    return jsonify({"message": "Se actualizó el planeta favorito"}), 200

# Eliminar planeta de un usuario
@app.route("/deletefavoriteplanet/<int:id>", methods=['DELETE'])
def delete_favorite_planet(id):
    favorite_planet_delete = Favoriteplanet.query.get(id)
    if favorite_planet_delete is None:
        return jsonify({"error": "Planeta favorito no encontrado"}), 404

    db.session.delete(favorite_planet_delete)
    db.session.commit()

    return jsonify({"msg": "Planeta favorito eliminado", "status": "Success"}), 203

# -----------------------------FAVORITE PLANETS METHOD´S END---------------------------------------------


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

