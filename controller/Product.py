from datetime import datetime

from model.Product import Product


class ProductController():
    def __init__(self):
        self.product_model = Product()

    def get_all_products(self, limit):
        result = []
        try:
            res = self.product_model.get_all(limit=limit)
            for r in res:
                result.append({
                    'id': r.id,
                    'name': r.name,
                    'description': r.description,
                    'quantity': str(r.quantity),
                    'price': str(r.price),
                    'image': r.image,
                    'date_created': r.date_created
                })
                status = 200
        except Exception as e:
            result = []
            status = 400
            print(e)
        finally:
            return {
                'result': result,
                'status': status
            }

    def get_product_by_id(self, product_id):
        result = {}
        try:
            self.product_model.id = product_id
            res = self.product_model.get_product_by_id()
            result = {
                'id': res.id,
                'name': res.name,
                'description': res.description,
                'quantity': str(res.quantity),
                'price': str(res.price),
                'image': res.image,
                'date_created': res.date_created
            }
            status = 200
        except Exception as e:
            result = []
            status = 400
            print(e)
        finally:
            return {
                'result': result,
                'status': status
            }

    def save_product(self, obj):
        try:
            self.product_model.name = obj['name']
            self.product_model.description = obj['description']
            self.product_model.qtd = obj['quantity']
            self.product_model.price = obj['price']
            self.product_model.date_created = datetime.now()
            self.product_model.status = 1
            self.product_model.category = obj['category']
            self.product_model.user_created = obj['user_created']
            self.product_model.save()
            result = "Cadastrado"
            status = 200
        except Exception as e:
            result = "Falha ao cadastrar"
            status = 400
            print(e)
        finally:
            return {
                'result': result,
                'status': status
            }

    def update_product(self, obj):
        try:
            self.product_model.update(obj)
            result = "Atualizado"
            status = 200
        except Exception as e:
            result = "Falha ao atualizar"
            status = 400
            print(e)
        finally:
            return {
                'result': result,
                'status': status
            }

    def delete_product(self):
        try:
            self.product_model.delete()
            result = "Excluído"
            status = 200
        except Exception as e:
            result = "Falha ao excluir"
            status = 400
            print(e)
        finally:
            return {
                'result': result,
                'status': status
            }
