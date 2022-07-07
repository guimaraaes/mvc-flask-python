from config import app_active, app_config
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from model.Category import Category
from model.Product import Product
from model.User import User

config = app_config[app_active]


class HomeView(AdminIndexView):
    extra_css = [config.URL_MAIN + 'static/css/home.css',
                 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']

    @expose('/')
    def index(self):
        user_model = User()
        category_model = Category()
        product_model = Product()
        users = user_model.get_total_users()
        categories = category_model.get_total_categories()
        products = product_model.get_total_products()

        last_products = product_model.get_last_products()

        return self.render('home_admin.html', report={
            'users': 0 if not users else users[0],
            'categories': 0 if not categories else categories[0],
            'products': 0 if not products else products[0]
        }, last_products=last_products)


class UserView(ModelView):
    column_exclude_list = ['password', 'recovery_code']
    form_excluded_columns = ['last_update', 'recovery_code']
    can_view_details = True
    column_sortable_list = ['username']
    column_searchable_list = ['username', 'email']
    column_editable_list = ['username', 'email']
    column_details_exclude_list = ['password', 'recovery_code']
    export_types = ['csv']
    column_export_exclude_list = ['password', 'recovery_code']
    can_export = True
    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }
    column_labels = {
        'role_relationship': 'Função',
        'username': 'Nome de usuário',
        'email': 'E-mail',
        'date_created': 'Data de criação',
        'last_update': 'Última atualização',
        'active': 'Ativo',
        'password': 'Senha',
    }

    def on_model_change(self, form, User, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)

            else:
                del form.password
