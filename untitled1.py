import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql #따로 설치해주어야한다.

connect = pymysql.connect(host='localhost', user='hi', password='asd123', db='new_schema',charset='utf8mb4')
cur = connect.cursor()


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.addPummok()
        self.pummok.currentIndexChanged.connect(self.pummokPricediff)
        self.setuptableUI()

    def setuptableUI(self):
        cur.execute("SELECT COUNT(*) FROM data.db")
        result=cur.fetchone()
        
        self.pummok_2.setRowCount(645)
        self.pummok_2.setColumnCount(4)
        self.setTableWidgetData()
        self.pummok_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def setTableWidgetData(self):
        i = 0
        
        column_headers = ['상품명', '제조사', '올해평균가격', '전년도대비상승폭']
        self.pummok_2.setHorizontalHeaderLabels(column_headers)
        
        query="SELECT DISTINCT 상품명 FROM data.db;"
        
        cur.execute(query)
        connect.commit()
        
        self.pummok.addItem('')
        datas = cur.fetchall()
        for data in datas:
            pummokname=data[0] 
            self.pummok_2.setItem(i , 0, QTableWidgetItem(pummokname))
            i += 1
 
    def addPummok(self):
        query="SELECT DISTINCT 상품명 FROM new_schema.asd;"

        cur.execute(query)
        connect.commit()
        
        self.pummok.addItem('')
        datas = cur.fetchall()
        for data in datas:
            pummokname=data[0]
            self.pummok.addItem(pummokname)
            
    def pummokPricediff(self):
        pastyear=0
        nowyear=0

        for i in range(2020,2022):
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 상품명 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.pummok.currentText(),i)
            # from 뒤는 본인 mySQL "스케마.테이블"로 사용해주세요
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]
                count+=1

            if count==0:
                avg=-1
            else:
                avg=hap/count
            
            if i==2020:
                pastyear=avg
            else:
                nowyear=avg
         
        if pastyear!=-1 and nowyear!=-1:
            self.difflabel.clear()
            self.difflabel.setText(str((nowyear-pastyear)/pastyear*100))
        else: 
          self.difflabel.clear()
          self.difflabel.setText("x") 
          
        self.showpummokGraph()                           

    def showpummokGraph(self):
        yearprice=[]
        
        for i in range(2014,2022):
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 상품명 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.pummok.currentText(),i)
            # from 뒤는 본인 mySQL "스케마.테이블"로 사용해주세요
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]
                count+=1

            if count==0:
                avg=-1
            else:
                avg=hap/count
            
            print(avg)
            yearprice.append(avg)
        
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
