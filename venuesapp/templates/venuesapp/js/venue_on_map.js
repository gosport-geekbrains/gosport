ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
            center: [{{venue.lat}}, {{venue.lon}}],
            zoom: 4
        }, {
            searchControlProvider: 'yandex#search'
        }),

    // Создаем геообъект с типом геометрии "Точка".
        myGeoObject = new ymaps.GeoObject({
            // Описание геометрии.
            geometry: {
                type: "Point",
                coordinates: [{{venue.lat}}, {{venue.lon}}]
            },
            // Свойства.
            properties: {
                // Контент метки.
                iconContent: 'Я тащусь',
                hintContent: 'Ну давай уже тащи'
            }
        });

    myMap.geoObjects

        .add(new ymaps.Placemark([{{venue.lat}}, {{venue.lon}}], {
            balloonContent: 'цвет <strong>воды пляжа бонди</strong>'
        }, {
            preset: 'islands#icon',
            iconColor: '#0095b6'
        }));
}