from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget,QGroupBox
from PyQt5.QtWidgets import QMessageBox,QVBoxLayout,QHBoxLayout,QCheckBox,QButtonGroup,QPushButton,QLabel,QSpinBox,QComboBox,QFormLayout
from PyQt5 import uic
import main
from PyQt5.QtCore import QObjectCleanupHandler
from helper import res_path,classlistToIds

class EncoderOptions(QGroupBox):
    widget = None
    def __init__(self,main,id):
        super().__init__()
        self.main = main
        self.setType(id)
        

    def setType(self,id):
        layout = QVBoxLayout()
 
        found = True
        self.setTitle("Encoder settings")
        if(id == 2): # local encoder
            self.widget = (LocalEncoderConf(self,self.main))
            self.setTitle("Local Encoder")
        elif(id == 1): # tmc
            layout.addWidget(QLabel("Configure in TMC tab"))
            found = False
        else:
            layout.addWidget(QLabel("No settings"))

        
        #layout.setContentsMargins(0,0,0,0)
        if self.widget:
            layout.addWidget(self.widget)
            self.applyBtn = QPushButton("Apply")
            self.applyBtn.clicked.connect(self.widget.apply)
            footer = QHBoxLayout()
            footer.addStretch(5)
            footer.addWidget(self.applyBtn)
            footer.addStretch(5)
            layout.addLayout(footer)
 
        self.setLayout(layout)

class EncoderOption(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
    def apply(self):
        pass

    def hideEvent(self, a0) -> None:
        self.onclose()
        return super().hideEvent(a0)

    def showEvent(self, a0) -> None:
        self.onshown()
        return super().showEvent(a0)

    def onshown(self):
        pass

    def onclose(self):
        pass

class LocalEncoderConf(EncoderOption):
    def __init__(self,parent,main):
        self.main = main
        super().__init__(parent)
        self.initUI()
        

    def initUI(self):
        layout = QFormLayout()

        self.spinBox_cpr = QSpinBox()
        self.spinBox_cpr.setRange(0,0xffff)
        layout.addWidget(QLabel("CPR = 4x PPR"))
        layout.addRow(QLabel("CPR"),self.spinBox_cpr)
        self.setLayout(layout)

    def onshown(self):
        self.main.comms.serialGetAsync("cpr",self.spinBox_cpr.setValue,int) 

    def apply(self):
        val = self.spinBox_cpr.value()
        self.main.comms.serialWrite("cpr="+str(val)+"\n")
