from bson.objectid import ObjectId

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
        self.control.insert_one({
            "username": user["username"],
            "email": user["email"],
            "password": user["password"],
            "name": user["name"],
            "lastname": user["lastname"]
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

    #endregion

    #region Places collection
    #endregion