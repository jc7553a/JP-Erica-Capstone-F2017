var express = require('express');
var app = express();
var path = require('path');
var formidable = require('formidable'); // file transfer
var fs = require('fs');
var spawn = require('child_process').spawn;

var data = "Erica and JP";
var dataString = '';
var counter = 1;

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
        console.log("kickoff");
<<<<<<< HEAD
        var py = spawn('python', ['main.py']);       
=======
        
>>>>>>> 5d1811e0a88af564ac1ce4cde071073638426ab5
        /// function to kickoff python script using child_process mod
        var dataString = "";
        console.log('readingin');

        var py = spawn('python', ['helloworld.py']);        
        var textChunk = "Hai";
        py.stdout.on('data', function(chunk){
            textChunk = chunk.toString('utf8');// buffer to string
            console.log(textChunk);
        });
        // converts data to string and then send it to python script
        // py.stdout.on('data', function(data){
        //     console.log("data");
        //     console.log(data);
        //     dataString += data.toString();
        // });
        py.stdout.on('end', function(){
            console.log(textChunk);
            textChunk = textChunk + counter.toString();
            alertSuccess(textChunk);
            counter = counter + 1;
            //py.stdin.write(data.toString());
        });
        // console.log("here");
        // console.log(data.toString());
        // try {
        //     py.stdin.write(data.toString());
        // } catch(err) {
        //     console.log(err);
        // }
        // console.log("test");
        // py.stdin.end();
        // console.log("kickoff done");
    }
    
    var alertSuccess = function(dataString){
        console.log("alertSuccess");
        successJSONString = dataString.toString();
	//console.log(typeof successJSONString);
	var newString = successJSONString.replace(/\[/g , "");
	var newString2 = newString.replace(/\]/g, "");
	var newString3 = newString2.replace(/\'/g, "");
	var newString4 = newString3.replace(/\, /g, "");
	//var array = JSON.parse("["+ successJSONString + "]");
	//var chord = array[0][0]
	console.log(newString4);
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
        console.log("saved");
    });

    // log any errors that occur
    form.on('error', function(err) {
        console.log('An error has occured: \n' + err);
    });

    // once all the file has been uploaded let the client know
    form.on('end', function() {
        kickoff("/Data/Uploads/test.wav");
    });

    var alertSuccess = function(dataString){
        console.log("alertSuccess");
        console.log(dataString);
        //successJSONString = dataString.replace(/'/g, ' ');
        //delete file
        res.end(dataString);  
    }

    // parse the incoming request containing the form data
    form.parse(req);
});

// have server listen on port 3000
var server = app.listen(3000, function(){
    console.log('Server listening on port 3000');
});
