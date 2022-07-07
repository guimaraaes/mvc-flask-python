
from flask import Flask, redirect, render_template, request
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

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/login', methods=['GET'])
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_post():
        user = UserController()
        email = request.form['email']
        password = request.form['password']
        result = user.login(email, password)

        if result:
            return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': None})

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

    @app.route('/product', methods=['GET'])
    def get_all_products():
        product = ProductController()

        result = product.get_all_products()
        if result:
            message = result
        else:
            message = "Nenhum produto encontrado"
        return message

    @app.route('/product', methods=['POST'])
    def save_products():
        product = ProductController()

        result = product.save_product(request.form)
        if result:
            message = "Inserido"
        else:
            message = "Erro ao inserir"

        return message

    @app.route('/product', methods=['PUT'])
    def update_product():
        product = ProductController()

        result = product.update_product(request.form)
        if result:
            message = "Atualizado"
        else:
            message = "Erro ao atualizar"

        return message

    @app.route('/product', methods=['DELETE'])
    def delete_product():
        product = ProductController()

        result = product.delete_product(request.form)
        if result:
            message = "Excluído"
        else:
            message = "Erro ao excluir"

        return message

    return app
