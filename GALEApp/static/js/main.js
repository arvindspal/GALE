$(document).ready(function(){
    "use strict";
    jQuery.ajaxSettings.traditional = true;

    //const API_URL = 'http://127.0.0.1:8001'
    const API_URL = 'https://gale-ipl.azurewebsites.net'

    $(document.body).on('change', '.season-select', function(e){
        e.preventDefault();
        var selectedSeason = $('option:selected', this).val();
        window.location.replace(API_URL + '/season/' + selectedSeason);
    });

});
