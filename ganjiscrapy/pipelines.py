# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class GanjiscrapyPipeline(object):
    def process_item(self, item, spider):
        dirname=item["dirname"]
        filename=item["filename"]
        if dirname=="深圳房产":
            dirpath=r"D:\PYTHON.XIAO\赶集网\\" +dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file1:
                price=item["price"]
                im=item["im"]
                title=item["title"]
                dress=item["dress"]
                hre=item["hre"]
                file1.write((im+" "+price + "##" + title + "##" + dress+" "+hre+"\r\n").encode("utf-8","ignore"))
            pass
        elif dirname=="二手车":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file2:
                price=item["price"]
                im=item["im"]
                title=item["title"]
                storename=item["storename"]
                hre=item["hre"]
                carage=item["carage"]
                file2.write((im+" "+"##" + title + "##" + carage + "##" + price + "##" + storename+" "+hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname=="新车":
            pass
        elif dirname=="汽车服务":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file4:
                info=item["info"]
                im=item["im"]
                title=item["title"]
                phone=item["phone"]
                hre=item["hre"]
                file4.write((im+" "+"##" + title + "##" + info + "##" + phone +" "+hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname=="招商加盟":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file5:
                info=item["info"]
                im=item["im"]
                title=item["title"]
                phone=item["phone"]
                hre=item["hre"]
                file5.write((im+" "+"##" + title + "##" + info + "##" + phone+" "+hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname=="深圳招聘":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file6:
                price=item["price"]
                company=item["company"]
                title=item["title"]
                dress=item["dress"]
                hre=item["hre"]
                file6.write((title + "##" + price + "##" + company + "##" + dress +" "+hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname=="二手市场":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file7:
                price=item["price"]
                title=item["title"]
                dress=item["dress"]
                hre=item["hre"]
                im=item["im"]
                file7.write((im+" "+"##" + title + "##" + dress + "##" + price+" "+hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname == "宠物":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file8:
                price=item["price"]
                title=item["title"]
                dress=item["dress"]
                hre=item["hre"]
                im=item["im"]
                file8.write((im+" "+"##" + title + "##" + price + "##" + dress +" "+hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname == "票务卡券":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file9:
                price=item["price"]
                title=item["title"]
                dress=item["dress"]
                hre=item["hre"]
                datatime=item["datatime"]
                file9.write((datatime+"##" + title + "##" + price + "##" + dress+" "+hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname == "到家生活服务":
            pass
        elif dirname == "本地生活服务":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file11:
                im=item["im"]
                title=item["title"]
                info=item["info"]
                hre=item["hre"]
                phone=item["phone"]
                file11.write((im+" "+"##" + title + "##" + info + "##" + phone+" "+hre+"\r\n").encode("utf-8"))
                pass
        elif dirname == "装修建材":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file12:
                im = item["im"]
                title = item["title"]
                info = item["info"]
                hre = item["hre"]
                phone = item["phone"]
                file12.write((im + " " + "##" + title + "##" + info + "##" + phone + " " + hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname == "婚庆摄影":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file13:
                im = item["im"]
                title = item["title"]
                info = item["info"]
                hre = item["hre"]
                phone = item["phone"]
                file13.write((im + " " + "##" + title + "##" + info + "##" + phone + " " + hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname == "旅游休闲":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file14:
                im = item["im"]
                title = item["title"]
                info = item["info"]
                hre = item["hre"]
                phone = item["phone"]
                file14.write((im + " " + "##" + title + "##" + info + "##" + phone + " " + hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname == "本地商务服务":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file15:
                im = item["im"]
                title = item["title"]
                info = item["info"]
                hre = item["hre"]
                phone = item["phone"]
                file15.write((im + " " + "##" + title + "##" + info + "##" + phone + " " + hre+"\r\n").encode("utf-8","ignore"))
                pass
        elif dirname == "教育培训":
            dirpath = r"D:\PYTHON.XIAO\赶集网\\" + dirname
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            with open(dirpath + "\\" + filename + ".txt", "ab") as file16:
                im=item["im"]
                title=item["title"]
                info=item["info"]
                hre=item["hre"]
                dress=item["dress"]
                file16.write((im+" "+"##" + title + "##" + info + "##" + dress +" "+hre+"\r\n").encode("utf-8","ignore"))
                pass
        return item
