# fm dealer confirmation
ทาง FM Dealer ขอให้ช่วยประเมินว่าสามารถตรวจสอบไฟล์ในกลุ่ม Order เทียบกับไฟล์ “CF MF” กับ “รวมรูปแบบ confirmation” ได้หรือไม่ครับ

## environment spec
- python version  
- pip3 install tabula

## env
- py -m pip3 install --upgrade pip
- py -m pip3 install --user virtualenv  --update
- py -m venv env_313

> python -m venv -p (python-exe-path) env-name
> example
> py -m virtualenv -p C:\Python\Python313\python.exe env_3131
  
- .\env_3131\Scripts\activate
- deactivate

-- pip3 install --upgrade pip
## offline
- pip3 install --upgrade setuptools wheel twine
- 
- pip3 freeze > requirements.txt
- mkdir wheelhouse && pip3 download -r requirements.txt -d wheelhouse    
- -- run in cmd

[comment]: # (move requirements.txt to wheelhouse folder)

- pip3 install -r wheelhouse/requirements.txt --no-index --find-links wheelhouse
- # bblam
- pip3 show <package>    -- แสดงรายละเอียดของ package ที่เรา install  พร้อมพาธ
- pip3 list -v           -- อยากจะดูเฉพาะพาธของ package ที่เรา install

- config  status    prod = prodution    dev = development
- การอ่านไฟล์ config ใดๆ ต้องใช้ class mี่เป็นเชิง prototype อ่านออกมาก่อนเท่านั้น  เผื่อในอนาคตมีการเปลี่ยนแปลงวิธีการอ่าน อย่างเช่นการเข้ารหัส

================================================================================
Assume that the content of YourClass.py is:

class YourClass:
    # ......

If you use:
  from YourClassParentDir import YourClass  # means YourClass.py

In this way, you will get TypeError: 'module' object is not callable if you then tried to call YourClass().

But, if you use:
    from YourClassParentDir.YourClass import YourClass   # means Class YourClass

or use YourClass.YourClass(), it works.
================================================================================

