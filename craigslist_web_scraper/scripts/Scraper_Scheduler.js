/***** INSTRUCTIONS *****
 * Step 1: Put your account key from Syncano in the Config apiKey section
 * Step 2: Set the options below
    * label - label for how often this will run
    * codebox - find the id of the craigslist scraper codebox
    * crontab - http://docs.syncano.io/docs/schedules#section-creating-codebox-schedule-with-a-crontab-parameter
************************/

var Syncano = require('syncano');
var account = new Syncano({accountKey: CONFIG.accntKey});

var options = {
  label: "every monday at 10am", // Schedule label
  codebox: 1, // CodeBox Id to run
  crontab: "0 15 * * 1" // when schedule should run (cron syntax)
};

account.instance('aged-hill-6029').schedule().add(options)
    .then(function(res){
        console.log(res);
    })
    .catch(function(err){
        console.log(err);
    })