var Syncano = require('syncano');
var syncano = Syncano({accountKey: CONFIG.accountKey});
var instance = syncano.instance(CONFIG.instance);

instance.class('data').detail()
    .then(function(res){
        var count = {
            "count": res.objects_count
        }
        
        instance.class('counter').dataobject().list()
            .then(function(res){
                if(res.objects.length < 1){
                    instance.class('counter').dataobject().add(count)
                        .then(function(res){
                            console.log(res);
                        })
                        .catch(function(err){
                            console.log(err);
                        });
                } else {
                    instance.class('counter').dataobject(res.objects[0].id).update(count)
                        .then(function(res){
                            console.log(res);
                        })
                        .catch(function(err){
                            console.log(err);
                        });
                }
            })
            .catch(function(err){
                console.log(err);
            });
    })
    .catch(function(err){
        console.log(err);
    });