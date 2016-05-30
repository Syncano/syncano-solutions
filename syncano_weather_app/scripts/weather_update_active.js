var Syncano = require('syncano');

var instance = new Syncano({accountKey: CONFIG.accountKey}).instance(META.instance);
var cities = instance.class('weather_active_cities').dataobject();
var codebox = instance.codebox(CONFIG.codeboxId);

cities.list().then(function(res){
    var objects = res.objects;
    for(var i = 0; i < objects.length; i++) {
        codebox.run({payload: {city_id: objects[i].city_id}});
    }
});