from contract import Contract
from pathlib import Path
import datetime
from exception import FileExceed, IllegalContractNumber


def _return_information(c):
    return c.supplier, c.buyer, c.brand, c.sign_date, c.delivery_date, c.delivery_location, c.location, \
           c.payment_method, c.comments, c.others, c.supplier_location, c.supplier_bank, c.supplier_account, \
           c.supplier_tax_num, c.supplier_tel, c.buyer_location, c.buyer_bank, c.buyer_account, c.buyer_tax_num, \
           c.buyer_tel, c.name, c.contract_number


class ContractLoader:

    def __init__(self, dir='data/contract'):
        self.contracts = {}
        self.templates = {}
        self.dir = dir

        # load contracts
        contracts_path = Path(dir) / 'contract'
        if contracts_path.exists():
            for f in contracts_path.iterdir():
                cid = f.stem
                if f.suffix == '.data' and isLegalCid(cid):
                    self.contracts[cid] = Contract.load(cid, dir)

        # load templates
        template_path = Path(dir) / 'template'
        if template_path.exists():
            for f in template_path.iterdir():
                cid = f.stem
                if f.suffix == '.data' and isLegalCid(cid):
                    self.templates[cid] = Contract.load(cid, dir)

    def get_contract_list(self):
        return [(i, v.get_name()) for i, v in self.contracts.items()]

    def get_template_list(self):
        return [(i, v.get_name()) for i, v in self.templates.items()]

    def override_contract(self, contract_cid, supplier, buyer, brand, sign_date, delivery_date, delivery_location,
                          location, payment_method, comments, others, supplier_location, supplier_bank,
                          supplier_account, supplier_tax_num, supplier_tel, buyer_location, buyer_bank, buyer_account,
                          buyer_tax_num, buyer_tel, name, contract_number):
        c = self.contracts[contract_cid]
        c.supplier = supplier
        c.buyer = buyer
        c.brand = brand
        c.sign_date = sign_date
        c.delivery_date = delivery_date
        c.delivery_location = delivery_location
        c.location = location
        c.payment_method = payment_method
        c.comments = comments
        c.others = others
        c.supplier_location = supplier_location
        c.supplier_bank = supplier_bank
        c.supplier_account = supplier_account
        c.supplier_tax_num = supplier_tax_num
        c.supplier_tel = supplier_tel
        c.buyer_location = buyer_location
        c.buyer_bank = buyer_bank
        c.buyer_account = buyer_account
        c.buyer_tax_num = buyer_tax_num
        c.buyer_tel = buyer_tel
        c.name = name
        c.contract_number = contract_number
        c.save()

    def override_template(self, template_cid, supplier, buyer, brand, delivery_date, delivery_location,
                          location, payment_method, comments, others, supplier_location, supplier_bank,
                          supplier_account, supplier_tax_num, supplier_tel, buyer_location, buyer_bank, buyer_account,
                          buyer_tax_num, buyer_tel, name, contract_number):
        c = self.templates[template_cid]
        c.supplier = supplier
        c.buyer = buyer
        c.brand = brand
        c.delivery_date = delivery_date
        c.delivery_location = delivery_location
        c.location = location
        c.payment_method = payment_method
        c.comments = comments
        c.others = others
        c.supplier_location = supplier_location
        c.supplier_bank = supplier_bank
        c.supplier_account = supplier_account
        c.supplier_tax_num = supplier_tax_num
        c.supplier_tel = supplier_tel
        c.buyer_location = buyer_location
        c.buyer_bank = buyer_bank
        c.buyer_account = buyer_account
        c.buyer_tax_num = buyer_tax_num
        c.buyer_tel = buyer_tel
        c.name = name
        c.contract_number = contract_number
        c.save()

    def create_contract(self, contract_cid, supplier, buyer, brand, sign_date, delivery_date, delivery_location,
                     location, payment_method, comments, others, supplier_location, supplier_bank,
                     supplier_account, supplier_tax_num, supplier_tel, buyer_location, buyer_bank, buyer_account,
                     buyer_tax_num, buyer_tel, name, contract_number):
        if not isLegalCid(contract_number):
            raise IllegalContractNumber("Not a legal contract number.")
        c = Contract()
        c.contract_cid = contract_cid
        c.supplier = supplier
        c.buyer = buyer
        c.brand = brand
        c.sign_date = sign_date
        c.delivery_date = delivery_date
        c.delivery_location = delivery_location
        c.location = location
        c.payment_method = payment_method
        c.comments = comments
        c.others = others
        c.supplier_location = supplier_location
        c.supplier_bank = supplier_bank
        c.supplier_account = supplier_account
        c.supplier_tax_num = supplier_tax_num
        c.supplier_tel = supplier_tel
        c.buyer_location = buyer_location
        c.buyer_bank = buyer_bank
        c.buyer_account = buyer_account
        c.buyer_tax_num = buyer_tax_num
        c.buyer_tel = buyer_tel
        c.name = name
        c.contract_number = contract_number
        c.save()
        self.contracts[c.cid] = c

    def create_template(self):
        c = Contract()
        c.save(self.dir)
        self.templates[c.cid] = c

    def get_contract(self, cid):
        if cid in self.contracts:
            return _return_information(self.contracts[cid])
        elif cid in self.templates:
            return _return_information(self.templates[cid])
        else:
            raise ValueError('Cid is not exists.')

    def rename(self, cid, name):
        if cid in self.contracts:
            self.contracts[cid].name = name
        elif cid in self.templates:
            self.templates[cid].name = name
        else:
            raise ValueError('Cid is not exists.')

    def delete(self, cid):
        if cid in self.contracts:
            self.contracts[cid].delete(self.dir)
            del self.contracts[cid]
        elif cid in self.templates:
            self.templates[cid].delete(self.dir)
            del self.templates[cid]
        else:
            raise ValueError('Cid is not exists.')

    @staticmethod
    def generate_contract_num(date, dir='data/contract'):
        """date: (year, month, date)"""
        p = Path(dir) / 'contract'
        pre_six = '{}{:0>2d}{:0>2d}'.format(str(date[0])[-2:], int(date[1]), int(date[2]))
        if not p.exists():
            return pre_six + '01'
        check_occupy = [True] * 99
        for i in p.iterdir():
            if i.stem.startswith(pre_six[:4]):
                check_occupy[int(i.stem[6:8]) - 1] = False
        last_two = None
        for i, not_occupy in enumerate(check_occupy):
            if not_occupy:
                last_two = i + 1
                break
        if not last_two:
            raise FileExceed(f'Contract for {pre_six} exceed 100.')
        return '{}{:0>2d}'.format(pre_six, last_two)

    @staticmethod
    def get_today():
        today = datetime.date.today()
        return str(today.year), str(today.month), str(today.day)


def isLegalCid(cid):
    if type(cid) != str:
        return False
    if len(cid) != 8:
        return False
    if not cid[:8].isnumeric():
        return False
    if cid.startswith('0000'):
        return True
    try:
        datetime.datetime(2000 + int(cid[:2]), int(cid[2:4]), int(cid[4:6]))
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    import os
    import logging
    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.WARNING)
    cl = ContractLoader()