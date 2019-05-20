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

        objectManager.objects.options.set({

            iconImageSize: [5, 5],
            iconImageOffset: [5, 5]
        });

    myMap.geoObjects.add(objectManager);

        $.ajax({
        url: "{{ venues_json }}"
    }).done(function(data) {
        objectManager.add(data);
        //checkState;
    });


    //фунуция обрабатывает перетаскивание, изменение масштаба. Для определения видимых объектов на карте
    myMap.events.add(['boundschange', 'multitouchend','load'], function(e){
       objectsInBounds();
       //geoQuery и  
       //console.log(myMap.geoObjects)
        //console.log(myMap.getCenter());
        //center = new myMap.pl
        //var storage = ymaps.geoQuery(myMap.geoObjects);
        //console.log(storage)
        //var center = ymaps.geoQuery(myMap.getCenter());
        //let closest = storage.sortByDistance([34, 53]);
        //console.log(closest)
    });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    //objectManager.objects.options.set('preset', 'islands#greenDotIcon');
    
    function objectsInBounds() {
        //if (e.get('newZoom') !== e.get('oldZoom')) {
        //console.log(e.get('newZoom'))
        //выдача границ видимой части карты.
        let bounds = myMap.getBounds();
        let strBounds = JSON.stringify(bounds);
        //console.log(checkState());
        $.ajax({
            type: "POST",
            url: "get_objects_in/",
            data: {
                'bounds': strBounds,
                'filter': JSON.stringify(checkState()),
                //'filter': filters,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function showVenuesIn(serverAnswer) {

                //console.log(serverAnswer);
                //$('.card').slideToggle('slow'); //медленное переключение
                //$('.card').hide('slow'); //убрать элемент с уезжание
                //$('.card').show('slow'); //выплывание элемента

                result = JSON.parse(serverAnswer);
                //console.log(result);

                let resultHTML = "";


                result.forEach(function (item) {

                    let description = item.description ? item.descriptionn : "";

                    let venueHTML = `<div class="col-md-6 card-2">
                        <div class="card">
                        <a href="${item.pk}"><img class="card-img-top"  src="${item.photo}"
                                alt="${item.name}"></a>
                            <div class="card-body">
                                <h5 class="card-title">${item.name}</h5>
                                <ul class="card-rating">
                                    <li>5.0</li>
                                    <li>3 ratings</li>
                                        <li><i class="fa fa-circle" aria-hidden="true"></i></li>
                                    <li>${item.paid}</li>
                                        <li><i class="fa fa-circle" aria-hidden="true"></i></li>
                                    <li>${item.category} </li>
                                    </ul>
                                <p class="card-text">${description}</p>
                                </div>
                                <div class="card-bottom"><span></span>
                                </div> </div> </div>`

                    resultHTML += venueHTML

                });

                $('.card').animate({ opacity: "hide" }, "slow");
                //отрисовка полученного.
                $('#venuesObjects').html(resultHTML);
                $('.card').animate({ opacity: "show" }, "slow");
            }
        });
        //}
    }


    function checkState() {
        //console.clear();
        let result = [];
        let checkAdmStr = [];
        let checkDatasetStr = [];
        let checkOptionsStr= [];

        let checkAdm = [];
        let checkDataset = [];
        let checkOptions = [];

        let admAreaFilter = $("#venuesFilterAdm :checkbox").map(function () {
    
            if ($(this).prop('checked')) {
                checkAdmStr.push('properties.'+this.dataset.ftype + '=="' + this.dataset.value +'"');
                checkAdm.push(this.dataset.value)
            }
        }).get();

        //console.log(check)
        let objectTypeFilter = $("#venuesFilterDataset :checkbox").map(function () {
            if ($(this).prop('checked')) {
                checkDatasetStr.push('properties.' + this.dataset.ftype + '=="' + this.dataset.value + '"');
                checkDataset.push(this.dataset.value)
                   //console.log(this.dataset.ftype)
                   //console.log(this.dataset.value)
            }


        }).get();

        let optionsFilter = $("#venuesFilterOptions :checkbox").map(function () {

            if ($(this).prop('checked')) {
                checkOptionsStr.push('properties.' + this.dataset.ftype + '=="1"');
                console.log(this.dataset.ftype)
                console.log(this.dataset.value)
            }

        }).get();
        
        //strFilter = "'(" + checkAdm.join(" || ") + ") && (" + checkDistrict.join(" || ") + ")'"
       // strFilterAdm = checkAdmStr.join(" || ");
        //strFilterDataset = checkDatasetStr.join(" || ");
        //strFilter = "(" + strFilterAdm + ") && (" + strFilterDataset + ")"
        //objectManager.setFilter(strFilter);


        result.push({'adm_area': checkAdm});
        result.push({'dataset': checkDataset});

        return result;

    }

    function selectAll() {

        
    }

    

    function mapFilter() {

        filterString = checkState();



        let adm = filterString[0]['adm_area'];
        let dataset = filterString[1]['dataset'];

        let admProp = adm.map(function(value) {
            return `properties.adm == "${value}"`
        });

        let datasetProp = dataset.map(function(value) {
            return `properties.type == "${value}"`
        });

        strFilterAdm = admProp.join(" || ");
        strFilterDataset = datasetProp.join("||");

        strFilter = "(" + strFilterAdm + ") && (" + strFilterDataset + ")";

        objectManager.setFilter(strFilter);
        objectsInBounds();
    }



    window.onload = objectsInBounds();



    //adm_area 
    {% for adm_area in adm_areas %}
    $('#admArea{{ adm_area.pk }}').click(mapFilter)
    {% endfor %}

    //datasets
    {% for category in categories %}
    $('#category{{ category.pk }}').click(mapFilter)
    {% endfor %}

    $('#sel_all').click(mapFilter);

    $('#dress1').click(mapFilter);
    $('#eat1').click(mapFilter);
    $('#light1').click(mapFilter);

//
//
//

}
