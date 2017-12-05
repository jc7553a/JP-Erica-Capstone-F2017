var express = require('express');
var app = express();
var path = require('path');
var formidable = require('formidable'); // file transfer
var fs = require('fs');
var spawn = require('child_process').spawn;
try{
process.chdir('\Chord-Recognition');
var py = spawn('python', ['main.py']);
}
catch(err)
{
console.log('dammit');
}

var data = "Erica and JP";
var dataString = '';

app.use(express.static(path.join(__dirname, 'public')));

app.use('/js', express.static(__dirname + '/node_modules/bootstrap/dist/js')); // redirect bootstrap JS
app.use('/js', express.static(__dirname + '/node_modules/jquery/dist')); // redirect JS jQuery
app.use('/css', express.static(__dirname + '/node_modules/bootstrap/dist/css')); // redirect CSS bootstrap
app.use('/fonts', express.static(__dirname + '/node_modules/bootstrap/dist/fonts')); // redirect bootstrap JS


app.get('/', function(req, res){
    res.sendFile(path.join(__dirname, 'views/index.html'));
});

app.post('/upload', function(req, res){
    var kickoff = function(data){
        /// function to kickoff python script using child_process mod
        var dataString = ""
        // converts data to string and then send it to python script
        py.stdout.on('data', function(data){
            dataString += data.toString();
        });
        py.stdout.on('end', function(){
            console.log('Test:',dataString);
            alertSuccess(dataString);
        });
        py.stdin.write(JSON.stringify(data));
        py.stdin.end();
    }
    

    var alertSuccess = function(dataString){
        console.log("alertSuccess");
        successJSONString = "{\"success\" : \"" + dataString.toString() +  "\", \"status\" : 200}";
        console.log(typeof successJSONString);
	//var len = successJSONString.length;
	//console.log(len);
	//var newString = successJSONString.substring(16, (len- 44));
	//console.log(newString);
	//var newString2 = newString.replace(/'/g, '"');
	//var array = JSON.parse("[" + newString2 + "]");
	//console.log(typeof array)
	res.end(successJSONString);  
    }

    // create an incoming form object
    var form = new formidable.IncomingForm();

    // we only want to let the user upload one file
    form.multiples = false;

    // store all uploads in the uploads dir
    form.uploadDir = path.join(__dirname, 'Chord-Recognition/Data/Uploads');

    // every time a file has been uploaded successfully, save it as test.wav
    form.on('file', function(field, file) {
        // save file as test.wav
        fs.rename(file.path, path.join(form.uploadDir, "test.wav"));
    });

    // log any errors that occur
    form.on('error', function(err) {
        console.log('An error has occured: \n' + err);
    });

    // once all the file has been uploaded let the client know
    form.on('end', function() {
        kickoff("/Data/Uploads/test.wav");
    });

    // parse the incoming request containing the form data
    form.parse(req);
});

// have server listen on port 3000
var server = app.listen(3000, function(){
    console.log('Server listening on port 3000');
});