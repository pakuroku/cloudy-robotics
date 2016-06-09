var http = require('http'),   // require is used in nodeJS to import modules to the program. In this case, the http module is added
    fs = require('fs'),		  // import fs (filesystem) module for reading files
    // NEVER use a Sync function except at start-up!
    index = fs.readFileSync(__dirname + '/client/index.html');	// reads our webpage index.html file. __dirname specifies the directory path where this script resides

var url = require("url");	  // imports url module provides functions for url parsing and error checking
var path = require('path');	  // handles and changes file paths  
var mime = require('mime');   // used to get the mime content-type of the file

// Send index.html to all requests
var app = http.createServer(function(req, res) {  // creates the http server
    var dir = "/client";		
    var uri = url.parse(req.url).pathname;	// parses url pathname	
    if (uri == "/")
    {
        uri = "index.html";				// name of the html file
    }
    var filename = path.join(dir, uri);  // concatenates file name with file path
    console.log(filename);
    console.log(mime.lookup(filename)); // displays mime type 
    fs.readFile(__dirname + filename,	// reads index.html
        function (err, data)						
        {
            if (err)
            {
                res.writeHead(500);   // if there is an error, send code 500 to the requester
                return res.end('Error loading index.html');
            }
            console.log(data);		
            console.log(filename + " has read");	// display that file index.html has been read
            res.setHeader('content-type', mime.lookup(filename));  // sets header with the content-type. In our case it is text/html.
            res.writeHead(200);						// sends code 200 to indicate that index.html was successfully read for the request
            res.end(data);							// write data to the request
        });
});

// Socket.io server listens to our app
var io = require('socket.io').listen(app);// loads socketIO module to handle the connect to the python and HTML clients and binds http server object to socketIO
var voltage = 0;	//initializes values 
var count1 = 0;
var count2 = 0;
var degree1 = 0;
var degree2 = 0;
var current = 0;
var charging = "not charging";
// Send current time to all connected clients
function senddata() {	// this function sends data received from python programs to index.html via socketIO
        io.sockets.emit('current',current);	
        io.sockets.emit('count1',count1);
        io.sockets.emit('count2',count2);
        io.sockets.emit('voltage',voltage);         
        io.sockets.emit('degree1',degree1);
        io.sockets.emit('degree2',degree2);
		io.sockets.emit('charging',charging);
	}

function action(command) {	// this function passes any robot control command received from index.html
	console.log(command);
	io.sockets.emit('raspberry', command);	// passes robot control command using emit() to the raspberry pi python programs and names it "raspberry" as the event
}


setInterval(senddata, 1000); // executes senddata function every second which sends all data from the python programs

// Emit welcome message on connection
io.sockets.on('connection', function(socket) {	
    //socket.emit('welcome', { message: 'Welcome!' });	
    //socket.on('i am client', console.log);
    socket.on('action', action);	// listens for robot control command from the index.html webpage using on()	
    socket.on('voltage',function(volts) {   // listens for voltage,current,encoder counts, position in degrees, and battery status values from raspberry pi python programs
              
              //console.log(volts);
              voltage = volts;
    });
    socket.on('current',function(amps) {
            
              //console.log(current);
              current = amps;
    });

    socket.on('count1',function(count) {
              
              //console.log(count);
              count1 = count;
    });
    socket.on('count2',function(count) {
              
              //console.log(count);
              count2 = count;
    });
    socket.on('degree1',function(degree) {
             
              //console.log(degree1);
              degree1 = degree;
    });
    socket.on('degree2',function(degree) {
              
              //console.log(degree2);
              degree2 = degree;
    });
    socket.on('totaldegree2',function(degree) {
              
              //console.log(degree2);
              degree2 = degree;
    });
    socket.on('charging',function(battery_is_charging_or_not) {
              //console.log(charging);
              charging = battery_is_charging_or_not;
    });

});

app.listen(3000);	// http server object listens at port 3000
