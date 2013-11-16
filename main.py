__author__ = 'MpX'

# Import PySide classes
import sys
from PySide.QtCore import *
from PySide.QtGui import *

import urllib.request
import lxml.html
import threading
from time import sleep

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.but = QPushButton('Go', self)
        self.link = QLineEdit(self)
        self.delay = QLineEdit(self)
        self.lim = QLineEdit(self)
        self.link.setFixedWidth(350)
        self.but.move(10, 10)
        self.link.move(10, 50)
        self.delay.move(10, 75)
        self.lim.move(10, 100)
        self.link.setPlaceholderText('link (replace page number with {pn})')
        self.delay.setPlaceholderText('delay')
        self.lim.setPlaceholderText('page limit')

        self.but.clicked.connect(self.buttonClick)
        self.show()

    def buttonClick(self):
        sender = self.sender()
        delay = 5 #5sec default
        lim = -1 #no lim
        try:
            delay = int(self.delay.text())
        except ValueError: self.delay.setText("5")
        try:
            lim = int(self.lim.text())
        except ValueError: self.lim.setText("-1 (no lim)")
        t = threading.Thread(target=self.script, args=(self.link.text(), delay, lim, self.link))
        #self.script(self.link.text(), delay, lim, self.link)
        #t.daemon = True
        res = t.start()
        print(str(res))
    def script(self, url, delay, pageLim, info):

        if "m.avito" not in url:
            if "www" in url: url = url.replace("www", "m")
            else: url = url.replace("avito.ru", "m.avito.ru")

        try:
            delay
        except NameError:
            delay = 5 #5sec

        try:
            pageLim
        except NameError:
            pageLim = -1 #no limit

        urlSource = url
        pageNum = 0
        positions = []
        done = False

        while not done:
            url = urlSource.replace("{pn}", str(pageNum))
            try:
                response = urllib.request.urlopen(url)
            except urllib.error.HTTPError as e:
                print(e.code)
                done = True
            #print(e.read())
            pageNum += 1
            if response.getcode() == 200 and done == False:
                doc = lxml.html.document_fromstring(response.read())
                listElements = doc.xpath('//ul[@class="b-catalog-list"]//li')

                for element in listElements:
                    link = element.find_class('img')
                    if len(link) != 0:
                        link = "http://m.avito.ru" + link[0].values()[1]
                        title = element.find_class('title').pop().text_content()
                        metro = element.find_class('metro metro_n')
                        if len(metro) != 0: metro = metro.pop().text_content()
                        else: metro = 'none'
                        price = element.find_class('price')
                        if len(price) != 0: price = price.pop().text_content()
                        else: price = 'n/a'

                        positions.append((title, metro, price, link))

            #done = True #debug
            print(pageNum)
            info.setText('working on page: ' + str(pageNum))
            #info.repaint()
            if response.getcode() != 200 or pageNum == pageLim: done = True
            else: sleep(delay)

        self.writeOut(positions)


    def writeOut(self, positions):
        output = open('list.txt', 'wt')
        for line in positions:
            output.write(line[0]+'\t'+line[1]+'\t'+line[2]+'\t'+line[3]+'\n')
        output.close()

        self.link.setText('Done! See list.txt')


def main():
    # Create a Qt application
    app = QApplication(sys.argv)
    wid = MainWindow()
    wid.resize(370, 130)
    wid.setWindowTitle('AVITO Simple Parser')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

'''
def script(url, delay, pageLim):
    url = url.split('{pn}')
    pageNum = 0
    positions = []
    done = False

    while not done:
        url = url[0] + str(pageNum) + url[1]
        try:
            response = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print(e.code)
            done = True
        #print(e.read())
        pageNum += 1
        if response.getcode() == 200 and done == False:
            doc = lxml.html.document_fromstring(response.read())
            listElements = doc.xpath('//ul[@class="b-catalog-list"]//li')

            for element in listElements:
                link = element.find_class('img')
                if len(link) != 0:
                    link = link[0].values()[1]
                    title = element.find_class('title').pop().text_content()
                    metro = element.find_class('metro metro_n')
                    if len(metro) != 0: metro = metro.pop().text_content()
                    else: metro = 'none'
                    price = element.find_class('price')
                    if len(price) != 0: price = price.pop().text_content()
                    else: price = 'n/a'

                    positions.append((title, metro, price, link))

        done = True #debug
        print(pageNum)
        if response.getcode() != 200 or pageNum == pageLim: done = True
        else: sleep(delay)

    output = open('list.txt', 'wt')
    for line in positions:
        output.write(line[0]+'\t'+line[1]+'\t'+line[2]+'\t'+line[3]+'\n')
    output.close()

    self.link.setPlaceholderText('done')
'''