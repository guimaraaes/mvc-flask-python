from config import app_active, app_config
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import true

config = app_config[app_active]


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('home_admin.html', data={
            'username': 'Sara'
        })


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
