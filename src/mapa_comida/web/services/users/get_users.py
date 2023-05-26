from flask import request

def register_routes(app, scouts):

    @app.route('/users', methods=['GET'])
    def get_users():
        multimap = request.args if request.method == 'GET' else request.form
        busqueda_params = multimap.to_dict(flat=True)

        response = []
        error = None

        try:
            results = scouts.find_users()
        except Exception as e:
            raise e