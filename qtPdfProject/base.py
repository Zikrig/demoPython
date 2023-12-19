import sys, os, io

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QVBoxLayout
from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QColor

import aspose.pdf as ap

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Read PDF")
        self.setMinimumHeight(600)
        self.setMinimumWidth(500)
        
        self.layoutMain = QVBoxLayout()
        self.layout = QHBoxLayout()
        
        self.setLayout(self.layoutMain)
        self.layoutMain.addLayout(self.layout)
        
        self.pageNow = 1
        self.fileOpen = False
        self.outputPdfDir = os.path.dirname(os.path.abspath(__file__)) + "\\tmp\\"
        self.picture = self.outputPdfDir + "page_out.png"
        self.paintNow = False

        self.coords = {
            'x0': 0,
            'y0': 0,
            'x1': 0,
            'y1': 0,
        }

        button = QPushButton("Read PDF")
        button.setCheckable(True)
        button.clicked.connect(self.loadDoc)
        self.layout.addWidget(button)

        buttonLeft = QPushButton("<<")
        buttonLeft.setCheckable(True)
        buttonLeft.clicked.connect(self.getLeftPage)
        self.layout.addWidget(buttonLeft)

        buttonRight = QPushButton(">>")
        buttonRight.setCheckable(True)
        buttonRight.clicked.connect(self.getRightPage)
        self.layout.addWidget(buttonRight)

        self.lbl = QLabel(self)
        self.layoutMain.addWidget(self.lbl)

    def resizeEvent(self, event):
        if(self.fileOpen):
            self.makeNewPage()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.paintNow = False
            self.pressPos = event.pos()
            self.coords['x0'] = self.pressPos.x()
            self.coords['y0'] = self.pressPos.y()
            
    def mouseMoveEvent(self, event):
        if (event.pos() in self.rect() and
            self.fileOpen):
                self.pressPos2 = event.pos()
          
                self.coords['x1'] = self.pressPos2.x()
                self.coords['y1'] = self.pressPos2.y()
 
                self.paintNow = True

                self.update()

    def mouseReleaseEvent(self, event):
        if (self.pressPos is not None and 
            event.button() == Qt.MouseButton.LeftButton and 
            event.pos() in self.rect() and
            self.fileOpen):
                self.pressPos2 = event.pos()
                self.coords['x1'] = self.pressPos2.x()
                self.coords['y1'] = self.pressPos2.y()
                self.paintNow = True
                self.update()
                
        self.pressPos = None

    def paintEvent(self, event):
        if(self.fileOpen):
            painter = QPainter(self)
            painter.drawPixmap(10, 40, self.scPixmap.width(), self.scPixmap.height(), self.scPixmap)

        if(self.paintNow):
            painter.setPen(QColor(255, 0, 0))
            
            self.xosn = self.coords['x0']
            self.xlen = self.coords['x1'] - self.coords['x0']

            self.yosn = self.coords['y0']
            self.ylen = self.coords['y1'] - self.coords['y0']
        
            painter.drawRect(QRect(self.xosn, self.yosn, self.xlen, self.ylen))
            self.paintNow = False
            self.setFixedWidth(self.scPixmap.width() + 20)
     

    def getLeftPage(self):
        if(not self.fileOpen):
            return True
        if(self.pageNow == 1):
            return True
        self.pageNow -= 1

        self.makeNewPage()

    def getRightPage(self):
        if(not self.fileOpen):
            return True
        if(self.pageNow == min(4, len(self.document.pages))):
            return True
        self.pageNow += 1

        self.makeNewPage()

    def makeNewPage(self):
        allInDir = os.listdir(self.outputPdfDir)
        for f in allInDir:
            os.remove(self.outputPdfDir+f)

        imageStream = io.FileIO(
            self.picture, 'x'
        )
        self.device.process(self.document.pages[self.pageNow], imageStream)
        imageStream.close()

        pixmap = QPixmap(self.picture)
        self.scPixmap = pixmap.scaledToHeight(self.height()-10)
        self.setFixedWidth(self.scPixmap.width() + 20)
        self.update()

    def loadDoc(self):
        files, _ = QFileDialog.getOpenFileName(None, "Open File", "", "PDF Files (*.pdf)")
        fileName = str(files)
        if(fileName == ''):
            self.fileOpen = False
            return True
        self.fileOpen = True
        
        allInDir = os.listdir(self.outputPdfDir)
        for f in allInDir:
            os.remove(self.outputPdfDir+f)

        self.fileName = fileName
        self.document = ap.Document(self.fileName)
        resolution = ap.devices.Resolution(300)
        self.device = ap.devices.PngDevice(resolution)

        self.makeNewPage()


app = QApplication(sys.argv)


window = MainWindow()
window.show()

app.exec()