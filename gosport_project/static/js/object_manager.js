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
            clusterDisableClickZoom: true,
            clusterIconLayout: "default#pieChart"
        });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    objectManager.objects.options.set('preset', 'islands#greenDotIcon');
    
	objectManager.objects.options.set({
		iconLayout: 'default#image',
	//	iconImageHref: 'static/images/map_markers/point_blue.gif',
        iconImageSize: [5, 5],
        iconImageOffset: [5, 5] });
    
	
	objectManager.clusters.options.set('preset', 'islands#greenClusterIcons');
    myMap.geoObjects.add(objectManager);

    listBoxItems = [
        new ymaps.control.ListBoxItem({
            data: {
                content: '893 tzt',
                dataset_id: 893
            },
                state: {
                    selected: true
                }
            
        }),
        new ymaps.control.ListBoxItem({
            data: {
                content: '912 text',
                dataset_id: 912
            },
            state: {
                selected: true
            }
        })
    ],



    // Создадим 5 пунктов выпадающего списка.
//    var listBoxItems = ['893', '1251', '898', '886', '885', '917','912','1388','1387']
 //       .map(function (title) {
//            return new ymaps.control.ListBoxItem({
//                data: {
//                    content: title
//                },
//                state: {
//                    selected: true
 //               }
 //           })
 //       }),
        // Теперь создадим список, содержащий 5 пунктов.
        listBoxControl = new ymaps.control.ListBox({
            data: {
                content: 'Фильтр',
                title: 'Фильтр'
            },
            items: listBoxItems,
            state: {
                // Признак, развернут ли список.
                expanded: false,
                filters: listBoxItems.reduce(function (filters, filter) {
                    filters[filter.data.get('dataset_id')] = filter.isSelected();  //content
                    return filters;
                }, {})
            }
        });
    myMap.controls.add(listBoxControl);

    // Добавим отслеживание изменения признака, выбран ли пункт списка.
    listBoxControl.events.add(['select', 'deselect'], function(e) {
        var listBoxItem = e.get('target');
        var filters = ymaps.util.extend({}, listBoxControl.state.get('filters'));
        filters[listBoxItem.data.get('dataset_id')] = listBoxItem.isSelected(); //content
        listBoxControl.state.set('filters', filters);
    });

    var filterMonitor = new ymaps.Monitor(listBoxControl.state);
    filterMonitor.add('filters', function(filters) {
        // Применим фильтр.
        objectManager.setFilter(getFilterFunction(filters));
    });

    function getFilterFunction(categories){
        return function(obj){
            var content = obj.properties.dataset_id;
            return categories[content]   //
        }
    }


    $.ajax({
        url: "/static/json/data.json"
    }).done(function(data) {
        objectManager.add(data);
    });

}