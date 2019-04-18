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
    listBoxItems = [
    {% for dataset in datasets %}
        new ymaps.control.ListBoxItem({
            data: {
                content: '{{ dataset.name }}',
                dataset_id: {{ dataset.dataset_id }}
            },
                state: {
                    selected: true
                }
            
        }),
    {% endfor %}
    ]



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
    function checkState() {
        var checkAdm = [];
        var checkDistrict = [];
        var ids = $("#venuesFilterAdm :checkbox").map(function () {
            
            if ($(this).prop('checked')) {
                checkAdm.push('properties.'+this.dataset.ftype + '=="' + this.dataset.value +'"')
                //console.log(this.dataset.ftype)
                //console.log(this.dataset.value)
            }

            //console.log(this.id)
            //alert(this.dataset.ftype)
            //return check;
            //console.log(check)
        }).get();
        //console.log(check)

        var ids1 = $("#venuesFilterDistrict :checkbox").map(function () {

            if ($(this).prop('checked')) {
                checkDistrict.push('properties.' + this.dataset.ftype + '=="' + this.dataset.value + '"')
                   console.log(this.dataset.ftype)
                   console.log(this.dataset.value)
            }

            //console.log(this.id)
            //alert(this.dataset.ftype)
            //return check;
            //console.log(check)
        }).get();
        //console.log(checkAdm)
        //console.log(checkDistrict)
        //console.log(check.join(" && "))
        //strFilter = "'(" + checkAdm.join(" || ") + ") && (" + checkDistrict.join(" || ") + ")'"
        strFilter = checkAdm.join(" || ")
        objectManager.setFilter(strFilter)
        console.log(strFilter)
        //objectManager.setFilter('(properties.adm_area=="2") && (properties.district=="1")')
        //objectManager.setFilter("(" + checkAdm.join(" || ") + ") && (" + checkDistrict.join(" || ") + ")")

        if ($('#adm1').prop('checked')) {
        //    console.log(event.target.id)
        //    objectManager.setFilter('properties.adm_area == "adm1"')
        //    objectManager.setFilter(function (object) {
                 
         //       return object.properties.adm_area == event.target.id;
        //console.log(check)
        //    });
        } else {
            objectManager.setFilter()
        }
    }

    function selectAll() {

        
    }

    function mapFilter() {
        filterString = []
        objectManager.setFilter()
    }
    
$('#adm1').click(checkState);
$('#adm2').click(checkState);
$('#adm3').click(checkState);
$('#sel_all').click(selectAll);
$('#district1').click(checkState);
$('#district2').click(checkState);
$('#district3').click(checkState);




    $.ajax({
        url: "/static/json/data.json"
    }).done(function(data) {
        objectManager.add(data);
    });

}