import sys#시스템 모듈
import os#OS 모듈
from PyQt5 import uic#pyqt를 위한 모듈
from PyQt5.QtWidgets import *
import pymysql #mysql 쿼리문을 python에서 사용하게하는 라이브러리
import matplotlib.pyplot as plt#matplotlib import
from mpl_toolkits.mplot3d import Axes3D#matlotlib 그래프를 qt에 띄우기 위한 라이브러리
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json#json파일 처리를 위한 모듈


connect = pymysql.connect(host='localhost', user='hi', password='asd123', db='new_schema',charset='utf8mb4')#mysql 접속
cur = connect.cursor()#커서로 포인팅

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :    
    def __init__(self) :
        super().__init__()
        self.setupUi(self)#기본ui세팅
        self.setuptableUI()#테이블세팅
        self.company.cellClicked.connect(self.companyPricediff)#회사 테이블 클릭 시 시그널
        self.place.cellClicked.connect(self.placePricediff)#지점 테이블 클릭 시 시그널
        self.pummok.cellClicked.connect(self.pummokPricediff)#품목 테이블 클릭 시 시그널
        self.setFixedSize(1280, 720)#ui사이즈 고정
        self.setWindowTitle("Pricer")#프로그램 이름
        self.setupMap()#지도 초기화
        self.pummokButton.clicked.connect(self.pummokSearch)#품목별 검색 버튼 클릭 시그널
        self.jijumButton.clicked.connect(self.jijumSearch)#지점별 검색 버튼 클릭 시그널
        self.companyButton.clicked.connect(self.companySearch)#회사별 검색 버튼 시그널
    
    def setupMap(self):#지도 초기화
        if os.path.exists("jijum.json"):#jijum.json파일이 존재하면
            os.remove("jijum.json")#삭제
    

    def setuptableUI(self):#ui 세팅
        cur.execute("SELECT COUNT(DISTINCT 상품명) FROM new_schema.asd")#db에서 상품명 읽어오기
        result=cur.fetchone()
        
        self.pummok.setRowCount(result[0])#row번호
        self.pummok.setColumnCount(2)#col번호
        self.setpummokTableWidgetData()#품목 테이블 세팅
        self.pummok.setEditTriggers(QAbstractItemView.NoEditTriggers)#테이블 내 항목 수정 불가
        self.pummok.setSortingEnabled(True)#테이블 항목 정렬 가능
        self.pummok.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)#헤더 크기 조정
        self.pummok.setColumnWidth(1, self.width()*1/6)#컬럼 크기 조정
        
        cur.execute("SELECT COUNT(DISTINCT 제조사) FROM new_schema.asd")#bd에서 회사 읽어오기
        result=cur.fetchone()
        
        self.company.setRowCount(result[0])#row번호
        self.company.setColumnCount(1))#col번호
        self.setcompanyTableWidgetData()#회사 테이블 세팅
        self.company.setEditTriggers(QAbstractItemView.NoEditTriggers)#테이블 내 항목 수정 불가
        self.company.setSortingEnabled(True)#테이블 항목 정렬 가능
        self.company.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)#헤더 크기 조정
        
        cur.execute("SELECT COUNT(DISTINCT 판매업소) FROM new_schema.asd")#db에서 지점 읽어오기
        result=cur.fetchone()
        
        self.place.setRowCount(result[0])#row번호
        self.place.setColumnCount(1)#col번호
        self.setplaceTableWidgetData()#지점 테이블 세팅
        self.place.setEditTriggers(QAbstractItemView.NoEditTriggers)#테이블 내 항목 수정 불가
        self.place.setSortingEnabled(True)#테이블 항목 정렬 가능
        self.place.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)#헤더 크기 조정
        
    def setpummokTableWidgetData(self):#품목테이블 세팅
        i = 0#행 카운트
        
        column_headers = ['상품명', '제조사']#품목 테이블 헤더
        self.pummok.setHorizontalHeaderLabels(column_headers)#헤더 삽입
        
        query="SELECT DISTINCT 상품명, 제조사 FROM new_schema.asd;"#db에서 상품명, 제조사 가져오기
        cur.execute(query)
        connect.commit()
        
        datas = cur.fetchall()
        for data in datas:
            pummokname=data[0] #상품명
            companyname=data[1] #제조사
            self.pummok.setItem(i , 0, QTableWidgetItem(pummokname))#i행 0열에 품목명 삽입
            self.pummok.setItem(i , 1, QTableWidgetItem(companyname))#i행 1열에 제조사 삽입
            i += 1#행 카운트 증가
 
    def setcompanyTableWidgetData(self):#회사 테이블 세팅
        i = 0#행 카운트
        
        column_headers = ['제조사']#회사 테이블 헤더
        self.company.setHorizontalHeaderLabels(column_headers)#헤더 삽입
        
        query="SELECT DISTINCT 제조사 FROM new_schema.asd;"#db에서 제조사 fetch
        cur.execute(query)
        connect.commit()
        
        datas = cur.fetchall()
        for data in datas:
            companyname=data[0] #회사명
            self.company.setItem(i , 0, QTableWidgetItem(companyname))#i행 0열에 회사명 삽입
            i += 1#행 카운트 증가
      
    def setplaceTableWidgetData(self):#지점 테이블 세팅
        i = 0#행 카운트
        
        column_headers = ['판매업소']#지점 테이블 헤더
        self.place.setHorizontalHeaderLabels(column_headers)#헤더 삽입
        
        query="SELECT DISTINCT 판매업소 FROM new_schema.asd;"#db에서 지점 fetch
        cur.execute(query)
        connect.commit()
        
        datas = cur.fetchall()
        for data in datas:
            placename=data[0] #지점명
            self.place.setItem(i , 0, QTableWidgetItem(placename))#i행 0열에 지점명 삽입
            i += 1#행카운트 증가
    
    
    def pummokSearch(self):#품목 검색
        keyword=self.pummokText.text()#검색창 텍스트 가져오기
        for i in range(0, self.pummok.rowCount()):#테이블 탐색
            if keyword==self.pummok.item(i,0).text():#검색어 찾으면
                self.pummok.setCurrentCell(i,0)#현재 셀을 검색어 셀로 설정
                self.pummokPricediff()#클릭시 기능과 동일하게 시행
                
                
    def jijumSearch(self): #지점 검색
        keyword=self.jijumText.text()#검색창 텍스트 가져오기
        for i in range(0, self.place.rowCount()):#테이블 탐색
            if keyword==self.place.item(i,0).text():#검색어 찾으면
                self.place.setCurrentCell(i,0)#현재 셀을 검색어 셀로 설정
                self.placePricediff()#클릭시 기능과 동일하게 시행
                
    def companySearch(self):#회사 검색
        keyword=self.companyText.text()#검색창 텍스트 가져오기
        for i in range(0, self.company.rowCount()):#테이블 탐색
            if keyword==self.company.item(i,0).text():#검색어 찾으면
                self.company.setCurrentCell(i,0)#현재 셀을 검색어 셀로 설정
                self.companyPricediff()#클릭시 기능과 동일하게 시행
                
                
    def companyPricediff(self):#회사 전년대비 가격 변동량 
        pastyear=0#작년평균
        nowyear=0#올해평균
        
        for i in range(2020,2022):#20년 21년
            count=0#데이터 카운터
            hap=0#데이터 합계
            avg=0.0#평균
            query="SELECT 판매가격 FROM new_schema.asd WHERE 제조사 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.company.item(self.company.currentRow(),0).text(),i)
           #선택한 회사, i년의 판매가격 fetch
            
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]#데이터 hap에 더하기
                count+=1#카운트 증가

            if count==0:#데이터가 없었다면
                avg=None#평균 없음
            else:
                avg=hap/count#평균 구하기
            
            if i==2020:#20년도
                pastyear=avg#pastyear
            else:#21년도
                nowyear=avg#nowyear
         
        if pastyear!=None and nowyear!=None:#작년평균이나 올해평균이 둘다 존재하면
            self.companydifflabel.clear()
            self.companydifflabel.setText(str(round((nowyear-pastyear)/pastyear*100,2))+'%')#작년대비 올해 변동량
        else: 
          self.companydifflabel.clear()
          self.companydifflabel.setText("작년/올해 데이터가 없습니다.")  
        
        self.showcompanygraph()#회사 변동량 그래프
            
    def pummokPricediff(self):#품목 평균가, 변동량
        pastyear=0#작년평균
        nowyear=0#올해평균
        avgprice=0#평균가
       
        for i in range(2020,2022):#20년 21년
            count=0#데이터 카운터
            hap=0#데이터 합계
            avg=0.0#평균
            query="SELECT 판매가격 FROM new_schema.asd WHERE 상품명 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.pummok.item(self.pummok.currentRow(),0).text(),i)
            #선택한 품목, i년의 판매가격 fetch
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:
                hap+=data[0]#데이터 hap에 더하기
                count+=1#카운트 증가

            if count==0:#데이터가 없었다면
                avg=None#평균 없음
            else:
                avg=hap/count#평균 구하기
            
            if i==2020:#20년도
                pastyear=avg#pastyear
            else::#21년도
                nowyear=avg#nowyear
                
                if nowyear==None:#올해 데이터가 없으면
                    self.pricelabel.clear()
                    self.pricelabel.setText("올해 데이터가 없습니다.")
                else:
                    self.pricelabel.clear()
                    self.pricelabel.setText(str(round(nowyear))+'원')#평균가 출력
         
        if pastyear!=None and nowyear!=None:#작년평균이나 올해평균이 둘다 존재하면
            self.pummokdifflabel.clear()
            self.pummokdifflabel.setText(str(round((nowyear-pastyear)/pastyear*100,2))+'%')#가격 변동량 출력
        else: 
          self.pummokdifflabel.clear()
          self.pummokdifflabel.setText("작년/올해 데이터가 없습니다.") 
          
        self.showpummokGraph()#품목 가격 그래프                         

    def showcompanygraph(self):#회사 변동량 그래프
        distance=[]#작년대비 변동량 값 리스트
        pastyear=0#작년 평균
        nowyear=0#올해 평균
        
        self.fig = plt.Figure()#그래프 캔버스 초기화
        self.canvas = FigureCanvas(self.fig)
        
        self.companygraph.addWidget(self.canvas)
        
        for i in range(2014,2022):#2014~2021
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 제조사 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.company.item(self.company.currentRow(),0).text(),i)
             #선택한 회사, i년의 판매가격 fetch
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
            
            if i==2014:#14년도이면
                nowyear=avg
                distance.append(0)#변동량 0            
            else:
                pastyear=nowyear#작년값 갱신
                nowyear=avg#올해값은 avg
                if pastyear==None and nowyear==None:#작년값 올해값 둘다 없으면
                    distance.append(0)#변동량 0 추가
                    continue
                
                if pastyear==None or nowyear==None:#작년값이나 올해가 없으면
                    distance.append(0)#0 추가
                else:
                    distance.append((nowyear-pastyear)/pastyear*100)#변동량 계산 후 추가
            
        print(distance)

        ax = self.fig.add_subplot(111)#그래프 plot 생성
        ax.plot(['2014','2015','2016','2017','2018','2019','2020','2021'],distance,marker='o')#행에 연도 삽입
        ax.set_xlabel("year")#x축 텍스트
        ax.set_ylabel("Growth rate compared to last year")#y축 텍스트
        ax.legend()
        self.canvas.draw()#그래프 그리기
        self.companygraph.removeWidget(self.canvas)#다음 선택을 위해 그래프 비워두기
        
    def showpummokGraph(self):#품목 가격 그래프
        yearprice=[]#가격 리스트
        
        self.fig = plt.Figure()#그래프 캔버스 초기화
        self.canvas = FigureCanvas(self.fig) 
        self.pummokgraph.addWidget(self.canvas)

        for i in range(2014,2022):#2014~2021
            count=0
            hap=0
            avg=0.0
            query="SELECT 판매가격 FROM new_schema.asd WHERE 상품명 LIKE '%s' AND 조사일 LIKE '%d%%';"%(self.pummok.item(self.pummok.currentRow(),0).text(),i)
            #선택한 품목, i년의 판매가격 fetch
            cur.execute(query)
            connect.commit()
        
            datas = cur.fetchall()
            for data in datas:#평균가 구하기
                hap+=data[0]
                count+=1

            if count==0:
                avg=None
            else:
                avg=hap/count
                avg=int(avg)
            
            print(avg)
            yearprice.append(avg)

        ax = self.fig.add_subplot(111)#그래프 그리기
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
