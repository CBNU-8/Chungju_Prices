
"""
Created on Thu May 20 15:55:43 2021

@author: admin
"""
# -*- coding: utf-8 -*-
from pandas import DataFrame

#예제 데이터 만들기

ex = {'경도' : [127.061026,127.047883,127.899220,128.980455,127.104071,127.102490,127.088387,126.809957,127.010861,126.836078
                ,127.014217,126.886859,127.031702,126.880898,127.028726,126.897710,126.910288,127.043189,127.071184,127.076812
                ,127.045022,126.982419,126.840285,127.115873,126.885320,127.078464,127.057100,127.020945,129.068324,129.059574
                ,126.927655,127.034302,129.106330,126.980242,126.945099,129.034599,127.054649,127.019556,127.053198,127.031005
                ,127.058560,127.078519,127.056141,129.034605,126.888485,129.070117,127.057746,126.929288,127.054163,129.060972],
     '위도' : [37.493922,37.505675,37.471711,35.159774,37.500249,37.515149,37.549245,37.562013,37.552153,37.538927,37.492388
              ,37.480390,37.588485,37.504067,37.608392,37.503693,37.579029,37.580073,37.552103,37.545461,37.580196,37.562274
              ,37.535419,37.527477,37.526139,37.648247,37.512939,37.517574,35.202902,35.144776,37.499229,35.150069,35.141176
              ,37.479403,37.512569,35.123196,37.546718,37.553668,37.488742,37.493653,37.498462,37.556602,37.544180,35.111532
              ,37.508058,35.085777,37.546103,37.483899,37.489299,35.143421],
     '구분' : ['음식','음식','음식','음식','생활서비스','음식','음식','음식','음식','음식','음식','음식','음식','음식','음식'
             ,'음식','음식','소매','음식','음식','음식','음식','소매','음식','소매','음식','음식','음식','음식','음식','음식'
             ,'음식','음식','음식','음식','소매','음식','음식','의료','음식','음식','음식','소매','음식','음식','음식','음식'
             ,'음식','음식','음식']}

ex=DataFrame(ex)
ex

import folium

#지도의 중심을 지정하기 위해 위도와 경도의 평균 구하기
lat = ex['위도'].mean()
long = ex['경도'].mean()

#지도 띄우기
m = folium.Map([lat,long],zoom_start=9)
m.save('test.html')
m

import webbrowser
 
#message = """<html>
#<head></head>
#<body><p>Hello World!</p></body>
#</html>"""
 
#with open(filepath, 'w') as f:
#    f.write(message)
#    f.close()
 
#webbrowser.get()
#<webbrowser.WindowsDefault object at 0x00000226ED70F3A0>

#chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
#webbrowser.get(chrome_path).open(filepath)



#filepath = "test.html"
#webbrowser.open(filepath)


url = 'http://localhost:8000/kakao_map.html'

webbrowser.open(url)

