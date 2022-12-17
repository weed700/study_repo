import sys
import pandas as pd
import math

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import QDate, Qt

# form_class2 = uic.loadUi("s_window.ui")[0]

# class Est_Manager(QMainWindow, form_class2):

#     def __init__(self):
#         super().__init__()
#         self.setUI()
#         self.setWindowTitle("견적 담당자")
#         self.setWindowIcon(QIcon("gluesys_logo.png"))

form_class = uic.loadUiType("main_windows.ui")[0]

class MyWindow(QMainWindow, form_class):
    model_name = ''
    detail_model_name = ''
    disc=0
    est_manager_list ={'이사 박 근 식':['010-5669-3172','gspark@gluesys.com','5371'], 
                       '이사 허 남 중':['010-3741-0869','njheo@gluesys.com','8158'],
                       '이사 김 재 호':['010-7520-9425','justin@gluesys.com','5302'],
                       '대리 우 동 현':['010-5769-7610','dhwoo@gluesys.com','5301'],
                       '대리 김 정':['010-3153-3327','jkim@gluesys.com','5374']}
    m_name=''
    m_code=''
    m_disc=''
    m_count=''
    est_code_list = ['(N)', '(E)', '(P)', '(G)', '(A)', '(M)']

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
        self.Manager()
        self.Code()

        # 오늘 날짜 입력
        self.now = QDate.currentDate()
        self.date.setText(self.now.toString('yyyy년 MM월 dd일'))


        self.count_init.clicked.connect(self.Count_Init) # 수량 초기화 버튼
        
        self.OK.clicked.connect(self.button) # 최종 버튼

    def Count_Init(self):
        #print("수량 초기화")
        for key in self.db_val.keys():
            self.money[key][1]=1
            self.db_val[key][1][0].setText('')
        self.Money_func()

    def Manager_func(self):
        a = self.sender()
        #print(a.currentText())
        self.m_name=a.currentText()
        self.Num_make()

    def Manager(self):
        for m in self.est_manager_list.keys():
            self.est_manager.addItem(m)
        self.est_manager.currentTextChanged.connect(self.Manager_func)

    def Code_func(self):
        a= self.sender()
        self.m_code=a.currentText()
        self.Num_make()

    def Code(self):
        for m in self.est_code_list:
            self.est_code.addItem(m)
        self.est_code.currentTextChanged.connect(self.Code_func)

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
        #for t in set(model_name):
        l=[]
        l2=[]

        for a in db.index:
            n=''
            if 'GW Single' == a[0]:
                n = a[0]
                l.append([a[1],a[2],a[3]])
            elif 'GW Cluster' == a[0]:
                n = a[0]
                l2.append([a[1],a[2],a[3]])

            if 'GW Single' == n:
                dic[n]=l
            elif 'GW Cluster' == n:
                dic[n]=l2
            
        return dic

    def Count_func(self):
        c = self.sender()
        self.m_count=c.text()
        self.Num_make()

    def Ob_db(self,db_key):
        self.db_val = {}
        self.money = {}
        
        label_list=['model_','memory_','disk1_','disk2_','nic1_','nic2_','hba1_','hba2_','w1_','w2_','cpu_','op_']
        for l in label_list:
            box= l+'box'
            a=[]

            a.append(self.findChildren(QComboBox,box))
            
            for i in range(0,4):
                if 0 == i:
                    a.append(self.findChildren(QLineEdit,l+str(i)))
                else:
                    t = l+str(i)
                    a.append(self.findChildren(QLabel, t))

            self.db_val[box] = a
            self.db_val[box][0][0].currentTextChanged.connect(lambda: self.combobox_event(db_key))
            self.db_val[box][1][0].textChanged.connect(self.lineedit_func)
        
        self.disc_box.currentTextChanged.connect(self.Disc_func)
        self.est_count.textChanged.connect(self.Count_func)
        # 초기화
        for key in self.db_val.keys():
            self.money[key]=[0,1]


    # 콤보박스 클리어 함수
    def Combobox_clear(self):
        for box in self.db_val.keys():
            self.db_val[box][0][0].clear()
    
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
                    self.disk1_box.addItem(self.est_db[temp][i][2])
                    self.disk2_box.addItem(self.est_db[temp][i][2])
                elif 'NW' == temp:
                    if 'NIC' == self.est_db[temp][i][0]:
                        self.nic1_box.addItem(self.est_db[temp][i][2])
                        self.nic2_box.addItem(self.est_db[temp][i][2])
                    if 'HBA' == self.est_db[temp][i][0] or 'IB' == self.est_db[temp][i][0]:
                        self.hba1_box.addItem(self.est_db[temp][i][2])
                        self.hba2_box.addItem(self.est_db[temp][i][2])
                elif '워런티' == temp:
                    self.w1_box.addItem(self.est_db[temp][i][2])
                    # 나눠야하나?
                    self.w2_box.addItem(self.est_db[temp][i][2])
                    if '옵션SW' == self.est_db[temp][i][0]:
                        self.op_box.addItem(self.est_db[temp][i][2])
    
        # 할인율 0~100까지 리스트 만들기
        for i in range(0,101):
            d = str(i)+'%'
            self.disc_box.addItem(d)

    def Money_func(self):
        sum_1=0
        sum_2=0

        for key in self.money.keys():
            a=int(self.money[key][0]*self.money[key][1])
            b=int(self.money[key][0]*self.money[key][1]*self.disc)
            sum_1+=a
            sum_2+=b
            for temp in self.db_val.keys():
                if key == temp:
                    self.db_val[key][2][0].setText(format(int(a),',d'))
                    self.db_val[key][3][0].setText(format(int(b),',d'))

        self.money_sum_1.setText(format(sum_1,',d'))
        self.money_sum_2.setText(format(sum_2,',d'))
        temp = int(sum_2/10000)*10000
        self.tt.setText(format(temp,',d'))  
    def Num_make(self):
        # 견적 번호 만들기
        e_num=''
        self.m_disc=self.disc_box.currentText().split('%')
        if self.m_name and self.m_code and self.m_disc:
            e_num='GLS-'+self.now.toString('yyyyMMdd')+'0'+self.m_disc[0]+self.est_count.text()+'-'+self.est_manager_list[self.m_name][2]+self.m_code
        
        self.est_num.setText(e_num)

    def Disc_func(self):
        d=self.sender()
        val=d.currentText().split('%')
        self.disc=(100-int(val[0]))/100
        self.Money_func()
        self.Num_make()

    def Combobox_detail_list(self,db_key):
        for i in range(0,len(self.detail_model_db[db_key])):
            if 'GW Single' == db_key:
                self.model_box.addItem(self.detail_model_db[db_key][i][1])
            elif 'GW Cluster' == db_key:
                self.model_box.addItem(self.detail_model_db[db_key][i][1])
            # elif 'CPU Upgrade' == db_key:
            #     self.cpu_box.addItem(self.detail_model_db[db_key][i][1])

        #self.cpu_box.currentTextChanged.connect(lambda: self.combobox_event(db_key))
        
    # 수량 입력 창
    def lineedit_func(self):
        for key in self.db_val.keys():
            if '' == self.db_val[key][1][0].text():
                a=1
            else:
                a=self.db_val[key][1][0].text()
            self.money[key][1] = int(a)
            
        self.Money_func()


    # 콤보박스 시그널 시 발생하는 함수(slot)
    def combobox_event(self,db_key):
        cb = self.sender()
        ob_name= cb.objectName()

        for key in self.est_db.keys(): 
            for i in range(0,len(self.est_db[key])):
                if db_key == key:
                    if cb.currentText() == self.est_db[key][i][2]:
                        v=self.est_db[key][i][3]
                        self.money['model_box'][0] = v
                        self.model_1.setText(format(v,',d'))
                        self.model_3.setText(self.est_db[key][i][1])          
                elif '메모리' == key:
                    if cb.currentText() == self.est_db[key][i][2]:
                        v=self.est_db[key][i][3]
                        self.money['memory_box'][0] = v
                        self.memory_1.setText(format(v,',d'))
                        self.memory_3.setText(self.est_db[key][i][1]) 
                elif '디스크' == key:
                    if cb.currentText() == self.est_db[key][i][2]:
                        v=self.est_db[key][i][3]
                        self.money[ob_name][0] = v
                        if ob_name == 'disk1_box':
                            self.disk1_1.setText(format(v,',d'))
                            self.disk1_3.setText(self.est_db[key][i][1])
                        elif ob_name == 'disk2_box':
                            self.disk2_1.setText(format(v,',d'))
                            self.disk2_3.setText(self.est_db[key][i][1]) 
                elif 'NW' == key:
                    if cb.currentText() == self.est_db[key][i][2]:
                        v=self.est_db[key][i][3]
                        self.money[ob_name][0] = v
                        if 'NIC' == self.est_db[key][i][0]:   
                            if ob_name == 'nic1_box':          
                                self.nic1_1.setText(format(v,',d'))
                                self.nic1_3.setText(self.est_db[key][i][1])
                            elif ob_name == 'nic2_box':
                                self.nic2_1.setText(format(v,',d'))
                                self.nic2_3.setText(self.est_db[key][i][1])
                        if 'HBA' == self.est_db[key][i][0] or 'IB' == self.est_db[key][i][0]:
                            if ob_name == 'hba1_box':
                                self.hba1_1.setText(format(v,',d'))
                                self.hba1_3.setText(self.est_db[key][i][1])
                            elif ob_name == 'hba2_box':
                                self.hba2_1.setText(format(v,',d'))
                                self.hba2_3.setText(self.est_db[key][i][1])
                elif '워런티' == key:
                    if cb.currentText() == self.est_db[key][i][2]:
                        v=self.est_db[key][i][3]
                        self.money[ob_name][0] = v
                        if ob_name == 'w1_box':
                            self.w1_1.setText(format(v,',d'))
                            self.w1_3.setText(self.est_db[key][i][1])
                        elif ob_name == 'w2_box':
                            self.w2_1.setText(format(v,',d'))
                            self.w2_3.setText(self.est_db[key][i][1])
                        if '옵션SW' == self.est_db[key][i][0]:
                            if ob_name == 'op_box':
                                self.op_1.setText(format(v,',d'))
                                self.op_3.setText(self.est_db[key][i][1])
                elif 'CPU Upgrade' == key:
                    if cb.currentText() == self.est_db[key][i][2]:
                        self.money[ob_name][0] = v
                        v=self.est_db[key][i][3]
                        self.cpu_1.setText(format(v,',d'))
                        self.cpu_3.setText(self.est_db[key][i][1])
        self.Money_func()     

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
        print(self.detail_model_db.keys())
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
            self.Ob_db(radi.name)
            self.Combobox_clear() # 콤보박스 전부 클리어 함수
            self.Combobox_list(radi.name) # 콤보박스 리스트 설정

    def Check_Event_Detail(self):
        radi=self.sender()
        if radi.isChecked():
            self.model_box.clear() # 콤보박스 모델 부분 클리어 함수
            self.Combobox_detail_list(radi.name) # 콤보박스 리스트 설정
       

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

