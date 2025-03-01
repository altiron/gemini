from abc import ABC, abstractmethod

import os

# Step 1: Defining the Product
# Abstract Order Class
class Order(ABC):
    def __init__(self, counter_party=None, portfolio=None, securities_code=None,trade_date=None,settlement_date=None,maturity_date=None,yields=None,unit=None,clean_price=None,accrued_interest=None,settlement_amount=None):
        self.counter_party = counter_party
        self.portfolio = portfolio
        self.securities_code = securities_code
        self.trade_date = trade_date
        self.settlement_date = settlement_date
        self.maturity_date = maturity_date
        self.yields = yields
        self.unit  = unit
        self.clean_price = clean_price
        self.accrued_interest = accrued_interest
        self.settlement_amount = settlement_amount


    @property                 
    def format(self):     
        return '%Y-%m-%d'
    
    @property
    @abstractmethod
    def counter_party(self):
        pass

    @property
    @abstractmethod
    def portfolio(self):
        pass

    @property
    @abstractmethod
    def securities_code(self):
        pass

    @property
    @abstractmethod
    def trade_date(self):
        pass

    @property
    @abstractmethod
    def settlement_date(self):
        pass

    @property
    @abstractmethod
    def maturity_date(self):
        pass

    @property
    @abstractmethod
    def yields(self):
        pass

    @property
    @abstractmethod
    def unit(self):
        pass

    @property
    @abstractmethod
    def clean_price(self):
        pass

    @property
    @abstractmethod
    def accrued_interest(self):
        pass

    @property
    @abstractmethod
    def settlement_amount(self):
        pass

    #============================
    @classmethod
    @abstractmethod
    def convert_to_text(cls, pdf_path_list):
        """Translate the given message."""
        pass

    # @abstractmethod
    # def confirm_dict(self):
    #     pass

    @classmethod
    @abstractmethod
    def convert_to_record(cls, text):
        """ """
        pass

    @classmethod
    @abstractmethod
    def find_fields(cls, matches):
        """ """
        pass
    
    @staticmethod
    def CreateTempFolder(self):
        path = os.path.dirname(os.path.abspath(__file__))
        # print(path)
        # print('--------')
        # print(os.path.dirname(path))
        self.tmp_dir = os.path.join(os.path.dirname(path), 'tmp')
        # print(TMP_DIR)

        if not os.path.exists(os.path.join(self.tmp_dir, self.counter_party)):
            os.mkdir(os.path.join(self.tmp_dir, self.counter_party))
