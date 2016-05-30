var Syncano = require('syncano');
var _ = require('lodash');
var Http = require('machinepack-http');

ARGS = _.merge({}, ARGS, ARGS.POST, ARGS.GET);
delete ARGS.POST;
delete ARGS.GET;

//Sample Data to test -> {"city": "Indianapolis", "stateOrCountry": "IN"}

var instance = new Syncano({apiKey: CONFIG.accountKey, instance: META.instance});

var weatherObjects = instance.class("weather_active_cities").dataobject();

var baseOpts = {
    baseUrl: 'http://api.openweathermap.org/data/2.5/',
    method: 'get',
    params: {
        APPID: CONFIG.open_weather_map_api_key
    }
};

var localOpts;

var allData = {};

var callOpenWeather = function(options, cb) {
    return (
        Http.sendHttpRequest(options)
        .exec({
            success: function(httpResponse) {
                cb(JSON.parse(httpResponse.body));
            },
            error: function(err) {
                console.log(err);
            }
        })
    );
};

var getCurrentWeather = function(options, cb) {
    var opts = _.merge({}, options, baseOpts);
    opts.url = 'weather';
    return callOpenWeather(opts, cb);
};

var getForecast = function(options, cb) {
    var opts = _.merge({}, options, baseOpts);
    opts.url = 'forecast/daily';
    opts.params.cnt = 5;
    return callOpenWeather(opts, cb);
};


var getWeatherData = function(opts, cb) {
    getCurrentWeather(opts, function(data){
        allData = _.merge({}, formatCurrentData(data), allData);
        getForecast(opts, function(data) {
            allData = _.merge({}, formatForecastData(data), allData);
            cb(allData);
        });
    });
};

var formatCurrentData = function(data) {
    var obj = {};
    obj.city_id = data.id;
    obj.city_name = data.name,
    obj.current_temp = data.main.temp;
    obj.short_description = data.weather[0].main;
    return obj;
};

var formatForecastData = function(data) {
    var obj = {forecast:{}};
    data.list.shift();
    _.forEach(data.list, function(value) {
        var f = {
            temp_min: value.temp.min,
            temp_max: value.temp.max,
            short_description: value.weather[0].main,
        };
        obj.forecast[value.dt] = f;
    });
    obj.forecast = JSON.stringify(obj.forecast);
    return obj;
};

var getIdbyCityId = function(data, cb) {
    weatherObjects.list({query: {city_id:{_eq:data.city_id}}}).then(function(res){
        if (res.objects.length === 0) {
            cb(false);
        } else {
            cb(res.objects[0].id);
        }
        
    })
    .catch(function(err) {
        cb(err);
    });
};

var addActiveCity = function(data) {
    data.channel = "weather_realtime";
    data.channel_room = data.city_id;
    data.other_permissions = "full";
    weatherObjects.add(data).catch(function(err) {});
};

var updateActiveCity = function(id, data) {
    weatherObjects.update(id, data).catch(function(err) {console.log(err)});
};

if ((!ARGS.city || !ARGS.stateOrCountry)&& !ARGS.city_id) {
    console.log('Valid data for both "stateOrCountry" and "city", or only "city_id" must be provided.');
} else if (ARGS.city_id) {
    localOpts = {
        params : {id: ARGS.city_id}
    };
} else {
    var cityStateOrCountry = ARGS.city + ',' + ARGS.stateOrCountry;
    localOpts = {
        params : {q: cityStateOrCountry}
    };
}

getWeatherData(localOpts, function(res){
    getIdbyCityId(res, function(id) {
        if (id) {
            updateActiveCity(id, res);
        } else {
            addActiveCity(res);
        }
    });
    console.log(JSON.stringify(res));
});