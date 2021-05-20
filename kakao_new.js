// 마커를 담을 배열입니다
var markers = [];

var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };  

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption); 
// 지도에 확대 축소 컨트롤을 생성한다
var zoomControl = new kakao.maps.ZoomControl();
// 지도의 우측에 확대 축소 컨트롤을 추가한다
map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);
// 지도 타입 변경 컨트롤을 생성한다
var mapTypeControl = new kakao.maps.MapTypeControl();
// 지도의 상단 우측에 지도 타입 변경 컨트롤을 추가한다
map.addControl(mapTypeControl, kakao.maps.ControlPosition.TOPRIGHT);	

// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places();  

// 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
var infowindow = new kakao.maps.InfoWindow({zIndex:1});



// 키워드로 장소를 검색합니다
searchPlaces();

// 키워드 검색을 요청하는 함수입니다
function searchPlaces() {

    var keyword = document.getElementById('keyword').value;

    if (!keyword.replace(/^\s+|\s+$/g, '')) {
        alert('키워드를 입력해주세요!');
        return false;
    }

    // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
    ps.keywordSearch( keyword, placesSearchCB); 
}

// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {

        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);

        // 페이지 번호를 표출합니다
        // displayPagination(pagination);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === kakao.maps.services.Status.ERROR) {

        alert('검색 결과 중 오류가 발생했습니다.');
        return;

    }
}

// 검색 결과 목록과 마커를 표출하는 함수입니다
function displayPlaces(places) {

    var listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';
    
    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();
    
    var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
    var imageSize = new kakao.maps.Size(30, 42); 
    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

    for ( var i=0; i<places.length; i++ ) {

        // 마커를 생성하고 지도에 표시합니다
        var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            //marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

        // 마커가 표시될 위치입니다 
        var markerPosition  = new kakao.maps.LatLng(places[i].y, places[i].x); 

        // 마커를 생성합니다
        var marker = new kakao.maps.Marker({
            position: markerPosition,
            image : markerImage // 마커 이미지 
        });

        // 마커가 지도 위에 표시되도록 설정합니다
        marker.setMap(map);

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);

        // 마커와 검색결과 항목에 mouseover 했을때
        // 해당 장소에 인포윈도우에 장소명을 표시합니다
        // mouseout 했을 때는 인포윈도우를 닫습니다
        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'mouseover', function() {
                var htmltxt = itemEl.innerHTML;
                displayInfowindow(marker, title, htmltxt);
            });

            kakao.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });

            itemEl.onmouseover =  function () {
                var htmltxt = itemEl.innerHTML;
                displayInfowindow(marker, title, htmltxt);
            };

            itemEl.onmouseout =  function () {
                infowindow.close();
            };
        })(marker, places[i].place_name);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {

    var el = document.createElement('li'),
    itemStr = '<div class="info">' +
                '   <h5 style="font-size: 19px;">'+ "지점명 : " + places.place_name + '</h5>';

    if (places.road_address_name) {
        itemStr += '    <span style="font-size: 19px;" >' + "주소 : " + places.road_address_name + '</span><br>';
    } else {
        itemStr += '    <span >' + "주소 : " + places.address_name  + '</span><br>'; 
    }
                 
      itemStr += '  <span class="tel" style="font-size: 19px;" >' + "전화번호 : " + places.phone  + '</span><br>' +
                '</div>';           

    el.innerHTML = itemStr;
    el.className = 'item';

    return el;
}


// json 형식의 파일에서 값들을 불러오는 함수입니다.
var xhttp;
function createHttpRequest(){
  xhttp = new XMLHttpRequest();
}

function mySend(){
  createHttpRequest();
  xhttp.onreadystatechange = callFunction;
  xhttp.open("GET", "temp.json", true);
  xhttp.send(null);
}

function callFunction(){
  if(xhttp.readyState == 4) {
    if(xhttp.status == 200){
        var responseData = xhttp.responseText;
        var jsonObject = eval('(' + responseData + ')');

        var goods = jsonObject.상품명;
            var date = jsonObject.조사일;
            var price = jsonObject.판매가격;
            var place = jsonObject.판매업소;
            document.getElementById("goods").innerHTML = goods;
            document.getElementById("date").innerHTML = date;
            document.getElementById("price").innerHTML = price;
            document.getElementById('keyword').value = place;
    }
  }
}

// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title, htmltxt) {

    mySend();
    var content = htmltxt +'<div style="padding:0px";></div>'
    +'<table  border="1" bordercolor="blue" width ="300" height="80" align = "center" >'
	+'<th style="font-size: 15px;" align = "center" bgcolor="skybule" > 상품명 </th>'
	+'<th style="font-size: 15px;" align = "center" bgcolor="skybule" > 조사 날짜 </th>'
    +'<th style="font-size: 15px;" align = "center" bgcolor="skybule" > 가격 </th>'
	+'<tr>'
	+'<td style="font-size: 15px;" id = "goods" ></td>'
	+'<td style="font-size: 15px;" id = "date"></td>'
    +'<td style="font-size: 15px;" id = "price"></td>'
	+'</tr>'
    +'</table>'
    
    infowindow.setContent(content);
    infowindow.open(map, marker);
}


 // 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}


// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}