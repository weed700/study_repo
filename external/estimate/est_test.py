import sys
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import QDate, Qt


form_class = uic.loadUiType("main_windows.ui")[0]

class MyWindow(QMainWindow, form_class):
    model_name = ''
    detail_model_name = ''

    def __init__(self):
        super().__init__()
        self.setUI()
        self.setWindowTitle("견적양식")
        self.setWindowIcon(QIcon("gluesys_logo.png"))
        #self.setFixedSize(1024, 600)

    # UI(window)에 프린트되는 아이템들
    def setUI(self):
        self.setupUi(self)  # window 창 
        self.Model_Check() # 모델 체크 함수

        #self.Combobox_list()
        # 오늘 날짜 입력
        now = QDate.currentDate()
        self.date.setText(now.toString('yyyy년 MM월 dd일'))

        self.OK.clicked.connect(self.button) # 최종 버튼

    # 모델 DB 변수 저장
    def Excel_DB(self):
        db = pd.read_excel('AS500+PD 견적 양식.xlsm', engine='openpyxl',index_col=[1, 2, 3, 5, 6])
        model_name = []
        for split in db.index:
            model_name.append(split[0])

        # 같은 모델 찾아서 딕셔너리 만들기
        dic={}
        for t in set(model_name):
            l=[]
            for a in db.index:
                if t == a[0]:
                    l.append([a[1],a[2],a[3],a[4]])
            dic[t]=l
        del dic['모델']
        return dic

    # 세부 모델 DB 변수 저장
    def Excel_DB_Detail(self):
        db = pd.read_excel('AS500+PD 견적 양식.xlsm', engine='openpyxl',index_col=[2, 3, 5, 6])
        model_name = []
        for split in db.index:
            model_name.append(split[0])

        # 같은 모델 찾아서 딕셔너리 만들기
        dic={}
        for t in set(model_name):
            l=[]
            if 'GW Single' == t or 'GW Cluster' == t:
                for a in db.index:
                    l.append([a[1],a[2],a[3]])
                dic[t]=l
        return dic

    # 콤보박스 클리어 함수
    def Combobox_clear(self):
        self.model_box.clear()
        self.memory_box.clear()
        self.disk_box_1.clear()
        self.disk_box_2.clear()
        self.nic_box_1.clear()
        self.nic_box_2.clear()
        self.hba_box_1.clear()
        self.hba_box_2.clear()
        self.w_box_1.clear()
        self.w_box_2.clear()
        self.op_box.clear()
        self.cpu_box.clear()

    # 콤보박스 리스트 설정
    def Combobox_list(self,db_key):
        for temp in self.est_db.keys():
            for i in range(0,len(self.est_db[temp])):
                # 모델
                if db_key == temp:
                    self.model_box.addItem(self.est_db[db_key][i][2])
                elif '메모리' == temp:
                    self.memory_box.addItem(self.est_db[temp][i][2])
                elif '디스크' == temp:
                    self.disk_box_1.addItem(self.est_db[temp][i][2])
                    self.disk_box_2.addItem(self.est_db[temp][i][2])
                elif 'NW' == temp:
                    if 'NIC' == self.est_db[temp][i][0]:
                        self.nic_box_1.addItem(self.est_db[temp][i][2])
                        self.nic_box_2.addItem(self.est_db[temp][i][2])
                    if 'HBA' == self.est_db[temp][i][0] or 'IB' == self.est_db[temp][i][0]:
                        self.hba_box_1.addItem(self.est_db[temp][i][2])
                        self.hba_box_2.addItem(self.est_db[temp][i][2])
                elif '워런티' == temp:
                    self.w_box_1.addItem(self.est_db[temp][i][2])
                    # 나눠야하나?
                    self.w_box_2.addItem(self.est_db[temp][i][2])
                    if '옵션SW' == self.est_db[temp][i][0]:
                        self.op_box.addItem(self.est_db[temp][i][2])
                elif 'CPU Upgrade' == self.est_db[temp][i][0]:
                    self.cpu_box.addItem(self.est_db[temp][i][2])

        self.model_box.currentTextChanged.connect(lambda: self.combobox_event(db_key))
        self.memory_box.currentTextChanged.connect(lambda: self.combobox_event(db_key))

    def combobox_event(self,db_key):
        cb = self.sender()
        for key in self.est_db.keys(): 
            for i in range(0,len(self.est_db[key])):
                if db_key == key:
                    if cb.currentText() == self.est_db[key][i][2]:
                        self.mod_1.setText(format(self.est_db[key][i][3],',d'))
                elif '메모리' == key:
                    if cb.currentText() == self.est_db[key][i][2]:
                        self.mem_1.setText(format(self.est_db[key][i][3],',d'))
        
    # 모델 체크 이벤트 시그널 함수
    def Model_Check(self):
        self.est_db=self.Excel_DB() # excel DB 딕셔너리로 변경하여 저장
        # 모델 딕셔너리(디스크, 메모리 등 제거)
        self.model_db = self.est_db.copy()
        del self.model_db['메모리']
        del self.model_db['디스크']
        del self.model_db['워런티']
        del self.model_db['NW']

        self.detail_model_db = self.Excel_DB_Detail() # excel DB detail 모델 부분 딕셔너리로 변경하여 저장
        
        # 라디오 버튼 생성
        x=10; y=20
        
        for b_name in sorted(self.model_db.keys()): 
            rad=QRadioButton(b_name,self.groupBox)
            rad.move(x,y)
            rad.name=b_name
            rad.clicked.connect(self.Check_Event) # 체크 됬을 때 보내는 시그널
            y+=50

        # 세부 모델 라디오 버튼 생성
        d_x=10; d_y=20
        for d_name in sorted(self.detail_model_db.keys()): 
            rad2=QRadioButton(d_name,self.groupBox_2)
            rad2.move(d_x,d_y)
            rad2.name=d_name
            rad2.clicked.connect(self.Check_Event_Detail) # 체크 됬을 때 보내는 시그널
            d_y+=30

    def Check_Event(self):
        radi=self.sender()
        if radi.isChecked():
            self.Combobox_clear() # 콤보박스 클리어 함수
            self.Combobox_list(radi.name) # 콤보박스 리스트 설정

    def Check_Event_Detail(self):
        radi=self.sender()
        if radi.isChecked():
            print(radi.name)
       

    def button(self):
        # 버튼 눌렀을 때 이벤트 결과 부분
        print(self.model_name,self.detail_model_name)
        print("버튼클릭")


if __name__ == "__main__":
    print("견적양식 프로그램 실행")
    app=QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()

