var sendgrid  = require('sendgrid')(CONFIG.apiKey);

ARGS = ARGS.POST || ARGS; // Determine if this is being called by a Webhook or Trigger

sendgrid.send({
  to:       ARGS.to || CONFIG.to,
  toname:   ARGS.toName || CONFIG.toName,
  from:     ARGS.from || CONFIG.from,
  fromname: ARGS.fromName || CONFIG.fromName,
  subject:  ARGS.subject || CONFIG.subject,
  text:     ARGS.text || CONFIG.text,
  html:     ARGS.html || CONFIG.html,
  bcc:      ARGS.bcc || CONFIG.bcc,
  cc:       ARGS.cc || CONFIG.cc,
  replyto:  ARGS.replyTo || CONFIG.replyTo,
  date:     ARGS.date || CONFIG.date
}, function(err, json) {
  if (err) { return console.error(err); }
  console.log(json);
});

// For more info on SendGrid functions, visit https://github.com/sendgrid/sendgrid-nodejs.