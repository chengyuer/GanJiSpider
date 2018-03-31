# -*- coding: utf-8 -*-
import re
import scrapy
import ganjiscrapy.items
import lxml
import lxml.etree
import requests
import time
from bs4 import BeautifulSoup

class FuckganjiSpider(scrapy.Spider):
    name = 'fuckganji'
    allowed_domains = ['ganji.com']
    start_urls = ['http://sz.ganji.com/']
    flist = ['家教', '小时工',
             '学生兼职', '手工制作', '翻译', '促销员',
             '调查问卷', '设计制作', '模特', '服务员',
             '传单派发', '网站建设', '销售', '摄影师',
             '礼仪小姐', '其他兼职', '会计', '实习生',
             '酒吧KTV', '更多兼职', ]
    selist = ['销售', '餐饮酒店',
              '人力资源', '技工', '超市百货', '通信网络',
              '客服', '贸易运输', '生产制作', '行政',
              '家政安保', '金融投资', '财务', '市场公关',
              '更多简历']
    ershouflist = ['商用办公', '打印机', '投影仪',
                   '设备办公', '展柜货架', '五金机械', '农业产品',
                   '苗木/水产', '农用机械', '工艺品', '艺术收藏']
    ershouslist = ['热门推荐', '手机', '电脑', '金银',
                   '家用回收', '家具', '电器', '礼品',
                   '商用回收', '办公', '数码', '设备']
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "lxml")
        t = soup.find_all(class_=re.compile("^category.*"))
        dirname=None
        for i in t:
            dirname = i.find_all("h3")[0].find_all("a")[0].get_text()

            name = i.find_all("a")
            print("--------",dirname,"-------------")

            for a in name:
                    tage = a.parent.name
                    if tage != "h3":
                        item = ganjiscrapy.items.GanjiscrapyItem()
                        item["dirname"] = dirname
                        h = a["href"]
                        filename = a.get_text()
                        if h.find("ganji.com") == -1:
                            h = "http://sz.ganji.com/" + h
                        else:
                            h = ""
                        item["filename"]=filename
                        if len(h)!=0:
                            yield scrapy.Request(url=h,callback=self.main,meta={"meta":item})
    def main(self,response):
        # print("-------------")
        dirname=response.meta["meta"]["dirname"]
        filename=response.meta["meta"]["filename"]
        data=response.body
        item=response.meta["meta"]
        if dirname=="深圳房产":
            print("crawl---------------", dirname)
            if filename=="小区":
                mtree = lxml.etree.HTML(data)
                mlist = mtree.xpath("//*[@class=\"list-img\"]")
                mlist = mtree.xpath("//*[@class=\"list-img list-xq clearfix\"]")
                n=mtree.xpath("*//a[@class=\"next\"]/@href")
                for m in mlist:
                   try:
                        im = m.xpath(".//img/@src")[0]
                        title = m.xpath(".//*[@class=\"info-title\"]/a/text()")[0]
                        hre = m.xpath(".//*[@class=\"info-title\"]/a/@href")[0]
                        ds = m.xpath(".//*[@class=\"xiaoqu-street\"]//text()")
                        ps = m.xpath(".//*[@class=\"list-part\"]//text()")

                        dress = ""
                        price = ""
                        # print(ds)
                        for p in ps:
                            price += p.strip().replace("\n", "").replace("\xa0", "")
                        for d in ds:
                            dress += d.strip().replace("\n", "").replace("\xa0", "")
                        item["price"]=price
                        item["im"]=im
                        item["title"]=title
                        item["dress"]=dress
                        item["hre"]=hre
                        print(im, price + "##" + title + "##" + dress + "##", hre)
                        yield item
                   except:
                       print("fuck__________________________________")
                if len(n)!=0:
                    newn = "http://sz.ganji.com" + n[0]
                    yield scrapy.Request(url=newn,callback=self.main,meta={"meta":item})

            elif filename=="日租短租" or filename=="写字楼" or filename=="出租" or filename=="出售":


                mtree = lxml.etree.HTML(data)
                mlist = mtree.xpath("//*[@class=\"list-img\"]")
                n = mtree.xpath("*//a[@class=\"next\"]/@href")
                for m in mlist:
                    try:
                        im = m.xpath(".//img/@src")[0]
                        title = m.xpath(".//*[@class=\"info-title\"]/a/text()")[0]
                        hre = m.xpath(".//*[@class=\"info-title\"]/a/@href")[0]
                        ds = m.xpath(".//*[@class=\"list-word\"]//text()")
                        ps = m.xpath(".//*[@class=\"price\"]//text()")
                        dress = ""
                        price = ""
                        for d in ds:
                            dress += d.strip().replace("\n", "").replace(" ", "")
                        for p in ps:
                            price += p.strip().replace("\n", "").replace(" ", "")
                        if hre.find("http") == -1:
                            hre = "http://sz.ganji.com" + hre
                        item["price"] = price
                        item["im"] = im
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        print(im, price + "##" + title + "##" + dress + "##", hre)
                        yield item
                    except:
                        print("fuck___________________________________")
                if len(n) != 0:
                    newn = "http://sz.ganji.com" + n[0]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
            else:
                mtree = lxml.etree.HTML(data)
                mlist = mtree.xpath("//*[@class=\"f-list-item-wrap f-clear\"]")
                n = mtree.xpath("*//a[@class=\"next\"]/@href")
                for i in mlist:
                    try:
                        ps = i.xpath(".//*[@class=\"price\"]//text()")
                        price = ""
                        for p in ps:
                            price += p.strip().replace("\n", "").replace(" ", "")
                        im = i.xpath("./*[@class=\"img\"]//img/@src")[0]
                        title = i.xpath(".//*[@class=\"dd-item title\"]/a/text()")[0]
                        hre = i.xpath(".//*[@class=\"dd-item title\"]/a/@href")[0]
                        if hre.find("http") == -1:
                            hre = "http://sz.ganji.com" + hre
                        cs = i.xpath(".//*[@class=\"dd-item size\"]//text()")
                        ds = i.xpath(".//*[@class=\"dd-item address\"]//text()")
                        # print(ds)
                        content = ""
                        dress = ""
                        for c in cs:
                            content += c.strip()
                        for d in ds:
                            dress += d.strip().replace("\n", "").replace(" ", "")
                        title += content
                        item["price"] = price
                        item["im"] = im
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        print(im, price + "##" + title + "##" + dress + "##", hre)
                        yield item
                    except:
                        print("fuck_____________________________________")
                if len(n) != 0:
                    newn = "http://sz.ganji.com" + n[0]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})

        elif dirname=="二手车":
            print("crawl---------------",dirname)
            if filename=="工程车":
                pass
            elif filename=="货车":
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all("dl", class_=re.compile("^list-pic.*"))
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        im = m.find_all("img")[0]["src"]
                        title = m.find_all("p", class_="infor-titbox")[0].find("a").get_text().strip()
                        hre = m.find_all("p", class_="infor-titbox")[0].find("a")["href"]
                        price = m.find_all("dd", class_="digit")[0].get_text()
                        cs = m.find_all("p", class_="infor-dep")
                        storename = "no store--"
                        # print(cs)
                        carage = ""
                        for c in cs:
                            carage += c.get_text().strip().replace("\n", "").replace(" ", "")
                        if carage == "":
                            carage = "no carage"
                        # print("=====")
                        if hre.find("http") == -1:
                            hre = "http://sz.ganji.com" + hre
                        item["price"] = price
                        item["im"] = im
                        item["title"] = title
                        item["storename"] = storename
                        item["hre"] = hre
                        item["carage"]=carage
                        print(im, "##" + title + "##" + carage + "##" + price + "##" + storename, hre)
                        yield item
                    except:
                        print("fuck_____________________________________")
                if len(n) != 0:
                    print("1 lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
            elif filename=="摩托车":
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all("tr", class_=re.compile("^zzinfo.*"))

                span = soup.find_all("span")
                n = ""
                for sp in span:

                    if sp.get_text() == "下一页":
                        n = sp.parent["href"]
                for m in mlist:
                    try:
                        im = m.find_all("img")[0]["src"]
                        title = m.find_all(class_="t")[0].a.get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.find_all(class_="t")[0].a["href"]
                        carage = "no find"
                        price = m.find_all("span", class_="pricebiao")[0].get_text()
                        storename = m.find_all("span", class_="desc")[0].get_text().strip().replace("\n", "").replace(
                            " ", "")
                        item["price"] = price
                        item["im"] = im
                        item["title"] = title
                        item["storename"] = storename
                        item["hre"] = hre
                        item["carage"] = carage
                        print(im, "##" + title + "##" + carage + "##" + price + "##" + storename, hre)
                        yield item
                    except:
                        print("fuck________________________________________")
                if len(n) != 0:
                    print("2  lailai====================================")
                    newn = "http://sz.ganji.com" + n
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
            elif filename=="拖拉机":
                pass
            else:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all(id=re.compile("^puid-.*"))
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        tagelist = m.find_all("img")[0].attrs

                        f = 'data-original'
                        if (f not in tagelist):
                            im = m.find_all("img")[0]["src"]
                        else:
                            im = m.find_all("img")[0]["data-original"]
                        title = m.find_all("a", class_="infor-title pt_tit js-title")[0].get_text().strip()
                        hre = m.find_all("a", class_="infor-title pt_tit js-title")[0]["href"]
                        carage = m.find_all(class_="js-license")[0].get_text().strip() + \
                                 m.find_all(class_="js-roadHaul")[
                                     0].get_text().strip()
                        price = m.find_all(class_="v-Price")[0].get_text().strip()
                        sts = m.find_all(class_="fc-gray")
                        storename = ""
                        for st in sts:
                            storename += st.get_text().strip()
                        item["price"] = price
                        item["im"] = im
                        item["title"] = title
                        item["storename"] = storename
                        item["hre"] = hre
                        item["carage"] = carage
                        print(im, "##" + title + "##" + carage + "##" + price + "##" + storename, hre)
                        yield item
                    except:
                        print("fuck____________________________")
                if len(n) != 0:
                    print("3  lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
        elif dirname=="新车":
            print("crawl---------------", dirname)
            pass
        elif dirname=="汽车服务":
            print("crawl---------------", dirname)
            soup = BeautifulSoup(data, "lxml")
            mlist = soup.find_all(class_=re.compile("^list.+img$"))
            n = soup.find_all("a", class_="next")

            for m in mlist:
                try:
                    info = ""
                    hre = ""
                    title = ""
                    im = ""
                    phone = ""
                    if m["class"][0] == "list-img":
                        im = m.find_all("img")[0]["src"]

                        if im.find("http") == -1:
                            im = "http:" + im
                        titles = m.find_all("p", class_="t")
                        if len(titles) != 0:
                            title = titles[0].a.get_text().strip().replace("\n", "").replace(" ", "")
                            hre = titles[0].a["href"]
                        else:
                            title = "no found"
                            hre = " no found"

                        infos = m.find_all(class_="intro")
                        if len(infos) != 0:
                            info = infos[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            info = "no found"
                        phone = m.find_all(class_="list-r-area")[0].get_text().strip().replace("\n", "").replace(" ",
                                                                                                                 "")

                    elif m["class"][0] == "list-noimg":
                        im = " no found"
                        title = m.find_all(class_="txt")[0].p.get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.find_all(class_="txt")[0].a["href"]
                        infos = m.find_all("span", class_="fl p1")
                        if len(infos) != 0:
                            info = infos[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            info = "no found"
                        phone = m.find_all(class_="list-r-area")[0].get_text().strip().replace("\n", "").replace(" ",
                                                                                                                 "")

                    if hre.find("ganji") == -1:
                        hre = "http://sz.ganji.com" + hre
                    else:
                        hre = "http:" + hre

                    if len(phone) == 0:
                        phone = "no phone"
                    item["info"] = info
                    item["im"] = im
                    item["title"] = title
                    item["phone"] = phone
                    item["hre"] = hre
                    print(im, "##" + title + "##" + info + "##" + phone + "##", hre)
                    yield item
                except:
                    print("fuck___________________________________")
            if len(n) != 0:
                print("3  lailai====================================")
                newn = "http://sz.ganji.com" + n[0]["href"]
                yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})

        elif dirname=="招商加盟":
            print("crawl---------------", dirname)
            soup = BeautifulSoup(data, "lxml")
            mlist = soup.find_all(class_=re.compile("^list.+img$"))
            n = soup.find_all("a", class_="next")

            for m in mlist:
                try:
                    info = ""
                    hre = ""
                    title = ""
                    im = ""
                    phone = ""
                    if m["class"][0] == "list-img":
                        im = m.find_all("img")[0]["src"]

                        if im.find("http") == -1:
                            im = "http:" + im
                        titles = m.find_all("p", class_="t")
                        if len(titles) != 0:
                            title = titles[0].a.get_text().strip().replace("\n", "").replace(" ", "")
                            hre = titles[0].a["href"]
                        else:
                            title = "no found"
                            hre = " no found"

                        infos = m.find_all(class_="intro")
                        if len(infos) != 0:
                            info = infos[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            info = "no found"
                        phone = m.find_all(class_="list-r-area")[0].get_text().strip().replace("\n", "").replace(" ",
                                                                                                                 "")

                    elif m["class"][0] == "list-noimg":
                        im = " no found"
                        title = m.find_all(class_="txt")[0].p.get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.find_all(class_="txt")[0].a["href"]
                        infos = m.find_all("span", class_="fl p1")
                        if len(infos) != 0:
                            info = infos[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            info = "no found"
                        phone = m.find_all(class_="list-r-area")[0].get_text().strip().replace("\n", "").replace(" ",
                                                                                                                 "")

                    if hre.find("ganji") == -1:
                        hre = "http://sz.ganji.com" + hre
                    else:
                        hre = "http:" + hre

                    if len(phone) == 0:
                        phone = "no phone"
                    item["info"] = info
                    item["im"] = im
                    item["title"] = title
                    item["phone"] = phone
                    item["hre"] = hre
                    print(im, "##" + title + "##" + info + "##" + phone + "##", hre)
                    yield item
                except:
                    print("fuck___________________________________")
            if len(n) != 0:
                print("3  lailai====================================")
                newn = "http://sz.ganji.com" + n[0]["href"]
                yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
            pass
        elif dirname=="深圳招聘":
            print("crawl---------------", dirname)
            if filename in self.flist:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all("dl", class_="list-noimg job-list clearfix")
                n = soup.find_all("a", class_="next")
                print(len(mlist))
                for m in mlist:
                    try:
                        title = m.dt.a.get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.dt.a["href"]
                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        company = m.find_all(class_="company")[0].get_text().strip().replace("\n", "").replace(" ", "")
                        price = "面议 "
                        dr = m.find_all(class_="pay")
                        if len(dr) != 0:
                            dress = dr[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            dress = ""
                        item["price"] = price
                        item["company"] = company
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        print(title + "##" + price + "##" + company + "##" + dress + "##", hre)
                        yield item
                    except:
                        print("fuck_____________________________________")
                if len(n) != 0:
                    print("0  lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
            elif filename in self.selist:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all("dl", class_="list-noimg job-j-list clearfix job-new-list")
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        title = "zhiliao>>" + m.find_all(class_="basic-info")[0].get_text().strip().replace("\n",
                                                                                                            "").replace(
                            " ", "")
                        hre = m.find_all("a", class_="fl")[0]["href"]
                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        company = "zidingyi-.-"
                        dress = m.find_all("p", class_="district")[0].get_text().strip().replace("\n", "").replace(" ",
                                                                                                                   "")
                        price = m.find_all("p", class_="salary")[0].get_text().strip().replace("\n", "").replace(" ","")
                        item["price"] = price
                        item["company"] = company
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        print(title + "##" + price + "##" + company + "##" + dress + "##", hre)
                        yield item
                    except:
                        print("fuck____________________________________")
                if len(n) != 0:
                    print("1  lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
            elif filename=="放心企业":
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all("dl", class_="normal-fir tl-cate-list clearfix")
                n = soup.find_all("a", class_="next")
                print(len(mlist))
                for m in mlist:
                    try:
                        title = m.dt.a.get_text()
                        hre = m.dt.a["href"]
                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        company = m.find_all("em", class_="display sty-4b")[0].a.get_text()
                        price = m.find_all("span", class_="ml-5")[0].get_text()
                        dress = m.find_all("span", class_="ml-5")[0].next_sibling.get_text()
                        item["price"] = price
                        item["company"] = company
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        print(title + "##" + price + "##" + company + "##" + dress + "##", hre)
                        yield item
                    except:
                        print("fuck_____________________________________")
                if len(n) != 0:
                    print("2  lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
            else:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all("dl", class_=re.compile(".+new-dl$"))
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        title = m.dt.a.get_text()
                        hre = m.dt.a["href"]
                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        company = m.dt.find_all(class_="new-dl-company")[0].a.get_text().strip().replace("\n",
                                                                                                         "").replace(
                            " ", "")
                        price = m.find_all(class_="company")[0].get_text().strip().replace("\n", "").replace(" ", "")
                        dress = m.find_all(class_="pay")[0].get_text().strip().replace("\n", "").replace(" ", "")
                        item["price"] = price
                        item["company"] = company
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        print(title + "##" + price + "##" + company + "##" + dress + "##", hre)
                        yield item
                    except:
                        print("fuck________________________________________")
                if len(n) != 0:
                    print("3  lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
        elif dirname=="二手市场":
            print("crawl---------------", dirname)
            if filename=="闲置换钱":
                pass
            elif filename in self.ershouflist:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all(class_="list-bigpic clearfix")
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        title = m.find_all(class_="ft-db")[0].get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.find_all(class_="ft-db")[0].a["href"]
                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        im = m.find_all("img")[0]["src"]
                        if im.find("http"):
                            im = "http:" + im
                        dress = m.find_all("span")[-2].get_text() + m.find_all("span")[-3].get_text()
                        dress = dress.strip().replace("\n", "").replace(" ", "")
                        if len(dress) == 0:
                            dress = "no dress"
                        prs = m.find_all(class_="pt-price")
                        if len(prs) != 0:
                            price = prs[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            price = "no price"
                        item["price"] = price
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        item["im"]=im
                        print(im, "##" + title + "##" + dress + "##" + price + "##", hre)
                        yield item
                    except:
                        print("fuck_____________________________________")
                if len(n) != 0:
                    print("1 lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
            elif filename in self.ershouslist:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all(class_=re.compile("^list.+img$"))
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        title = m.find_all(class_="txt")[0].get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.find_all(class_="txt")[0].a["href"]
                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        drs = m.find_all(class_="p2")
                        if len(drs) != 0:
                            dress = drs[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            dress = "no dress"
                        ims = m.find_all("img")
                        if len(ims) != 0:
                            im = ims[0]["src"]
                        else:
                            im = "no img"
                        if im.find("http"):
                            im = "http:" + im
                        prs = m.find_all(class_="J_tel_phone_span")
                        if len(prs) != 0:
                            price = "phone>>" + prs[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            price = "no phone"
                        item["price"] = price
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        item["im"]=im
                        print(im, "##" + title + "##" + dress + "##" + price + "##", hre)
                        yield item
                    except:
                        print("fuck__________________________________")
                if len(n) != 0:
                    print("2  lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
                pass
            else:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all(class_=re.compile("^zzinfo.*"))
                span = soup.find_all("span")
                n = ""
                for sp in span:
                    if sp.get_text() == "下一页":
                        n = sp.parent["href"]
                for m in mlist:
                    try:
                        title = m.find_all(class_="t")[0].a.get_text()
                        hre = m.find_all(class_="t")[0].a["href"]
                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        im = m.find_all("img")[0]["src"]
                        if im.find("http"):
                            im = "http:" + im
                        prs = m.find_all("span", class_="pricebiao")
                        if len(prs) != 0:
                            price = prs[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            price = "no price"
                        drs = m.find_all("span", class_="fl")
                        if len(drs) != 0:
                            dress = drs[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            dress = "no dress"
                        item["price"] = price
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        item["im"]=im
                        print(im, "##" + title + "##" + dress + "##" + price + "##", hre)
                        yield item
                    except:
                        print("fuck____________________________________")
                if len(n) != 0:
                    print("3  lailai====================================")
                    newn = "http://sz.ganji.com" + n
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        elif dirname=="宠物":
            print("crawl---------------", dirname)
            soup = BeautifulSoup(data, "lxml")
            mlist = soup.find_all(class_="list-pic info-tworows ")
            n = soup.find_all("a", class_="next")
            print(len(mlist))
            for m in mlist:
                try:
                    title = m.find_all(class_="infor-title")[0].a.get_text().strip().replace("\n", "").replace(" ", "")
                    hre = m.find_all(class_="infor-title")[0].a["href"]
                    if hre.find("http") == -1:
                        hre = " http://sz.ganji.com" + hre
                    ims = m.find_all("img")
                    if len(ims) != 0:
                        im = ims[0]["src"]
                        if im.find("http") == -1:
                            im = "http:" + im
                    else:
                        im = "no img"
                    prs = m.find_all(class_="fc-org f14")
                    if len(prs) != 0:
                        price = prs[0].get_text().strip().replace("\n", "").replace(" ", "")
                    else:
                        price = "no price"
                    drs = m.find_all(class_="list-word")
                    if len(drs) != 0:
                        dress = drs[0].get_text().strip().replace("\n", "").replace(" ", "")
                    else:
                        dress = "no dress"
                    item["price"] = price
                    item["title"] = title
                    item["dress"] = dress
                    item["hre"] = hre
                    item["im"]=im
                    print(im, "##" + title + "##" + price + "##" + dress + "##", hre)
                    yield item
                except:
                    print("fuck________________________________")
            if len(n) != 0:
                print("1 lailai====================================")
                newn = "http://sz.ganji.com" + n[0]["href"]
                yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        elif dirname=="票务卡券":
            print("crawl---------------", dirname)
            if filename=="电话卡":
                pass
            else:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all(class_="list-nopic")
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        title = m.find_all(class_="infor01")[0].a.get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.find_all(class_="infor01")[0].a["href"]
                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        dtime = m.find_all(class_="time fc-70")
                        if len(dtime) != 0:
                            datatime = dtime[0].get_text().strip().replace("\n", "").replace(" ", "")
                        else:
                            datatime = "no datatime"
                        prs = m.find_all(class_="list-word")
                        if len(prs) != 0:
                            price = prs[0].get_text().strip().replace("\n", "").replace(" ", "")
                            if price.find("-") != -1:
                                price = price.split("-")[1]
                        else:
                            price = "no price"
                        drs = m.find_all(class_="list-word")
                        if len(drs) != 0:
                            dress = drs[0].get_text().strip().replace("\n", "").replace(" ", "")
                            if dress.find("-") != -1:
                                dress = dress.split("-")[0]

                        else:
                            dress = "no dress"
                        if len(dress) == 0:
                            dress = "no dress"
                        if len(price):
                            price = "no price"
                        item["price"] = price
                        item["title"] = title
                        item["dress"] = dress
                        item["hre"] = hre
                        item["datatime"]=datatime
                        print(datatime, "##" + title + "##" + price + "##" + dress + "##", hre)
                        yield item
                    except:
                        print("fuck_______________________________")
                if len(n) != 0:
                    print("1 lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        elif dirname=="到家生活服务":
            print("crawl---------------", dirname)
            pass
        elif dirname=="本地生活服务":
            print("crawl---------------", dirname)
            if filename=="搬家估价" or filename=="无忧装修" or filename=="金牌商家":
                pass
            else:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all(class_=re.compile("^list.+img$"))
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        title = m.find_all(class_="txt")[0].p.get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.find_all(class_="txt")[0].p.a["href"]

                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        ims = m.find_all("img")
                        if len(ims) != 0:
                            im = ims[0]["src"]
                            if im.find("http") == -1:
                                im = "http:" + im
                        else:
                            im = "no img"
                        phone = m.find_all(class_="list-r-area")[0].span.get_text().strip().replace("\n", "").replace(
                            " ", "")
                        if len(phone) == 0:
                            phone = "no phone"
                        infos = m.find_all(class_="txt")
                        info = ""
                        if len(infos) != 0:
                            count = 0
                            for ch in infos[0].children:
                                count += 1
                                try:
                                    if count == 4:
                                        info = ch.get_text().strip().replace("\n", "").replace(" ", "")
                                except:
                                    info = "no info"
                        else:
                            info = "no info"
                        item["im"] = im
                        item["title"] = title
                        item["info"] = info
                        item["hre"] = hre
                        item["phone"] = phone
                        print(im, "##" + title + "##" + info + "##" + phone + "##", hre)
                        yield item
                    except:
                        print("fuck________________________________")
                if len(n) != 0:
                    print("1 lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        elif dirname=="装修建材":
            print("crawl---------------", dirname)
            if filename=="服务" or filename=="效果图":
                pass
            else:
                soup = BeautifulSoup(data, "lxml")
                mlist = soup.find_all(class_=re.compile("^list.+img$"))
                n = soup.find_all("a", class_="next")
                for m in mlist:
                    try:
                        title = m.find_all(class_="txt")[0].p.get_text().strip().replace("\n", "").replace(" ", "")
                        hre = m.find_all(class_="txt")[0].p.a["href"]

                        if hre.find("http") == -1:
                            hre = " http://sz.ganji.com" + hre
                        ims = m.find_all("img")
                        if len(ims) != 0:
                            im = ims[0]["src"]
                            if im.find("http") == -1:
                                im = "http:" + im
                        else:
                            im = "no img"
                        phone = m.find_all(class_="list-r-area")[0].span.get_text().strip().replace("\n", "").replace(
                            " ", "")
                        if len(phone) == 0:
                            phone = "no phone"
                        infos = m.find_all(class_="txt")
                        info = ""
                        if len(infos) != 0:
                            count = 0
                            for ch in infos[0].children:
                                count += 1
                                try:
                                    if count == 4:
                                        print("fffffffffffffffffffff")
                                        info = ch.get_text().strip().replace("\n", "").replace(" ", "")
                                except:
                                    info = "no info"
                        else:
                            info = "no info"
                        item["im"] = im
                        item["title"] = title
                        item["info"] = info
                        item["hre"] = hre
                        item["phone"] = phone
                        print(im, "##" + title + "##" + info + "##" + phone + "##", hre)
                        yield item
                    except:
                        print("fuck________________________________")
                if len(n) != 0:
                    print("1 lailai====================================")
                    newn = "http://sz.ganji.com" + n[0]["href"]
                    yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        elif dirname=="婚庆摄影":
            print("crawl---------------", dirname)
            soup = BeautifulSoup(data, "lxml")
            mlist = soup.find_all(class_=re.compile("^list.+img$"))
            n = soup.find_all("a", class_="next")
            for m in mlist:
                try:
                    title = m.find_all(class_="txt")[0].p.get_text().strip().replace("\n", "").replace(" ", "")
                    hre = m.find_all(class_="txt")[0].p.a["href"]

                    if hre.find("http") == -1:
                        hre = " http://sz.ganji.com" + hre
                    ims = m.find_all("img")
                    if len(ims) != 0:
                        im = ims[0]["src"]
                        if im.find("http") == -1:
                            im = "http:" + im
                    else:
                        im = "no img"
                    phone = m.find_all(class_="list-r-area")[0].span.get_text().strip().replace("\n", "").replace(
                        " ", "")
                    if len(phone) == 0:
                        phone = "no phone"
                    infos = m.find_all(class_="txt")
                    info = ""
                    if len(infos) != 0:
                        count = 0
                        for ch in infos[0].children:
                            count += 1
                            try:
                                if count == 4:
                                    info = ch.get_text().strip().replace("\n", "").replace(" ", "")
                            except:
                                info = "no info"
                    else:
                        info = "no info"
                    item["im"] = im
                    item["title"] = title
                    item["info"] = info
                    item["hre"] = hre
                    item["phone"] = phone
                    print(im, "##" + title + "##" + info + "##" + phone + "##", hre)
                    yield item
                except:
                    print("fuck________________________________")
            if len(n) != 0:
                print("1 lailai====================================")
                newn = "http://sz.ganji.com" + n[0]["href"]
                yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        elif dirname=="旅游休闲":
            print("crawl---------------", dirname)
            soup = BeautifulSoup(data, "lxml")
            mlist = soup.find_all(class_=re.compile("^list.+img$"))
            n = soup.find_all("a", class_="next")
            for m in mlist:
                try:
                    title = m.find_all(class_="txt")[0].p.get_text().strip().replace("\n", "").replace(" ", "")
                    hre = m.find_all(class_="txt")[0].p.a["href"]

                    if hre.find("http") == -1:
                        hre = " http://sz.ganji.com" + hre
                    ims = m.find_all("img")
                    if len(ims) != 0:
                        im = ims[0]["src"]
                        if im.find("http") == -1:
                            im = "http:" + im
                    else:
                        im = "no img"
                    phone = m.find_all(class_="list-r-area")[0].span.get_text().strip().replace("\n", "").replace(" ",
                                                                                                                  "")
                    if len(phone) == 0:
                        phone = "no phone"
                    infos = m.find_all(class_="txt")
                    info = ""
                    if len(infos) != 0:
                        count = 0
                        for ch in infos[0].children:
                            count += 1
                            try:
                                if count == 4:
                                    info = ch.get_text().strip().replace("\n", "").replace(" ", "")
                            except:
                                info = "no info"
                    else:
                        info = "no info"
                    item["im"] = im
                    item["title"] = title
                    item["info"] = info
                    item["hre"] = hre
                    item["phone"] = phone
                    print(im, "##" + title + "##" + info + "##" + phone + "##", hre)
                    yield item
                except:
                    print("fuck________________________________")
            if len(n) != 0:
                print("1 lailai====================================")
                newn = "http://sz.ganji.com" + n[0]["href"]
                yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        elif dirname == "本地商务服务":
            print("crawl---------------", dirname)
            soup = BeautifulSoup(data, "lxml")
            mlist = soup.find_all(class_=re.compile("^list.+img$"))
            n = soup.find_all("a", class_="next")
            for m in mlist:
                try:
                    title = m.find_all(class_="txt")[0].p.get_text().strip().replace("\n", "").replace(" ", "")
                    hre = m.find_all(class_="txt")[0].p.a["href"]

                    if hre.find("http") == -1:
                        hre = " http://sz.ganji.com" + hre
                    ims = m.find_all("img")
                    if len(ims) != 0:
                        im = ims[0]["src"]
                        if im.find("http") == -1:
                            im = "http:" + im
                    else:
                        im = "no img"
                    phone = m.find_all(class_="list-r-area")[0].span.get_text().strip().replace("\n", "").replace(" ",
                                                                                                                  "")
                    if len(phone) == 0:
                        phone = "no phone"
                    infos = m.find_all(class_="txt")
                    info = ""
                    if len(infos) != 0:
                        count = 0
                        for ch in infos[0].children:
                            count += 1
                            try:
                                if count == 4:
                                    info = ch.get_text().strip().replace("\n", "").replace(" ", "")
                            except:
                                info = "no info"
                    else:
                        info = "no info"
                    item["im"] = im
                    item["title"] = title
                    item["info"] = info
                    item["hre"] = hre
                    item["phone"] = phone
                    print(im, "##" + title + "##" + info + "##" + phone + "##", hre)
                    yield item
                except:
                    print("fuck________________________________")
            if len(n) != 0:
                print("1 lailai====================================")
                newn = "http://sz.ganji.com" + n[0]["href"]
                yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        elif dirname == "教育培训":
            print("crawl---------------", dirname)
            soup = BeautifulSoup(data, "lxml")
            mlist = soup.find_all(class_=re.compile("^list.+img clearfix$"))
            n = soup.find_all("a", class_="next")
            print(len(mlist))
            for m in mlist:
                try:
                    title = m.find_all("p")[0].get_text().strip().replace("\n", "").replace(" ", "")
                    hre = m.find_all("p")[0].a["href"]
                    if hre.find("http") == -1:
                        hre = " http://sz.ganji.com" + hre
                    ims = m.find_all("img")
                    if len(ims) != 0:
                        im = ims[0]["src"]
                        if im.find("http") == -1:
                            im = "http:" + im
                    else:
                        im = "no img"
                    infos = m.find_all("p")
                    if len(infos) > 1:
                        info = m.find_all("p")[0].get_text().strip().replace("\n", "").replace(" ", "")
                    else:
                        info = "no info"
                    dres = m.find_all(class_=re.compile("^fc.*"))
                    if len(dres) != 0:
                        dress = dres[-1].get_text().strip().replace("\n", "").replace(" ", "")
                    else:
                        dress = "no dress"
                    if len(dress) == 0:
                        dress = "no dress"
                    item["im"] = im
                    item["title"] = title
                    item["info"] = info
                    item["hre"] = hre
                    item["dress"] = dress
                    print(im, "##" + title + "##" + info + "##" + dress + "##", hre)
                    yield item
                except:
                    print("fuck____________________________")
            if len(n) != 0:
                print("1 lailai====================================")
                newn = "http://sz.ganji.com" + n[0]["href"]
                yield scrapy.Request(url=newn, callback=self.main, meta={"meta": item})
        pass