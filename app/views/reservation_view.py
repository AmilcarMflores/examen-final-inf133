def render_reservation_list(resevations):
    return[
        {
            "id": "reservation.id",
            "user_id": "reservation.user_id",
            "restaurant_id": "reservation.restaurant_id",
            "num_guests": "reservation.num_guests",
            "special_requests": "reservation.special_requests",
            "status": "reservation.status"
        }
        for reservation in resevations
    ]

def render_reservation_detail(reservation):
    return{
            "id": "reservation.id",
            "user_id": "reservation.user_id",
            "restaurant_id": "reservation.restaurant_id",
            "num_guests": "reservation.num_guests",
            "special_requests": "reservation.special_requests",
            "status": "reservation.status"
        }