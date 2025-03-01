from abc import ABC, abstractmethod
from .Order import Order

import datetime
import re,os

import cv2
import pytesseract
from pdf2image import convert_from_path  
from PIL import Image

from bblam.Configger import Configger

from tempfile import TemporaryDirectory

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # your path may be different
os.environ["TESSDATA_PREFIX"] = "C:\\Program Files\\Tesseract-OCR\\tessdata"

config = Configger('fm_dealer')

# Step 2: Creating Concrete Products
class MFOrder(Order):

    """Concrete Product: Represents Order for MF. ขึ้นหน้าใหม่มี header และในแต่ละหน้าคือ 1 กอง   อันนี้ยังไม่ทราบ"""
    def __init__(self, counter_party=None, portfolio=None, securities_code=None,trade_date=None,settlement_date=None,maturity_date=None,yields=None,unit=None,clean_price=None,accrued_interest=None,settlement_amount=None):
        #  super().__init__(self, counter_party=None, portfolio=None, securities_code=None,trade_date=None,settlement_date=None,maturity_date=None,yields=None,unit=None,clean_price=None,accrued_interest=None,settlement_amount=None)
        pass

    @property
    def counter_party(self):
        return self._counter_party

    @counter_party.setter
    def counter_party(self,name):
        self._counter_party = str(name)

    @property
    def portfolio(self):
        return self._portfolio

    @portfolio.setter
    def portfolio(self,name):
        self._portfolio = str(name)

    @property
    def securities_code(self):
        return self._securities_code
    
    @securities_code.setter
    def securities_code(self,code):
        self._securities_code = str(code)

    @property
    def trade_date(self):
        return self._trade_date

    @trade_date.setter
    def trade_date(self,date):
        self._trade_date = datetime.datetime.strptime(date, '%d/%m/%Y').strftime(self.format)

    @property
    def settlement_date(self):
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self,date):
        self._settlement_date = datetime.datetime.strptime(date, '%d/%m/%Y').strftime(self.format)

    @property
    def maturity_date(self):
        return self._maturity_date

    @maturity_date.setter
    def maturity_date(self,date):
        self._maturity_date = datetime.datetime.strptime(date, '%d/%m/%Y').strftime(self.format)  
    
    @property
    def yields(self):
        return self._yields
    
    @yields.setter
    def yields(self,value):
        yields = re.sub(r'\s+|,+', '', value)
        self._yields = float(yields)

    @property
    def unit(self):
        return self._unit
    
    @unit.setter
    def unit(self,value):
        unit = re.sub(r'\s+|,+', '', value)
        self._unit = float(unit)

    @property
    def clean_price(self):
        return self._clean_price
    
    @clean_price.setter
    def clean_price(self,value):
        clean_price = re.sub(r'\s+|,+', '', value)
        self._clean_price = float(clean_price)

    @property
    def accrued_interest(self):
        return self._accrued_interest
    
    @accrued_interest.setter
    def accrued_interest(self,value):
        accrued_interest = re.sub(r'\s+|,+', '', value)
        self._accrued_interest = float(accrued_interest)

    @property
    def settlement_amount(self):
        return self._settlement_amount
    
    @settlement_amount.setter
    def settlement_amount(self,value):
        settlement_amount = re.sub(r'\s+|,+', '', value)
        self._settlement_amount = float(settlement_amount)

    #========================================================
    def convert_to_text(cls, pdf_files):
        """Convert the pdf file to text."""
        # print(pdf_files)

        for f in pdf_files:
            # Store all the pages of the PDF in a variable
            image_file_list = []
            text = ''
            with TemporaryDirectory() as tempdir:
                # Create a temporary directory to hold our temporary images.
        
                """
                Part #1 : Converting PDF to images
                """
        
                pdf_pages = convert_from_path(
                    # f, 500, poppler_path=r"d:\git\poppler\Library\bin"
                    f, 500, poppler_path = config.config['poppler']   
                )
        
                # Iterate through all the pages stored above
                for page_enumeration, page in enumerate(pdf_pages, start=1):
                    # enumerate() "counts" the pages for us.
        
                    # Create a file name to store the image
                    # filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
                    filename = os.path.join(tempdir, f"page_{page_enumeration:03}.jpg")
        
                    # Save the image of the page in system
                    page.save(filename, "JPEG")
                    image_file_list.append(filename)
        
                """
                Part #2 - Recognizing text from the images using OCR
                """
        
                # with open(os.path.join(self.tmp_dir, self.custodian + '\\' + 'test.txt'), "a") as output_file:
                #     # Open the file in append mode so that
                #     # All contents of all images are added to the same file
        
                # Iterate from 1 to total number of pages
                for image_file in image_file_list:
                    print(image_file)
                    # Set filename to recognize text from
                    # Again, these files will be:
                    # page_1.jpg
                    # page_2.jpg
                    # ....
                    # page_n.jpg
    
                    # Grayscale, Gaussian blur, Otsu's threshold
                    image = cv2.imread(image_file)
                    # image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                    
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    blur = cv2.GaussianBlur(gray, (3,3), 0)
                    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

                    # Recognize the text as string in image using pytesserct
                    # custom_config = r'--oem 3 --psm 6'
                    custom_config = r'--psm 6'

                    # text = str(((pytesseract.image_to_string(Image.open(image_file)))))
                    text += str(((pytesseract.image_to_string(thresh, lang='eng', config=custom_config))))
    
                    # # Finally, write the processed text to the file.
                    # output_file.write(text)

            # self.text = self.text.replace("-\n", "")
        return text

    def convert_to_record(cls, text):
        """ """
        # pattern = r"(KIATNAKIN Confidential.*?(?=\n\n|\n*KIATNAKIN Confidential|\Z))"
        pattern = r"(BBL ASSET MANAGEMENT CO.,LTD.*?)(?=BBL ASSET MANAGEMENT CO.,LTD.|$)"
        # Find all words that end with 'ain'
        # matches = re.findall(pattern, text,  re.MULTILINE | re.DOTALL)
        matches = re.findall(pattern, text,  re.DOTALL)
        print(matches)
        return matches
    
    def find_fields(cls,matches):
        j = 1
        cf_list = []
        orders = []
        for match in matches:
            print(f'j = {j}')
            j = j + 1
            # print('match :')
            # print(match)
            # # ค้นหาคำระหว่าง "PORTFOLIO :" และ "FUND" ในบรรทัดที่ขึ้นต้นด้วย "PORTFOLIO :"
            # portfolio_pattern = r"^PORTFOLIO :\s*(.*?)\s*FUND"
            # portfolio_match = re.search(portfolio_pattern, text, re.MULTILINE)

            # portfolio_match = re.search(r"PORTFOLIO\s*:\s*(.*)", match)

            # ค้นหาคำระหว่าง "PORTFOLIO :" และ "FUND" ในบรรทัดที่ขึ้นต้นด้วย "PORTFOLIO :"
            # portfolio_pattern = r"^PORTFOLIO :\s*(.*?)\s+FUND"
            # portfolio_pattern = r"(?<=PORTFOLIO : )(.*?)(?= (CUSTODIAN|TRUSTEE))"
            # portfolio_match = re.search(portfolio_pattern, match,re.MULTILINE)

            portfolio_pattern = r"(?<=PORTFOLIO : )(.*?)(?= (CUSTODIAN|TRUSTEE))"
            portfolio_match = re.search(portfolio_pattern, match)

            if portfolio_match:
                portfolio = portfolio_match.group(0).strip()
                print(f"PORTFOLIO: {portfolio}")
                # self.portfolio = portfolio

                #============  assign to self attibute  ===========
                match2 = re.search(r"BBL ASSET MANAGEMENT CO.,LTD\.(.*)", match, re.DOTALL)

                if match2:
                    extracted_text = match2.group(1).strip()
                    print(extracted_text)
                    
                    bank = ['bbl','boa','cimbt','citi','deutsche','gsb','hsbc','jp-morgan','kbank','kgi','kkp','krungsri','krungthai','scb','standard','tisco','ttb','uob']
                    pattern = r"^(" + "|".join(bank) + r").*"

                    # ใช้ re.MULTILINE  | re.IGNORECASE เพื่อให้ regex ทำงานกับหลายบรรทัดและไม่สนใจตัวพิมพ์เล็ก-ใหญ่
                    re_matches = re.finditer(pattern, extracted_text, re.MULTILINE | re.IGNORECASE)

                    # แสดงผลลัพธ์ในรูปของ list
                    result = [re_matche.group(0).split() for re_matche in re_matches]

                    # แสดงผลลัพธ์
                    for line in result:
                        print('==============   match ===============')
                        print(line)

                        order = cls(
                            line[0].lower(),    # counter_party
                            portfolio,          # portfolio
                            line[1],            # securities_code
                            line[3],            # trade_date
                            line[4],            # settlement_date
                            line[5],            # maturity_date
                            line[6],            # yields
                            line[len(line)-5],  # unit
                            line[len(line)-4],  # clean_price
                            line[len(line)-3],  # accrued_interest
                            line[len(line)-1]   # settlement_amount
                        )
                        orders.append(order)
                        
                        # counter_party, portfolio, securities_code,trade_date,settlement_date,maturity_date,yields,unit,clean_price,accrued_interest,settlement_amount

                        # self.counter_party = line[0].lower()
                        # self.securities_code = line[1]
                        # self.trade_date = line[3]
                        # self.settlement_date = line[4]
                        # self.maturity_date = line[5]
                        # self.yields = line[6]
                        # self.unit = line[len(line)-5]
                        # self.clean_price = line[len(line)-4]
                        # self.accrued_interest = line[len(line)-3]
                        # self.settlement_amount = line[len(line)-1]

                #============  /assign to self attibute  ===========
            else:
                print('PORTFOLIO not found')
                # self.portfolio = ''

        return orders