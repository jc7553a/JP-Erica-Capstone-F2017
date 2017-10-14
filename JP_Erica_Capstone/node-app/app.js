var express = require('express');
var app = express();
var path = require('path');
var formidable = require('formidable'); // file transfer
var fs = require('fs');

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function(req, res){
    res.sendFile(path.join(__dirname, 'views/index.html'));
});

app.post('/upload', function(req, res){
    // create an incoming form object
    var form = new formidable.IncomingForm();

    // we only want to let the user upload one file
    form.multiples = false;

    // store all uploads in the uploads dir
    form.uploadDir = path.join(__dirname, '/uploads');

    // every time a file has been uploaded successfully, save it as test.wav
    form.on('file', function(field, file) {
        fs.rename(file.path, path.join(form.uploadDir, "test.wav"));
    });

    // log any errors that occur
    form.on('error', function(err) {
        console.log('An error has occured: \n' + err);
    });

    // once all the file has been uploaded let the client know
    form.on('end', function() {
        res.end('success');
    });

    // parse the incoming request containing the form data
    form.parse(req);
});

// have server listen on port 3000
var server = app.listen(3000, function(){
    console.log('Server listening on port 3000');
});
