import sys
import random
import hexdump
from os import path
from PyQt5 import QtCore, QtWidgets, QtGui
from CorvusHexDumpWidget import CorvusHexDumpWidget
from CorvusPlotsWidget import CorvusPlotsWidget
from CorvusHeatMapWidget import CorvusHeatMapWidget

appStyle="""
QMainWindow{
background-color: darkgrey;
}
"""

here = path.abspath(path.dirname(__file__))


class CorvusMainWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.bytes = []

        self.hexDump = CorvusHexDumpWidget()
        self.plotsWidget = CorvusPlotsWidget()
        self.heatMap = CorvusHeatMapWidget()
        self.setLayout(self.creatGridLayout())

    def creatGridLayout(self):
        horizontalGroupBox = QtWidgets.QGroupBox("Main")
        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.plotsWidget,0,0,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.heatMap,0,1,1,1,QtCore.Qt.AlignCenter)
        layout.addWidget(self.hexDump,0,2,1,1,QtCore.Qt.AlignLeft)

        return layout


    def getFileName(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fileNames = QtCore.QStringListModel()

        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            return fileNames[0]
        else:
            return None



    def openFile(self):
        self.fileName = self.getFileName()

        if self.fileName is not None:
            self.getBytesFromFile()
            self.hexDump.populateHexDumpWidget(self.bytes)
            self.plotsWidget.plot2D.updatePlot(self.bytes)
            self.plotsWidget.create3DPoints(self.bytes)
            self.heatMap.addBytesToHeatMap(self.bytes)
            self.heatMap.update()

    
    def getBytesFromFile(self):
        try:
            f = open(self.fileName, "rb")
            self.hexDump.hexDumpString = ""
        except:
            print("ERROR: Could not find %s" % fileName)
            return

        self.bytes = []

        byte = f.read(1)

        while byte:
            self.bytes.append(byte)
            byte = f.read(1)


class CorvusMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.mainWidget = CorvusMainWidget()

        self.setStyleSheet(appStyle)
        mainMenu = self.menuBar()
        menuBar = mainMenu.addMenu("File")
        menuBar.addAction("Open", self.mainWidget.openFile)
        self.setWindowIcon(QtGui.QIcon(here + '/CorvusIcon.png'))
        self.setCentralWidget(self.mainWidget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusMainWindow()
    window.show()
    sys.exit(app.exec_())
