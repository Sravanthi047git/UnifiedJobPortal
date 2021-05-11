var express = require('express');
var router = express.Router();


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

/* GET Hello World page. */
router.get('/helloworld', function(req, res) {
  res.render('helloworld', { title: 'Hello, World!' });
});


/* GET Userlist page. */
router.get('/joblist', function(req, res) {
  var db = req.db;
  var collection = db.get('jobs_tbl');

  collection.find({},{},function(e,docs){
      res.render('joblist', {
          "joblist" : docs
      });
  });
});


/* POST to Add User Service */
router.post('/addsearch', function(req, res) {
//router.get('/', (req, res) => {

        const {spawn} = require('child_process');

        // Get our form values. These rely on the "name" attributes
        var desig = req.body.designation;
        var loc = req.body.location;
        var ttl_jobs = req.body.no_of_jobs;
        var job_site = req.body.site;

         // spawn new child process to call the python script
         const python = spawn('python', ['/Users/twinklem/Desktop/OneDrive/CCA/projects/asp/Python/final/main.py', desig, loc, ttl_jobs, job_site]);



         // collect data from script
         python.stdout.on('data', function (data) {
          console.log('Pipe data from python script ...');
            //res.send("Scrapping jobs from the web page....please wait. Once it is completed you will be redirected to jobs list".toString());
         res.redirect("joblist");   //can not use response 2 times

         });


         // in close event we are sure that stream from child process is closed
         python.on('close', (code) => {
         console.log(`child process close all stdio with code ${code}`);

         });


});

module.exports = router;
