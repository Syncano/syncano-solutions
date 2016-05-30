var stripe = require('machinepack-stripe');

var apiKey = 'INSERT_STRIPE_API_KEY';

// Create a new charge for a customer
stripe.createCharge({
	apiKey: apiKey,
	amount: ARGS.amount,
	currency: ARGS.currency,
	card: ARGS.card,
	capture: ARGS.capture,
	description: ARGS.desc,
	customer: ARGS.customer,
}).exec({
	// An unexpected error occurred.
	error: function (err){
		console.log(err);
	},
	// OK.
	success: function (newCharge){
		console.log(newCharge);
	},
});