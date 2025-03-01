from classes import *

import shutil
import os,glob,time

from bblam.Logger import Logger
from bblam.Emailler import Emailler
from bblam.Configger import Configger

ConfirmationBank = ('bbl','boa','cimbt','citi','deutsche','gsb','hsbc','jp-morgan','kbank','kgi','kkp','krungsri','krungthai','scb','standard','tisco','ttb','uob')

def create_confirm(counter_party):
    counter_partys = {
        "kkp":   KKPConfirmation,
        "cimbt": CIMBTConfirmation,
    }
    
    return counter_partys[counter_party](counter_party)

def create_order(order):
    orders = {
        "mf":   MFOrder,
        "pvd": MFOrder,
    }
    
    return orders[order](order)

# def create_order(order_type):
#     order_classes = {
#         'mf': MFOrder,
#         'pvd': MFOrder
#     }
#     if order_type.lower() in order_classes:
#         return order_classes[order_type.lower()]()
#     raise ValueError("Invalid order type. Choose 'mf' or 'pvd'.")

if __name__ == '__main__':

    log = Logger('FM Dealer')
    log.logger.info("start : FM Dealer")
    config = Configger('fm_dealer')

    try:

        # Change directory
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        TMP_DIR = os.path.join(ROOT_DIR, 'tmp')
        SOURCE_DIR = config.config['source_path']

        try:
            log.logger.info("start : prepare file and directory")

            # ตรวจสอบว่าโฟลเดอร์มีอยู่หรือไม่
            if os.path.exists(TMP_DIR):
                shutil.rmtree(TMP_DIR)  # ลบโฟลเดอร์ TMP และทุกอย่างข้างใน
                print(f"ลบโฟลเดอร์ {TMP_DIR} สำเร็จ")

            # สร้างโฟลเดอร์ใหม่
            os.makedirs(TMP_DIR)
            print(f"สร้างโฟลเดอร์ {TMP_DIR} สำเร็จ")

            if not os.path.exists(TMP_DIR):
                os.mkdir(TMP_DIR)
            if not os.path.exists(SOURCE_DIR):
                os.mkdir(SOURCE_DIR)

        except Exception as e: 
            log.logger.error(f"An error occurred: {e}", exc_info=True)  # Logs the error with traceback
            exit()
        finally:
            log.logger.info("end : prepare file and directory")

        #---------------------------------------------------------------
        # ค้นหาไฟล์ PDF ทั้งหมดในโฟลเดอร์ที่ source
        pdf_files = [f.lower() for f in glob.glob(SOURCE_DIR + r"\\*.pdf", recursive=True)]
        # pdf_files = [f.lower() for f in glob.glob(os.path.join(SOURCE_DIR, "*.pdf"))]
        print(pdf_files)

    
        print('ddddddddddddddddddddddddddddddddddddddd')
        # ทำการย้านไฟล์จาก source ไปยัง tmp
        for file in pdf_files:
            try:
                shutil.move(file, TMP_DIR)
                print(f"ย้าย {file} → {TMP_DIR} สำเร็จ")
            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการย้าย {file}: {e}")
        
        print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        # ค้นหาไฟล์ PDF ทั้งหมดในโฟลเดอร์ที่ TMP   
        pdf_files = [f.lower() for f in glob.glob(TMP_DIR + r"\\*.pdf", recursive=True)]
        print(pdf_files)
        print('uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')

        # จัดกลุ่มไฟล์ตามเงื่อนไขที่กำหนด
        order_files = [f for f in pdf_files if os.path.basename(f).startswith(('mf_', 'pvd_'))]
        confirm_files = [f for f in pdf_files if os.path.basename(f).startswith(ConfirmationBank)]
        other_files = [f for f in pdf_files if f not in order_files + confirm_files]

        print('=====================================')
        print("Order : " + str(order_files))
        print("Confirm : " + str(confirm_files))
        print("Other : " + str(other_files))
        print('=====================================')

        if len(other_files) > 0:
            print("The file name is invalid : " + str(other_files))
            # จะมีการส่ง e-mail ไปบอก 
        else:

            order_dict = {}
            for f in order_files:
                # print(f)
                order = os.path.splitext(os.path.basename(f))[0].split("_")[0]
                # print(bank)
                # bank_list.append(bank)
                # bank_dict[bank] = f
                order_dict.setdefault(order,[]).append(f)

            order_ls = []
            i = 1
            for order,value in order_dict.items():
                print('pppppppppppppppppppppppppppp')
                print(order)
                od = create_order(order)
                # od = MFOrder()
                # print(od)
                text = od.convert_to_text(value)
                # print(text)
                record = od.convert_to_record(text)
                # print(record)
                a = od.find_fields(record)
                # b = cf._cf_list
                # b = od._order_ls
                # b = a
                # cf.fund_name = 'eeee'aa

                # print(cf.fund_name)
                # print(cf.confirm_dict())
                # confirm_ls.append(cf.confirm_dict())
                # confirm_ls.append(cf.confirm_ls())
                # confirm_ls.append(cf._confirm_ls)
                order_ls.append(a)
                
                print(f'i = {i}')
                i = i + 1

            print(order_ls)
            print("$$$$$$$$$$$$$========================================$$$$$$$$$$$$$")
            #$$$$$$$$$$$$$========================================$$$$$$$$$$$$$
            comfirm_dict = {}
            for f in confirm_files:
                # print(f)
                comfirm = os.path.splitext(os.path.basename(f))[0].split("_")[0]
                comfirm_dict.setdefault(comfirm,[]).append(f)

            comfirm_ls = []
            i = 1
            for comfirm,value in comfirm_dict.items():
                cf = create_confirm(comfirm)
                # print(od)
                text = cf.convert_to_text(value)
                # print(text)
                record = cf.convert_to_record(text)
                # print(record)
                a = cf.find_fields(record)
                # b = cf._cf_list
                b = cf._confirm_ls
                # cf.fund_name = 'eeee'aa

                # print(cf.fund_name)
                # print(cf.confirm_dict())
                # confirm_ls.append(cf.confirm_dict())
                # confirm_ls.append(cf.confirm_ls())
                # confirm_ls.append(cf._confirm_ls)
                comfirm_ls.append(a)
                
                print(f'i = {i}')
                i = i + 1

            # print(comfirm_ls)
            print("$$$$$$$$$$$$$========================================$$$$$$$$$$$$$")
            #$$$$$$$$$$$$$========================================$$$$$$$$$$$$$

            print(order_ls)
            print(comfirm_ls)


            # แปลงข้อมูลให้เป็น list เดียวกัน
            order_ls_flat = [item for sublist in order_ls for item in sublist]
            comfirm_ls_flat = [item for sublist in comfirm_ls for item in sublist]

            # ฟังก์ชันสำหรับตรวจสอบความตรงกันของข้อมูล
            def is_match(order, confirm):
                return (order['counter_party'].lower() == confirm['counter_party'].lower() and
                        order['portfolio'] == confirm['portfolio'] and
                        order['securities_code'] == confirm['securities_code'])

            # เก็บผลลัพธ์
            order_n_comfirm_cmp = []
            order_not_cmp = []
            comfirm_not_cmp = comfirm_ls_flat.copy()

            # ตรวจสอบการจับคู่
            for order in order_ls_flat:
                matched = False
                for confirm in comfirm_ls_flat:
                    if is_match(order, confirm):
                        order_n_comfirm_cmp.append((order, confirm))
                        comfirm_not_cmp.remove(confirm)  # ลบออกจากรายการที่ไม่ตรงกัน
                        matched = True
                        break
                if not matched:
                    order_not_cmp.append(order)

            def generate_html_report(matched_pairs, order_not_cmp, comfirm_not_cmp):
                html = "<html><head><style>table { border-collapse: collapse; width: 100%; } th, td { border: 1px solid black; padding: 8px; text-align: left; } .diff { background-color: #ffcccb; } .full-match { background-color: #ccffcc; }</style></head><body>"
                html += "<h2>Matched Orders Comparison</h2>"
                
                mismatched = []
                fully_matched = []
                
                for order, confirm in matched_pairs:
                    differences = [key for key in order.keys() if order[key] != confirm[key]]
                    if differences:
                        mismatched.append((order, confirm, differences))
                    else:
                        fully_matched.append((order, confirm))
                
                for order, confirm, differences in mismatched + [(o, c, []) for o, c in fully_matched]:
                    match_status = "Some fields do not match" if differences else "All fields match"
                    status_class = "diff" if differences else "full-match"
                    #html += f"<h3 class='{status_class}'>{match_status}</h3><table><tr><th>Source</th>"
                    html += f"<h3 class='{status_class}'>{match_status}</h3><table><tr>"
                    
                    for key in order.keys():
                        diff_class = " class='diff'" if key in differences else ""
                        html += f"<th{diff_class}>{key}</th>"
                    
                    # html += "</tr><tr><td>Order</td>"
                    html += "</tr><tr>"
                    for key in order.keys():
                        diff_class = " class='diff'" if key in differences else ""
                        html += f"<td{diff_class}>{order[key]}</td>"
                    
                    # html += "</tr><tr><td>Confirm</td>"
                    html += "</tr><tr>"
                    for key in confirm.keys():
                        diff_class = " class='diff'" if key in differences else ""
                        html += f"<td{diff_class}>{confirm[key]}</td>"
                    
                    html += "</tr></table><br>"
                
                html += "<h2>Orders Not Matched</h2><table><tr>"
                if order_not_cmp:
                    for key in order_not_cmp[0].keys():
                        html += f"<th>{key}</th>"
                    html += "</tr>"
                    for order in order_not_cmp:
                        html += "<tr>" + "".join(f"<td>{order[key]}</td>" for key in order.keys()) + "</tr>"
                else:
                    html += "<tr><td colspan='100%'>No unmatched orders</td></tr>"
                html += "</table><br>"
                
                html += "<h2>Confirms Not Matched</h2><table><tr>"
                if comfirm_not_cmp:
                    for key in comfirm_not_cmp[0].keys():
                        html += f"<th>{key}</th>"
                    html += "</tr>"
                    for confirm in comfirm_not_cmp:
                        html += "<tr>" + "".join(f"<td>{confirm[key]}</td>" for key in confirm.keys()) + "</tr>"
                else:
                    html += "<tr><td colspan='100%'>No unmatched confirms</td></tr>"
                html += "</table><br>"
                
                html += "</body></html>"
                return html

            html_report = generate_html_report(order_n_comfirm_cmp, order_not_cmp, comfirm_not_cmp)

            #-------------------------  Send email  ---------------------------
            if len(pdf_files) > 0:
                email = Emailler()
                email.sender = 'supawet.mu@bblam.co.th'
                # email.to = ['supawet.mu@bblam.co.th']
                email.to = config.config['email_to'].split(",")
                email.subject = 'ผลของการตรวจสอบ order และ confirmation ไฟล์'

                # _new_body = 'พบเซิร์ฟเวอร์มีการเปลี่ยนแปลง Service ดังนี้' + '<br/><br/>'

                email.body = html_report
                # email.attachments = os.path.join(TMP_DIR, report_file)

                email.send()

                # time.sleep(2)
                # print(pdf_files)

                # for f in pdf_files:
                #     try:
                #         f.close()
                #     except NameError:
                #         print("ไฟล์ยังไม่ได้ถูกเปิด จึงไม่ต้องปิด")
                #     except Exception as e:
                #         print(f"เกิดข้อผิดพลาด: {e}")
                #     os.remove(f)


            # with open("order_comparison_report.html", "w", encoding="utf-8") as file:
            #     file.write(html_report)

            # print("Matched Orders:", order_n_comfirm_cmp)
            # print("Orders Not Matched:", order_not_cmp)
            # print("Confirms Not Matched:", comfirm_not_cmp)
            # print("HTML report generated: order_comparison_report.html")

    except Exception as e: 
        log.logger.error(f"An error occurred: {e}", exc_info=True)  # Logs the error with traceback

    finally:
        log.logger.info("end : FM Dealer")
