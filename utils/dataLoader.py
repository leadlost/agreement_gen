from product import Product
from exception import productNotExist, productAlreadyExist
from pathlib import Path
import pickle
import os
import logging


class DataLoader:

    def __init__(self):
        self.data = {'products': {}, 'id_count': 0}

    def get_product(self, pid):
        if pid not in self.data['products']:
            logging.info(f"Product id not exist: {pid}")
            raise productNotExist(f"Product id not exist: {pid}")
        return self.data['products'][pid].copy()

    def get_products_list(self):
        product_list = [(i, self.data['products'][i]) for i in self.data['products']]
        return product_list

    def add_data(self, new_product):
        assert isinstance(new_product, Product)
        for i in self.data['products'].values():
            if i == new_product:
                logging.info(f'Product already exists: {i}')
                raise productAlreadyExist(f'Product already exists: {i}')
        logging.info(f'Add product pid {self.data["id_count"]}: {new_product}')
        self.data['products'][self.data['id_count']] = new_product
        self.data['id_count'] += 1

    def del_data(self, pid):
        if pid not in self.data['products']:
            logging.info(f"Product id not exist: {pid}")
            raise productNotExist(f"Product id not exist: {pid}")
        else:
            del self.data['products'][pid]
            logging.info(f"Delete product id: {pid}, {self.data['products'][pid]}")

    def save(self, data_dir='data'):
        p = Path(data_dir)
        if not p.exists():
            logging.info(f"Create data directory: {p.resolve}")
            p.mkdir(parents=True)
        p = p / 'products.data'
        logging.info(f"Save data: {p.resolve()}")
        with p.open('wb') as f:
            pickle.dump(self.data, f)

    @staticmethod
    def sorted(product_list, key):
        """Sort by [name] or [model]"""
        assert key == 'name' or key == 'model'
        if key == 'name':
            product_list = sorted(product_list, key=lambda x: x[1].model)
            product_list = sorted(product_list, key=lambda x: x[1].name)
        elif key == 'model':
            product_list = sorted(product_list, key=lambda x: x[1].model)
        return product_list

    @staticmethod
    def search(product_list, keyword):
        """ Search by keyword in products' model and products' name"""
        result = []
        for p in product_list:
            if keyword in p[1].get_name() or keyword in p[1].get_model():
                result.append(p)
        return result

    @staticmethod
    def load(data_dir='data'):
        p = Path(data_dir) / 'products.data'
        dl = DataLoader()
        if p.exists():
            dl = DataLoader()
            with p.open('rb') as pkl_file:
                dl.data = pickle.load(pkl_file)
            logging.info(f"Load data from file: {p.resolve()}")
            return dl
        else:
            logging.info(f'No existing dir: use empty dataloader')
        return dl

    def __str__(self):
        result = ''
        for i, v in self.data['products'].items():
            result += f'id {i}:{v}\n'
        return result

    def __getitem__(self, pid):
        return self.get_product(pid)


if __name__ == '__main__':
    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    dl = DataLoader.load()

    a = Product('塑壳断路器', 'RMM1-630S/3310', '500A', '台', 1220.00, [("抽屉式", 180), ("VC3", 30.1)])
    b = Product('交流塑壳断路', 'RMM1-100S/3300', '160A', '只', 174, [("带电剩余保护模块", 88)])
    c = Product
    dl.add_data(a)
    dl.add_data(b)
    print(dl)
    # dl.save()