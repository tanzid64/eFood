let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['bd']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    let geocoder = new google.maps.Geocoder();
    let address = document.getElementById('id_address').value;

    geocoder.geocode({'address': address}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            const latitude = results[0].geometry.location.lat();
            const longtitude = results[0].geometry.location.lng();
            document.getElementById('id_longitude').value = longtitude;
            document.getElementById('id_latitude').value = latitude;
            document.getElementById('id_address').value = address;
            // jquery
            // $('#id_latitude').val(latitude);
            // $('#id_longitude').val(longtitude);
        }});

        // Loop through the address component and assign the other address data..
        const address_comp = place.address_components;

        for (let i = 0; i < address_comp.length; i++) {
            for(let j = 0; j < address_comp[i].types.length; j++) {
                if(address_comp[i].types[j] == "country") {
                    document.getElementById('id_country').value = address_comp[i].long_name;
                }
                // if(address_comp[i].types[j] == "administrative_area_level_1") {
                //     document.getElementById('id_state').value = address_comp[i].long_name;
                // }

                if(address_comp[i].types[j] == "locality") {
                    document.getElementById('id_city').value = address_comp[i].long_name;
                }

                if(address_comp[i].types[j] == "postal_code") {
                    document.getElementById('id_pin_code').value = address_comp[i].long_name;
                } else {
                    document.getElementById('id_pin_code').value = "";
                }
            }
        }
}
