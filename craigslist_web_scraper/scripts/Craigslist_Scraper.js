/*************************************************************
*    Syncano Craigslist Item Scraper Codebox
*    Author: Devin Visslailli
*    
*    Credit to: Adnan Kukic through Scotch.io
*    https://scotch.io/tutorials/scraping-the-web-with-node-js
**************************************************************/

/***** INSTRUCTIONS *****
 * Step 1: Sign Up for Mailgun - www.mailgun.com
 * Step 2: Set Up Config Tab (up top)
    * 'email' is the email you want this list to be sent to
    * 'mail_api' is your Mailgun private API key
    * 'mail_domain' is your Mailgun sandbox default domain (sandbox...@mailgun.com)
 * Step 3: Set region and item in "Payload" box
    * Inside payload, type: {"region":"YOUR_REGION","search":"ITEM"}
 * Optional: Set Variables Below
 * Step 4: Save and Open Scraper Scheduler Codebox to set up the schedule
************************/

var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');
var Mailgun = require('machinepack-mailgun');

// Example payload: {"region":"newyork","search":"macbook"}
// OR
// Set permanent region and search by uncommenting the next line
// ARGS = {"region":"newyork","search":"macbook"};
var region = ARGS.region;
var search = ARGS.search;
var urlHome = "https://" + region + ".craigslist.org";
var urlSearch = urlHome + "/search/sss?sort=rel&query=" + search;

/**********************
*   SET YOUR VARIABLES
***********************/
var numItems = 20; // amount of items to send to your email
var emailName = "NAME";

// The first parameter is our URL
// The callback function takes 3 parameters, an error, response status code and the html
request(urlSearch, function(error, response, html){
    
    if(!error){
        var $ = cheerio.load(html); // Cheerio library helps build a DOM structure we can iterate through
        var itemDataArray = []; // where we'll store item objects
        counter = 0; // counter for the array
        
        $('.row').filter(function(){ // cheeriojs filter function
            var list = $(this);
            Item = function() {
                this.datePosted = "";
                this.title = "";
                this.price = 0.0;
                this.location = "";
                this.link = "";
            };
            
            // Craigslist specific DOM elements
            var item = new Item();
            item.datePosted = list.find('time').attr('title');
            item.title = list.find('.hdrlnk').text();
            item.price = list.find('.l2').find('.price').text();
            item.location = list.find('.pnr').find('small').text();
            item.link = urlHome + list.find('.hdrlnk').attr('href');
            itemDataArray[counter] = item;
            counter++;
        })
        
        sendResults(itemDataArray); // function to email results
    } else {
        console.log("Error!", error);
    }
})

function sendResults(results) {
    var htmlResults = "<h1>Search Results</h1><br>"; // Email header
    
    for (i = 0; i < numItems; i++){ // numItems set in global variables above
        htmlResults += '<h2>' + (i+1) + '. ' + results[i].title + '</h2>' +
            '<h3>Price: ' + results[i].price + '</h3>' +
            '<p>Location: ' + results[i].location + '</p>' +
            '<p>Date Posted: ' + results[i].datePosted + '</p>' +
            '<a href="' + results[i].link + '">Link</a>' +
            '<br><br>';
    }
    
    htmlResults += "<small>Sent by a Syncano Codebox</small>";
    
    // Using Mailgun Machinepack to send emails
    Mailgun.sendHtmlEmail({ // set CONFIG variables in the config tab up top
        apiKey: CONFIG.mail_api,
        domain: CONFIG.mail_domain,
        toEmail: CONFIG.email,
        toName: emailName,
        subject: 'Craigslist Scraper Results for ' + ARGS.search + ' in ' + ARGS.region,
        htmlMessage: htmlResults,
        fromEmail: 'no-reply@syncano.com',
        fromName: 'Syncano Codebox No-Reply'
        }).exec({
        error: function (err){
            console.log(err);
        },
        success: function (){
            console.log("Message sent!");
        },
    });
}