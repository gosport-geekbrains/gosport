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
            clusterDisableClickZoom: true
        });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    objectManager.objects.options.set('preset', 'islands#greenDotIcon');
    
	objectManager.objects.options.set({
		iconLayout: 'default#image',
	//	iconImageHref: 'static/images/map_markers/point_blue.gif',
		iconImageSize: [5, 5]});
    
	
	objectManager.clusters.options.set('preset', 'islands#greenClusterIcons');
    myMap.geoObjects.add(objectManager);



    $.ajax({
        url: "/static/json/data.json"
    }).done(function(data) {
        objectManager.add(data);
    });

}