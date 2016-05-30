var Syncano = require('syncano');
var syncano = new Syncano({accountKey: CONFIG.accountKey});
var instance = syncano.instance(CONFIG.instance);

var object = {
    "title": "object"
}

instance.class('data').dataobject().add(object)
    .then(function(res){
        console.log(res);
    })
    .catch(function(err){
        console.log(err); 
    });