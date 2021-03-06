from base_ui import WidgetUI
from PyQt5.QtWidgets import QDialog,QTableWidgetItem ,QHeaderView
from PyQt5.QtWidgets import QMessageBox,QVBoxLayout,QCheckBox,QButtonGroup,QPushButton,QLabel,QSpinBox,QComboBox
from PyQt5.QtCore import QAbstractTableModel,Qt,QModelIndex


class ErrorsModel(QAbstractTableModel):
    def __init__(self,parent):
        super(ErrorsModel, self).__init__()
        self.parent = parent
        self.errors = []
        self.header = ["Code", "Level","Info"]
 
    def data(self, index, role):
        if role == Qt.DisplayRole:
            idx = index.row()

            d = self.errors[idx]
                
            if(index.column() == 0):
                return d["code"]
            elif(index.column() == 1):
                return d["level"]
            elif(index.column() == 2):
                return d["info"]
            else:
                return None

    def headerData(self,section,orientation,role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]


    def getHeader(self):
        return self.header

    def rowCount(self, index):
        return len(self.errors)

    def columnCount(self, index):
        return len(self.header)

    def clearErrors(self):
        self.beginResetModel()
        self.errors.clear()
        self.endResetModel()

    def errorCount(self):
        return len(self.errors)
    
    def addError(self,error):
        errcnt = len(self.errors)
        self.beginInsertRows(QModelIndex(),errcnt,errcnt)
        self.errors.append(error)
        self.endInsertRows()

    def setErrors(self,errors):
        self.beginResetModel()
        self.errors = errors
        self.endResetModel()

class ErrorsDialog(QDialog):
    def __init__(self,main=None):
        QDialog.__init__(self, main)
        self.main = main
        self.ui = ErrorsUI(main,self)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.ui)
        self.setLayout(self.layout)
        self.setWindowTitle("Errors")

class ErrorsUI(WidgetUI):
    
    def __init__(self, main=None,parent = None):
        WidgetUI.__init__(self, parent,'errors.ui')
        self.main = main
        self.parent = parent
        main.comms.serialRegisterCallback("Err",self.errorCallback)
        self.pushButton_refresh.clicked.connect(self.readErrors)
        self.pushButton_clearAll.clicked.connect(self.clearErrors)
        self.errors = ErrorsModel(self.tableView)
        self.tableView.setModel(self.errors)
        header = self.tableView.horizontalHeader()
        header.setStretchLastSection(True)


    def clearErrors(self):
        self.main.comms.serialWrite("errorsclr\n")
        self.readErrors()

    def showEvent(self, a0):
        self.tableView.resizeColumnsToContents()
        #self.readErrors()

    def readErrors(self):
        if(self.isEnabled):
            self.main.comms.serialGetAsync("errors",self.errorCallback)

    def errorCallback(self,errorstring):
        self.parent.show()
        errors = []
        for errorline in errorstring.split("\n"):
            e = errorline.split(":")
            if(len(e) < 3):
                continue
            error = {"code":e[0], "level":e[1], "info":e[2]}
            errors.append(error)
        self.errors.setErrors(errors)
        self.tableView.resizeColumnsToContents()
        

            

    