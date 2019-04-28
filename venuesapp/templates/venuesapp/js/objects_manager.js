ymaps.ready(init);

function init () {
    var myMap = new ymaps.Map('map', {
            center: [55.76, 37.64],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        }),
        objectManager = new ymaps.ObjectManager({
            // Чтобы метки начали кластеризоваться, выставляем опцию.
            clusterize: true,
            // ObjectManager принимает те же опции, что и кластеризатор.
            gridSize: 70,
            clusterDisableClickZoom: false,
            clusterIconLayout: "default#pieChart"
        });
    //фунуция обрабатывает перетаскивание, изменение масштаба. Для определения видимых объектов на карте
    myMap.events.add(['boundschange', 'mouseup','multitouchend'], function(e){
        //if (e.get('newZoom') !== e.get('oldZoom')) {
            //console.log(e.get('newZoom'))
            //выдача границ видимой части карты.
            console.log(myMap.getBounds());
        //}
         });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    //objectManager.objects.options.set('preset', 'islands#greenDotIcon');
    
	objectManager.objects.options.set({
	//	iconLayout: 'default#image',
	//	iconImageHref: 'static/images/map_markers/point_blue.gif',
        iconImageSize: [5, 5],
        iconImageOffset: [5, 5] });
    
	//objectManager.clusters.options.set('preset', 'islands#greenClusterIcons');
    myMap.geoObjects.add(objectManager);

    function checkState() {
        //console.clear();
        var checkAdm = [];
        var checkDataset = [];
        var checkOptions = [];
        var ids = $("#venuesFilterAdm :checkbox").map(function () {
    
            if ($(this).prop('checked')) {
                checkAdm.push('properties.'+this.dataset.ftype + '=="' + this.dataset.value +'"');

            }

        }).get();
        //console.log(check)

        var ids1 = $("#venuesFilterDataset :checkbox").map(function () {

            if ($(this).prop('checked')) {
                checkDataset.push('properties.' + this.dataset.ftype + '=="' + this.dataset.value + '"');
                   //console.log(this.dataset.ftype)
                   //console.log(this.dataset.value)
            }


        }).get();

        var ids2 = $("#venuesFilterOptions :checkbox").map(function () {

            if ($(this).prop('checked')) {
                checkOptions.push('properties.' + this.dataset.ftype + '=="1"');
                console.log(this.dataset.ftype)
                console.log(this.dataset.value)
            }


        }).get();

        //strFilter = "'(" + checkAdm.join(" || ") + ") && (" + checkDistrict.join(" || ") + ")'"
        strFilterAdm = checkAdm.join(" || ");
        strFilterDataset = checkDataset.join(" || ");
        strFilter = "(" + strFilterAdm + ") && (" + strFilterDataset + ")"
        //if (length(checkDataset)) > 0 {
        //    strFilterOptions = 0
       // }
       // strFilter = '(properties.adm_area=="2" || properties.adm_area=="3") && (properties.district=="30")'
        objectManager.setFilter(strFilter)
        //console.log(strFilter)

    }

    function selectAll() {

        
    }

    

    function mapFilter() {
        filterString = []
        objectManager.setFilter()
    }
//adm_area 
{% for adm_area in adm_areas %}
$('#admArea{{ adm_area.pk }}').click(checkState)
{% endfor %}

//datasets
{% for dataset in datasets %}
    $('#dataset{{ dataset.pk }}').click(checkState)
{% endfor %}

$('#sel_all').click(selectAll);

$('#dress1').click(checkState);
$('#eat1').click(checkState);
$('#light1').click(checkState);

//
//
//

    $.ajax({
        url: "{{ venues_json }}"
    }).done(function(data) {
        objectManager.add(data);
        //checkState;
    });





window.onload = checkState;

}