from flask import Blueprint, request, jsonify
from app.models.reservation_model import Reservation
from app.views.reservation_view import render_reservation_detail, render_reservation_list
from app.utils.decorators import jwt_required, roles_required

#Crear un blueprint para el controlador
reservation_bp = Blueprint("reservation", __name__)



#Ruta para obtener la lista de productos
@reservation_bp.route("/reservations", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_products():
    reservations = Reservation.get_all()
    return jsonify(render_reservation_list(reservations))


#Ruta para obtener un reservacion especifico por id 
@reservation_bp.route("/reservations/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_reservation(id):
    reservation = Reservation.get_by_id(id)
    if reservation:
        return jsonify(render_reservation_detail(reservation))
    return jsonify({"error":"Reservacion no encontrado"}), 404

#Ruta para crear un nuevo reservacion y guardarlo en la base de datos
@reservation_bp.route("/reservations", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_reservation():
    data = request.json
    #name = data.get("name")
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_requests = data.get("special_requests")
    status = data.get("status")

    #Validadcion simple de datos de entrada
    if not user_id or not restaurant_id or not reservation_date or not num_guests or not special_requests or not status:
        return jsonify({"error":"Faltan datos requeridos"}), 400
    #Crear un nuevo reservacion
    reservation = Reservation(user_id=user_id, restaurant_id=restaurant_id,reservation_date=reservation_date, num_guests=num_guests, special_requests=special_requests, status=status)
    reservation.save()
    return jsonify(render_reservation_detail(reservation)), 201


#Ruta para actualizar un reservacion existente
@reservation_bp.route("/reservations/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_reservation(id):
    reservation = Reservation.get_by_id(id)
    if not reservation:
        return jsonify({"error":"Reservacion no encontrado"}), 404
    
    data = request.json
    #name = data.get("name")
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_requests = data.get("special_requests")
    status = data.get("status")

    #Actualziar los datos del reservacion
    reservation.update(user_id=user_id, restaurant_id=restaurant_id,reservation_date=reservation_date, num_guests=num_guests, special_requests=special_requests, status=status)
    return jsonify(render_reservation_detail(reservation))

#Ruta para eliminar un reservacion existente
@reservation_bp.route("/reservations/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_reservation(id):
    reservation = Reservation.get_by_id(id)
    if not reservation:
        return jsonify({"error":"reservacion no encontrado"}),404
    
    #eliminar el reservacion de la base de datos
    reservation.delete()
    
    #Respuesta vacia con codigo de estado 204
    return "", 204
