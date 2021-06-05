import sys#시스템 모듈
import os#OS 모듈
from PyQt5 import uic#pyqt를 위한 모듈
from PyQt5.QtWidgets import *
import pymysql #mysql 쿼리문을 python에서 사용하게하는 라이브러리
import matplotlib.pyplot as plt#matplotlib import
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json


connect = pymysql.connect(host='localhost', user='hi', password='asd123', db='new_schema',charset='utf8mb4')
cur = connect.cursor()

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("0603UI.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :    
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setuptableUI()
        self.company.cellClicked.connect(self.companyPricediff)
        self.place.cellClicked.connect(self.placePricediff)
        self.pummok.cellClicked.connect(self.pummokPricediff)
        self.setFixedSize(1280, 720)
        self.setWindowTitle("Pricer")
        self.setupMap()
    
    def setupMap(self):
        os.remove("jijum.json")
       
    def setuptableUI(self):
        cur.execute("SELECT COUNT(DISTINCT 상품명) FROM new_schema.asd")
        result=cur.fetchone()
        
        self.pummok.setRowCount(result[0])
        self.pummok.setColumnCount(2)
        self.setpummokTableWidgetData()
        self.pummok.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.pummok.setSortingEnabled(True)
        self.pummok.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.pummok.setColumnWidth(1, self.width()*1/6)
        
        cur.execute("SELECT COUNT(DISTINCT 제조사) FROM new_schema.asd")
        result=cur.fetchone()
        
        self.company.setRowCount(result[0])
        self.company.setColumnCount(1)
        self.setcompanyTableWidgetData()
        self.company.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.company.setSortingEnabled(True)
        self.company.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        cur.execute("SELECT COUNT(DISTINCT 판매업소) FROM new_schema.asd")
        result=cur.fetchone()
        
        self.place.setRowCount(result[0])
        self.place.setColumnCount(1)
        self.setplaceTableWidgetData()
        self.place.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.place.setSortingEnabled(True)
        self.place.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
    def setpummokTableWidgetData(self):
        i = 0
        
        column_headers = ['상품명', '제조사']
        self.pummok.setHorizontalHeaderLabels(column_headers)
        
        query="SELECT DISTINCT 상품명 FROM new_schema.asd;"
        cur.execute(query)
        connect.commit()
        
        datas = cur.fetchall()
        for data in datas:
            pummokname=data[0] 
            companyname=data[1]
            self.pummok.setItem(i , 0, QTableWidgetItem(pummokname))
            self.pummok.setItem(i , 1, QTableWidgetItem(companyname))
            i += 1
 
    def setcompanyTableWidgetData(self):
        i = 0
        
        column_headers = ['제조사']
        self.company.setHorizontalHeaderLabels(column_headers)
        
        query="SELECT DISTINCT 제조사 FROM new_schema.asd;"
        cur.execute(query)
        connect.commit()
        
        datas = cur.fetchall()
        for data in datas:
            companyname=data[0] 
            self.company.setItem(i , 0, QTableWidgetItem(companyname))
            i += 1
      
    def setplaceTableWidgetData(self):
        i = 0
        
        column_headers = ['판매업소']
        self.place.setHorizontalHeaderLabels(column_headers)
        
        query="SELECT DISTINCT 판매업소 FROM new_schema.asd;"
        cur.execute(query)
        connect.commit()
        
        datas = cur.fetchall()
        for data in datas:
            placename=data[0] 
            self.place.setItem(i , 0, QTableWidgetItem(placename))
            i += 1
     
    def companyPricediff(self):
        pastyear=0
        nowyear=0
        
        for i in range(2020,2022):
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 제조사 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.company.item(self.company.currentRow(),0).text(),i)
           
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]
                count+=1

            if count==0:
                avg=None
            else:
                avg=hap/count
            
            if i==2020:
                pastyear=avg
            else:
                nowyear=avg
         
        if pastyear!=None and nowyear!=None:
            self.companydifflabel.clear()
            self.companydifflabel.setText(str(round((nowyear-pastyear)/pastyear*100,2))+'%')
        else: 
          self.companydifflabel.clear()
          self.companydifflabel.setText("작년/올해 데이터가 없습니다.")  
        
        self.showcompanygraph()            
            
    def pummokPricediff(self):
        pastyear=0
        nowyear=0
        avgprice=0
       
        for i in range(2020,2022):
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 상품명 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.pummok.item(self.pummok.currentRow(),0).text(),i)
            # from 뒤는 본인 mySQL "스케마.테이블"로 사용해주세요
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]
                count+=1

            if count==0:
                avg=None
            else:
                avg=hap/count
            
            if i==2020:
                pastyear=avg
            else:
                nowyear=avg
                if nowyear==None:
                    self.pricelabel.clear()
                    self.pricelabel.setText("올해 데이터가 없습니다.")
                else:
                    self.pricelabel.clear()
                    self.pricelabel.setText(str(round(nowyear))+'원')
         
        if pastyear!=None and nowyear!=None:
            self.pummokdifflabel.clear()
            self.pummokdifflabel.setText(str(round((nowyear-pastyear)/pastyear*100,2))+'%')
        else: 
          self.pummokdifflabel.clear()
          self.pummokdifflabel.setText("작년/올해 데이터가 없습니다.") 
          
        self.showpummokGraph()                           

    def showcompanygraph(self):
        distance=[]
        pastyear=0
        nowyear=0
        
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        
        self.companygraph.addWidget(self.canvas)
        
        for i in range(2014,2022):
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 제조사 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.company.item(self.company.currentRow(),0).text(),i)
            # from 뒤는 본인 mySQL "스케마.테이블"로 사용해주세요
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]
                count+=1

            if count==0:
                avg=None
            else:
                avg=hap/count
            
            if i==2014:
                nowyear=avg
                distance.append(0)
            
            else:
                pastyear=nowyear
                nowyear=avg
                if pastyear==None and nowyear==None:
                    distance.append(0)
                    continue
                
                if pastyear==None or nowyear==None:
                    distance.append(0)
                else:
                    distance.append((nowyear-pastyear)/pastyear*100)
            
        print(distance)

        ax = self.fig.add_subplot(111)
        ax.plot(['2014','2015','2016','2017','2018','2019','2020','2021'],distance,marker='o')
        ax.set_xlabel("year")
        ax.set_ylabel("Growth rate compared to last year")
        ax.legend()
        self.canvas.draw()
        self.companygraph.removeWidget(self.canvas)
        
    def showpummokGraph(self):
        yearprice=[]
        
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig) 
        self.pummokgraph.addWidget(self.canvas)

        for i in range(2014,2022):
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 상품명 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.pummok.item(self.pummok.currentRow(),0).text(),i)
            # from 뒤는 본인 mySQL "스케마.테이블"로 사용해주세요
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]
                count+=1

            if count==0:
                avg=None
            else:
                avg=hap/count
                avg=int(avg)
            
            print(avg)
            yearprice.append(avg)

        ax = self.fig.add_subplot(111)
        ax.plot(['2014','2015','2016','2017','2018','2019','2020','2021'],yearprice,marker='o')
        ax.set_xlabel("year")
        ax.set_ylabel("price")
        ax.legend()
        self.canvas.draw()
        self.pummokgraph.removeWidget(self.canvas)
   
    def placePricediff(self):
        
        query="select distinct 판매업소 from new_schema.asd where 판매업소 like '%s';"%self.place.item(self.place.currentRow(),0).text()
        cur.execute(query)
        connect.commit()

        datas = cur.fetchall()

       
        info=[]
        for data in datas:
            with open("jijum.json", "w", encoding='utf-8') as json_file:
                info.append({"판매업소":data[0]})
                json.dump(info, json_file,ensure_ascii=False)

        self.webEngineView.reload()
        
        pastyear=0
        nowyear=0

        for i in range(2020,2022):
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 판매업소 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.place.item(self.place.currentRow(),0).text(),i)
           
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]
                count+=1

            if count==0:
                avg=None
            else:
                avg=hap/count
            
            if i==2020:
                pastyear=avg
            else:
                nowyear=avg
         
        if pastyear!=None and nowyear!=None:
            self.placedifflabel.clear()
            self.placedifflabel.setText(str(round((nowyear-pastyear)/pastyear*100,2))+'%')
        else: 
          self.placedifflabel.clear()
          self.placedifflabel.setText("작년/올해 데이터가 없습니다.") 
        
        self.showplacegraph()
        
    def showplacegraph(self):
        distance=[]
        pastyear=0
        nowyear=0
        
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.placegraph.addWidget(self.canvas) 
        
        for i in range(2014,2022):
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 판매업소 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.place.item(self.place.currentRow(),0).text(),i)
            # from 뒤는 본인 mySQL "스케마.테이블"로 사용해주세요
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]
                count+=1

            if count==0:
                avg=None
            else:
                avg=hap/count
            
            if i==2014:
                nowyear=avg
                distance.append(0)
            
            else:
                pastyear=nowyear
                nowyear=avg
                if pastyear==None and nowyear==None:
                    distance.append(0)
                    continue
                
                if pastyear==None or nowyear==None:
                    distance.append(0)
                else:
                    distance.append((nowyear-pastyear)/pastyear*100)
            
        print(distance)

        ax = self.fig.add_subplot(111)
        ax.plot(['2014','2015','2016','2017','2018','2019','2020','2021'],distance,marker='o')
        ax.set_xlabel("year")
        ax.set_ylabel("Growth rate compared to last year")
        ax.legend()
        self.canvas.draw()
        self.placegraph.removeWidget(self.canvas)   
       
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
