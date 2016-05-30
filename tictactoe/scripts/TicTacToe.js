var Moment = require('moment');
var _ = require('lodash');
var Syncano = require('syncano');
var connection = new Syncano({apiKey: CONFIG.apiKey, instance: CONFIG.instanceName});

connection.class(CONFIG.className).dataobject().list().then(function(resp) {
    var players = resp.objects;

    _.forEach(players, function(player) {
        var lastActivity = player.updated_at;

        if (Moment(Date.now()).diff(lastActivity, 'minutes') > 5) {
            connection.class(CONFIG.className).dataobject(player.id).update({is_connected: false}, function(resp) {
                console.log(player.name + ' disconnected...');
            })
        }
    });
})