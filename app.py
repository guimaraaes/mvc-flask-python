
from functools import wraps

from flask import (Flask, Response, abort, json, redirect, render_template,
                   request)
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from admin.Admin import start_views
from config import app_active, app_config
from controller.Product import ProductController
from controller.User import UserController

config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    db = SQLAlchemy(config.APP)

    start_views(app, db)
    Bootstrap(app)
    db.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # @app.route('/')
    # def index():
    #     return 'Hello World!'

    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args, **kwargs):
            user = UserController()
            try:
                result = user.verify_auth_token(
                    request.headers['access_token'])
                if result['status'] == 200:
                    return f(*args, **kwargs)
                else:
                    abort(result['status'], result['message'])
            except KeyError as e:
                abort(401, 'É necessário enviar um token de acesso')
        return verify_token

    @app.route('/login', methods=['GET'])
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_post():
        user = UserController()
        email = request.form["email"]
        password = request.form["password"]
        result = user.login(email, password)

        if result:
            return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': None})

    @app.route('/login_api/', methods=['POST'])
    def login_api():
        header = {}
        user = UserController()
        email = request.form["email"]
        password = request.form["password"]
        result = user.login(email, password)
        code = 401
        response = {
            'message': 'Usuário não autorizado',
            'result': []
        }
        if result:
            if result.active:
                result = {
                    'id': result.id,
                    'username': result.username,
                    'email': result.email,
                    'date_created': result.date_created,
                    'active': result.active
                }
                header = {
                    'access_token': user.generate_auth_token(result),
                    'token_type': 'JWT'
                }
                code = 200
                response["message"] = "Login realizado com sucesso"
                response["result"] = result
        return Response(json.dumps(response, ensure_ascii=False),
                        mimetype='application/json'), code, header

    @app.route('/recovery-password', methods=['GET'])
    def recovery_password():
        return 'tela recuperar senha'

    @app.route('/recovery-password', methods=['POST'])
    def recovery_password_post():
        user = UserController()

        result = user.recovery(request.form['email'])
        if result:
            return render_template('recovery.html', data={'status': 200, 'msg': 'E-mail de recuperação enviado com sucesso'})
        else:
            return render_template('recovery.html', data={'status': 401, 'msg': 'Erro ao enviar e-mail de recuperação'})

    @app.route('/products', methods=['GET'])
    @app.route('/products/<limit>', methods=['GET'])
    @auth_token_required
    def get_all_products(limit=None):
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }

        product = ProductController()

        result = product.get_all_products(limit=limit)
        return Response(json.dumps(result, ensure_ascii=False),
                        mimetype='application/json'), result['status'], header

    @app.route('/product/<product_id>', methods=['GET'])
    @auth_token_required
    def get_product_by_id(product_id):
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }

        product = ProductController()

        result = product.get_product_by_id(product_id=product_id)
        return Response(json.dumps(result, ensure_ascii=False),
                        mimetype='application/json'), result['status'], header

    @app.route('/product', methods=['POST'])
    @auth_token_required
    def save_products():
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }
        product = ProductController()

        result = product.save_product(request.form)
        return Response(json.dumps(result, ensure_ascii=False),
                        mimetype='application/json'), result['status'], header

    @app.route('/product', methods=['PUT'])
    @auth_token_required
    def update_product():
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }

        product = ProductController()

        result = product.update_product(request.form)
        return Response(json.dumps(result, ensure_ascii=False),
                        mimetype='application/json'), result['status'], header

    @app.route('/product', methods=['DELETE'])
    @auth_token_required
    def delete_product():
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }

        product = ProductController()

        result = product.delete_product(request.form)
        return Response(json.dumps(result, ensure_ascii=False),
                        mimetype='application/json'), result['status'], header

    @app.route('/user/<user_id>', methods=['GET'])
    @auth_token_required
    def get_user_by_id(user_id):
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }

        product = UserController()

        result = product.get_user_by_id(user_id=user_id)
        return Response(json.dumps(result, ensure_ascii=False),
                        mimetype='application/json'), result['status'], header

    @app.route('/user/email/<user_email>', methods=['GET'])
    @auth_token_required
    def get_user_by_email(user_email):
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }

        product = UserController()

        result = product.get_user_by_email(user_email=user_email)
        return Response(json.dumps(result, ensure_ascii=False),
                        mimetype='application/json'), result['status'], header

    return app
