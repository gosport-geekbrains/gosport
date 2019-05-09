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
    myMap.events.add(['boundschange', 'multitouchend','load'], function(e){
        //if (e.get('newZoom') !== e.get('oldZoom')) {
            //console.log(e.get('newZoom'))
            //выдача границ видимой части карты.
        bounds = myMap.getBounds();
        strBounds = JSON.stringify(bounds);
    console.log(checkState());
        $.ajax({
            type: "POST",
            url: "get_objects_in/",
            data: {
                'bounds': strBounds,
                'filters': checkState(),
                //'filter': filters,
                csrfmiddlewaretoken: '{{ csrf_token }}'},
            success: function (serverAnswer) {
 
                //console.log(serverAnswer);
                //$('.card').slideToggle('slow'); //медленное переключение
                //$('.card').hide('slow'); //убрать элемент с уезжание
                //$('.card').show('slow'); //выплывание элемента

                result = JSON.parse(serverAnswer);
                //console.log(result);

                let resultHTML = "";

                
                    result.forEach(function(item) {
                    
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
                    $('.card').animate({ opacity: "show" }, "slow" );
            }
        });
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
        let checkAdm = [];
        let checkAdmJSON = [];
        let checkDataset = [];
        let checkDatasetJSON = [];
        let checkOptions = [];
        let CheckOptionsJSON = [];
        let result = [];
        let ids = $("#venuesFilterAdm :checkbox").map(function () {
    
            if ($(this).prop('checked')) {
                checkAdm.push('properties.'+this.dataset.ftype + '=="' + this.dataset.value +'"');
                checkAdmJSON.push(this.dataset.value);

            }

        }).get();


        var ids1 = $("#venuesFilterDataset :checkbox").map(function () {

            if ($(this).prop('checked')) {
                checkDataset.push('properties.' + this.dataset.ftype + '=="' + this.dataset.value + '"');
                checkDatasetJSON.push(this.dataset.value)
                   //console.log(this.dataset.ftype)
                   //console.log(this.dataset.value)
            }


        }).get();

        var ids2 = $("#venuesFilterOptions :checkbox").map(function () {

            if ($(this).prop('checked')) {
                checkOptions.push('properties.' + this.dataset.ftype + '=="1"');
                checkOptionsJSON.push(this.dataset.ftype);
                //console.log(this.dataset.ftype)
                //console.log(this.dataset.value)
            }


        }).get();

        strFilterAdm = checkAdm.join(" || ");
        strFilterDataset = checkDataset.join(" || ");
        strFilter = "(" + strFilterAdm + ") && (" + strFilterDataset + ")"

        objectManager.setFilter(strFilter);


        result.push({'checkAdm': checkAdmJSON});
        result.push({'checkDataset': checkDatasetJSON});
        //result = result.push({'checkOptions':checkOptionsJSON});

        return JSON.stringify(result);

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