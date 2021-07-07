from product import Product
from exception import productNotExist,productAlreadyExist
import pickle
import os
import logging


class DataLoader:

    def __init__(self):
        self.data = {'products': {}, 'id_count': 0}

    def get_products(self):
        return self.data['products']  # todo

    def add_data(self, name, unit, raw_price, adjunct_price, **specs):
        for i in self.data['products'].values():  # todo
            if i.specs == specs:
                logging.info(f'Product already exists: {i}')
                raise productAlreadyExist(f'Product already exists: {i}')

        new_product = Product(name, specs, unit, raw_price, adjunct_price)
        logging.info(f'Add product: {new_product}')
        self.data['products'][self.data['id_count']] = new_product
        self.data['id_count'] += 1

    def hide_data(self, id):
        # hide the specific product from user
        if id not in self.data['products']:
            logging.info(f"Product id not exist: {id}")
            raise productNotExist(f"Product id not exist: {id}")
        else:
            logging.info(f"Hide product id: {id}, {self.data['products'][id]}")
            del self.data['products'][id]

    def save(self, data_dir ='data'):
        if not os.path.exists(data_dir):
            logging.info(f"Create data directory: {data_dir}")
            os.makedirs(data_dir)
        with open(f'{data_dir}/products.data', 'wb') as f:
            logging.info(f"Save data: f'{data_dir}/products.data'")
            pickle.dump(self.data, f)

    def load(self, data_dir =f'data'):
        if os.path.exists(f'{data_dir}\\products.data'):
            logging.info(f"Load data from file: {data_dir}\\products.data")
            with open(f'{data_dir}\\products.data', 'rb') as pkl_file:
                self.data = pickle.load(pkl_file)
        else:
            logging.info(f'No existing dir: use empty dataloader')

    def __str__(self):
        result = ''
        for i, v in self.data['products'].items():
            result += f'id {i}:{v}\n'
        return result


if __name__ == '__main__':
    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    dl = DataLoader()
    dl.load()

    # dl.add_data('塑壳断路器', '台', 1220, 130, model='RMM1-630S/3310', current='500A')
    # dl.add_data('塑壳断路器', '台', 1220, 130, model='RMM1-400S/3310', current='350A')
    # dl.save_data()
    print(dl)