class Scouts(object):
    def __init__(
            self,
            database,
            collection
    ):
        self.database = database

        self.control =self.database.get_collection(collection)

        #Definir el resto de búsquedas en BD

        def find_users(self):
            results = self.control.findAll()
            return results