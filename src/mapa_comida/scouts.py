from bson.objectid import ObjectId
import datetime

class Scouts(object):
    def __init__(
            self,
            database,
            collection,
            collection_places
    ):
        self.database = database

        self.control = self.database.get_collection(collection)
        self.collection_places = self.database.get_collection(collection_places)
        self.date_string = "%Y-%m-%d %H:%M:%S UTC"


    #region Users collection
    def find_users(self):
        """Obtiene todos los usuarios"""
        results = self.control.find({})
        return results
    
    def create_user(self, user):
        """Crea un nuevo usuario"""
        date = datetime.datetime.utcnow().strftime(self.date_string)
        self.control.insert_one({
            "username": user["username"],
            "email": user["email"],
            "password": user["password"],
            "name": user["name"],
            "lastname": user["lastname"],
            "created": date,
            "last_updated": date,
            "pass_updated": date
        })
    
    def find_user_id(self, user_id):
        """Encontrar usuario por Object id"""
        objInstance = ObjectId(user_id)
        results = self.control.find_one({"_id": objInstance})
        return results
    
    def find_user_by_email(self, email):
        """Encontrar usuario por email"""
        results = self.control.find_one({"email": email})
        return results
    
    def delete_user(self, user_id):
        """Eliminar usuario por ObjectId"""
        objInstance = ObjectId(user_id)
        self.control.delete_one({"_id": objInstance})

    def update_user(self, user):
        """Actualizar nombres y apellidos del usuario"""
        date = datetime.datetime.utcnow().strftime(self.date_string)
        objInstance = ObjectId(user["id"])
        user_updated = {
            "name": user["name"],
            "lastname": user["lastname"],
            "last_updated": date
        }
        query = {"_id": objInstance}
        new_values = {"$set": user_updated}

        self.control.update_one(query, new_values)

    #endregion

    #region Sign in
    def update_password(self, user_pass):
        """Valida actualización de contraseña"""
        objInstance = ObjectId(user_pass["id"])
        pass_updated = {"password": user_pass["password"]}
        query = {"_id": objInstance}
        new_values = {"$set": pass_updated}
        self.control.update_one(query, new_values)
    
    def find_by_id_password(self, user, user_pass):
        """Encuentra por usuario y contraseña"""
        results = self.control.find_one({"username": user, "password": user_pass})
        return results

    def update_user_email(self, user_id, user_email):
        """Actualiza correo del usuario"""
        objInstance = ObjectId(user_id)
        email_updated = {"email": user_email} 
        query = {"_id": objInstance}
        new_values = {"$set": email_updated}
        self.control.update_one(query, new_values)
    
    #endregion

    #region Spaces collection
    """
    Mongo collection
    {
        "_id": ObjectId(372832890),
        "name": "Nombre del espacio"
        "owner": Id_del_propietario,
        "users": [IdUsuario1, IdUsuario2]
    }
    """
    #endregion

    #region Places collection
    """
    Mongo collection:
    {
        "_id": ObjectId(372832890),
        "name": "Nombre del lugar",
        "created_by": "Id_del_creador",
        "cordenates": {
            "latitud": "latitude",
            "longitud": "longitud"
        },
        "address": "direccion"
        "created": "dateCreated",
        "updated": "dateUpdated"
    }
    """

    def find_all_places(self):
        """Obtiene todos los lugares"""
        results = self.collection_places.find({})
        return results
    
    def find_place_by_id(self, place_id):
        """Obtiene un lugar por id"""
        objInstance = ObjectId(place_id)
        results = self.collection_places.find_one({"_id": objInstance})
        return results
    
    def create_place(self, place_obj):
        """Crea un nuevo lugar"""
        date = datetime.datetime.utcnow().strftime(self.date_string)
        place = {
            "name": place_obj["name"],
            "created_by": place_obj["created_by"],
            "cordenates": {
                "latitud": place_obj["cordenates"]["latitud"],
                "longitud": place_obj["cordenates"]["longitud"]
            },
            "address": place_obj["address"],
            "created": date,
            "updated": date
        }
        self.collection_places.insert_one(place)

    def delete_place(self, place_id):
        """Elimina un lugar"""
        objInstance = ObjectId(place_id)
        self.collection_places.delete_one({"_id": objInstance})

    def find_place_by_cordenates(self, cordenates):
        """Encuentra un lugar por coordenadas"""
        latitud = cordenates["latitud"]
        longitud = cordenates["longitud"]
        query = {"cordenates.latitud":latitud, "cordenates.longitud":longitud}
        places = self.collection_places.find(query)
        return places
    
    def update_place(self, place):
        """Se actualiza lugar"""
        date = datetime.datetime.utcnow().strftime(self.date_string)
        objInstance = ObjectId(place["id"])
        place_updated = {
            "name": place["name"],
            "address": place["address"],
            "cordenates": place["cordenates"],
            "updated": date
        }
        query = {"_id": objInstance}
        new_values = {"$set": place_updated}

        self.collection_places.update_one(query, new_values)
    #endregion