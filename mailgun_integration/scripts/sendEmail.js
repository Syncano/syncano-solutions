// **** INSTRUCTIONS **** //

/* Before running or setting schedules/triggers, */
/* sign up for a mailgun account: mailgun.com    */
/*                                               */
/* Also, fill out the CONFIG section!            */
/*                                               */
/* POST/GET request details:                     */
/* - "email":"yourEmail"                         */
/* - "subject":"yourSubject"                     */
/* - "message":"yourMessage"                     */
/*                                               */

var Syncano = require("syncano"); // CommonJS
var account = new Syncano({accountKey:CONFIG.syncanoAccountKey}); // gets AccountKey from Config
var instance = CONFIG.instance; // sets instance from Config
var mailgun = require("mailgun-js")({apiKey: CONFIG.mailgunAPIKey, domain: CONFIG.mailgunDomain}); // Mailgun API info

//** ARGS Variables **//
var toEmail = "";
var subject = "";
var message = "";
var attachment = null;
var correctParams = false;

if (checkParams(ARGS.GET) && checkParams(ARGS.POST)) { // if a dual request
    throw "This is a GET and POST request. Please pick one."
} else if (checkParams(ARGS.GET)) { // if it's a GET req
    toEmail = ARGS.GET.email;
    subject = ARGS.GET.subject;
    message = ARGS.GET.message;
} else if (checkParams(ARGS.POST)) { // if it's a POST req
    toEmail = ARGS.POST.email;
    subject = ARGS.POST.subject;
    message = ARGS.POST.message;
} else { // if no ARGS
    throw "Error - no arguments provided.";
}

// TODO add attachments

var data = { // contents of the email
  from: CONFIG.fromName + '<' + CONFIG.fromEmail + '>', // name <email>
  to: toEmail,
  subject: subject,
  text: message
};

mailgun.messages().send(data, function (error, body) { // send message using mailgun-js
  if (!error){ // if successful
      console.log("Your message was sent");
      logMailReceipts(); // log the message
  } else { // if an error
      console.log(body.message); // print it
  }
});

function logMailReceipts() { // logs the mail receipt in Syncano
    var log = { // log object
        "toEmail":toEmail,
        "subject":subject,
        "attachment":'false'
    }
    
    // add object call - requires userKey or AccountKey (or API with ignore_acl)
    account.instance(CONFIG.instance).class("maillogs").dataobject().add(log)
        .then(function(res){
            
        })
        .catch(function(err){
            throw err;
        });
}

function checkParams(args) { // checks parameters to make sure they're correct
    // EXPECTING: args.email, args.subject, args.message
    argsLength = Object.keys(args).length; // gets amount of args properties
    
    if (argsLength != 3) { // TODO change when attachments are added ****
        return false;
    } else { // if right amount of args
        if (!args.email || !args.subject || !args.message) { // if one is missing
            throw "You're missing a parameter! You need: email, subject, and message";
        } else { // success
            return true;
        }
    }
}