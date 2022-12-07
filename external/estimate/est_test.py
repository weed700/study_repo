import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt


form_class = uic.loadUiType("main_windows.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.setWindowTitle("견적양식")
        self.setWindowIcon(QIcon("gluesys_logo.png"))
        self.setFixedSize(1024, 600)

    # UI(window)에 프린트되는 아이템들
    def setUI(self):
        self.setupUi(self)  # window 창
        self.OK.clicked.connect(self.button) # 최종 버튼
        #self.showList()
        self.Model_Check() # 모델 체크 함수
        self.apply.clicked.connect(self.Apply_function)
        
        
    def Apply_function(self):
        print(self.LineEdit_1.text())
        #self.LineEdit_1.setPlaceholderText(self.LineEdit_1.text())
        self.LineEdit_1.setPlaceholderText("sdfads")
        self.LineEdit_1.setDisabled(True)
        self.LineEdit_1.setEnabled(True)
    # 모델 체크 함수
    def Model_Check(self):
        # 체크 됬을 때 보내는 시그널
        self.AS700E.clicked.connect(self.Check_Event)
        self.AS9.clicked.connect(self.Check_Event)
        self.All_Hidden_Button()
        
    # 전체 세부 버튼 숨기기
    def All_Hidden_Button(self):
        # 세부 버튼  
        self.a1.setHidden(True)
        self.a2.setHidden(True)
        self.a3.setHidden(True)

    # AS700E 세부 버튼
    def AS700E_Detail_Button(self):
        self.a1.setHidden(False)
        self.a2.setHidden(False)
        self.a3.setHidden(True)

    def AS9_Detail_Button(self):
        self.a1.setHidden(True)
        self.a2.setHidden(True)
        self.a3.setHidden(False)
    
    def Check_Detail_Event(self):
        if self.a1.isChecked():
            print("A1")

    def Check_Event(self):
        if self.AS700E.isChecked():
            self.AS700E.setChecked(False)
            self.AS700E_Detail_Button()
            print("AS700E checked")
            self.a1.clicked.connect(self.Check_Detail_Event)
        elif self.AS9.isChecked():
            self.AS9_Detail_Button()
            print("as9 checked")


    def button(self):
        # 버튼 눌렀을 때 이벤트 결과 부분
        print("버튼클릭")

    def showList(self):
        number=["One", "Two", "Three", "Four"]

        model=QStandardItemModel()
        for x in number:
            model.appendRow(QStandardItem(x))
        self.listView.setModel(model)


if __name__ == "__main__":
    print("견적양식 프로그램 실행")
    app=QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()

