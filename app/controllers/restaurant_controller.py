from flask import Blueprint, request, jsonify
from app.models.restaurant_model import Restaurant
from app.views.restaurant_view import render_restaurant_detail, render_restaurant_list
from app.utils.decorators import jwt_required, roles_required

#Crear un blueprint para el controlador
restaurant_bp = Blueprint("restaurant", __name__)



#Ruta para obtener la lista de productos
@restaurant_bp.route("/reservations", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_products():
    reservations = Restaurant.get_all()
    return jsonify(render_product_list(reservations))


#Ruta para obtener un restaurante especifico por id 
@restaurant_bp.route("/reservations/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_restaurant(id):
    restaurant = Restaurant.get_by_id(id)
    if restaurant:
        return jsonify(render_restaurant_detail(restaurant))
    return jsonify({"error":"Restaurante no encontrado"}), 404

#Ruta para crear un nuevo restaurante y guardarlo en la base de datos
@restaurant_bp.route("/reservations", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_restaurant():
    data = request.json
    #name = data.get("name")
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("description")
    rating = data.get("rating")

    #Validadcion simple de datos de entrada
    if not name or not address or not city or not phone or not description or not rating:
        return jsonify({"error":"Faltan datos requeridos"}), 400
    #Crear un nuevo restaurante
    restaurant = Restaurant(name=name, address=address,city=city, phone=phone, description=description, rating=rating)
    restaurant.save()
    return jsonify(render_restaurant_detail(restaurant)), 201


#Ruta para actualizar un restaurante existente
@restaurant_bp.route("/reservations/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_reservation(id):
    restaurant = Restaurant.get_by_id(id)
    if not restaurant:
        return jsonify({"error":"Restaurante no encontrado"}), 404
    
    data = request.json
    #name = data.get("name")
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("description")
    rating = data.get("rating")

    #Actualziar los datos del restaurante
    restaurant.update(name=name, address=address,city=city, phone=phone, description=description, rating=rating)
    return jsonify(render_restaurant_detail(restaurant))

#Ruta para eliminar un restaurante existente
@restaurant_bp.route("/reservations/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_restaurant(id):
    restaurant = Restaurant.get_by_id(id)
    if not restaurant:
        return jsonify({"error":"restaurante no encontrado"}),404
    
    #eliminar el restaurante de la base de datos
    restaurant.delete()
    
    #Respuesta vacia con codigo de estado 204
    return "", 204
