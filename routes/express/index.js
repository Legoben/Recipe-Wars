module.exports = function(app) {
	app.get('/', function(req, res) {
		res.render('home',{
			title:"Emo Ice Cream Deluxe"
		});
	});
    
    app.get('/game', function(req, res) {
        //
        
		res.render('game',{
			title:"Play Emo Ice Cream Deluxe"
		});
	});
    
    
	app.get('/play', function(req, res) {
        //https://api.pearson.com/kitchen-manager/v1/cuisines?limit=50&apikey=NvQIAGWw4ynssAKix4gWCvu6DAW9OT1S
        
		res.render('play',{
			title:"Pick Category",
            foods: [{"n":"American","id":"american"},{"n":"American: Southern","id":"american-southern"},{"n":"Asian","id":"asian"},{"n":"French","id":"french"},{"n":"Indian","id":"indian"},{"n":"Italian","id":"italian"},{"n":"Mexican","id":"mexican"},{"n":"Other","id":"n-a"}]
		})
	});

};