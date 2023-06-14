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


    #region Users collection

    def find_users(self):
        """Obtiene todos los usuarios"""
        results = self.control.find({})
        return results
    
    def create_user(self, user):
        """Crea un nuevo usuario"""
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
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
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
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
    #endregion

    #region Places collection
    #endregion