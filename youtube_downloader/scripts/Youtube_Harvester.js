//Yo use this CodeBox you will need to pass a query that the search will be done on
//e.g {'query':'funny cats'} or {'query':'javascript'}
//if you don't provide a query, one is taken from Config

//Before running, please make sure to edit the Config and provide your Syncano Account Key 
//and YouTube (Google) Developer API Key 

//To obtain YouTube enabled developer API Key, go to: https://console.developers.google.com/project
//add a new project, go into "APIs & auth" -> "APIs", find "YouTube Data API" and enable it
//Now go into "APIs & auth" -> "Credentials" and create a key:
// - Click "Add Credentials"
// - Choose "Server Key"
// - Click Create
// - Copy newly created API Key and add it to Config of this CodeBox and save it

//Your Syncano Account Key you can find in your Account settings:
// - use the link: https://dashboard.syncano.io/#/account/authentication
// - click Copy next to the Account Key
// - add the key to the Codebox config and save it

//Results of downloading YouTube videos list are stored in a Class called videos
// - in the menu on the left, click on Classes and "videos"

var http = require('https');
var querystring = require('querystring');
var Syncano = require('syncano');

function getArgument(name, defaultValue) {
    var argument;
    if (ARGS.query !== undefined) {
        argument = ARGS[name];
    } else if (ARGS.GET !== undefined && ARGS.GET[name] !== undefined) {
        argument = ARGS.GET[name];
    } else if (ARGS.POST !== undefined && ARGS.POST[name] !== undefined) {
        argument = ARGS.POST[name];
    }
    if (argument === undefined) {
        argument = defaultValue;
    }
    return argument;
}

var query = getArgument('query',CONFIG['default-query']);

var account = new Syncano({accountKey: CONFIG['syncano-account-key']});

// list of params
// https://developers.google.com/youtube/v3/docs/search/list
var params = querystring.stringify({
    part: 'id,snippet',
    type: 'video',
    maxResults: CONFIG['max-number-of-results'],
    key: CONFIG['google-developer-key'],
    q: query,
    order: 'date'
});

var options = {
    hostname: 'www.googleapis.com',
    port: 443,
    path: '/youtube/v3/search?' + params,
    method: 'GET'
};

function parseVideosObjects(data) {
    var object = JSON.parse(data);
    if (object.items === undefined) {
        log("Error: Didn't download anything. Check your YouTube API Key.");
        return;
    }
    var list = [];
    log('Downloaded ' + object.items.length + ' items');
    for (var i = 0; i < object.items.length; i++) {
        var video = {
            source_id: object.items[i].id.videoId,
            url: 'https://youtube.com/watch?v=' + object.items[i].id.videoId,
            title: object.items[i].snippet.title,
            video_description: object.items[i].snippet.description,
            published_at: object.items[i].snippet.publishedAt,
            other_permissions: 'read',
            channel: 'youtube_videos'
        };
        list.push(video);
    }

    pushToSyncano(list);
}

function log(content) {
    console.log(content);
}

function pushToSyncano(videosList) {
    success = function() {
        log('Success saving data to Syncano');
    };
    error = function() {
        log('Error saving data to Syncano. Check your Account Key.');
    };

    for (var i = 0; i < videosList.length; i++) {
        var video = videosList[i];
        account.instance(META.instance).class('video').dataobject().add(video).then(success).catch(error);
    }
}

function sendHttpRequest(options, callback) {
    var req = http.request(options, function(res) {
        res.setEncoding('utf8');
        var dataResponse = '';
        res.on('data', function(chunk) {
            dataResponse += chunk;
        });
        res.on('end', function() {
            callback(dataResponse);
        });
    });
    req.on('error', function(e) {
        log('Error from Youtube ' + e);
    });
    req.end();
}

sendHttpRequest(options, parseVideosObjects);