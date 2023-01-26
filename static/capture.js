// Global variables for serial number and amount calculation

var cnt = 0; 
var amount = 0;

(function() {
  // The width and height of the captured photo.

  var width = 320;    
  var height = 0;   



  var streaming = false;

  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;

  function startup() {
    video = document.getElementById('video');
    // video.setAttribute('playsinline', '');
    // video.setAttribute('autoplay', '');
    // video.setAttribute('muted', '');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');

    var facingMode = "environment"; // Can be 'user' or 'environment' to access back or front camera (NEAT!)

    navigator.mediaDevices.getUserMedia({video:  {facingMode: facingMode}, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);
      
        if (isNaN(height)) {
          height = width / (4/3);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);

    startbutton.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
    }, false);
    
    clearphoto();
  }

  // Fill the photo with an indication that none has been
  // captured.

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);


    var data = canvas.toDataURL('image/png');

    // Saving the Image as Png in the preview window
    photo.setAttribute('src', data);
  }
  

  // Drawing the Image in Canvas

  function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);
    
      var data = canvas.toDataURL('image/png');
      
      photo.setAttribute('src', data);

      //--------------------------------------------------------------------

      var request = new XMLHttpRequest();
 
      request.open('POST', 'http://192.168.43.36:5000/upload');
      request.setRequestHeader('Content-Type', 'image/png');
      request.onload = function (e) {
          if (request.readyState == 4 &&  request.status == 200) {
            
              console.log(request.responseText);
              var result = JSON.parse(request.responseText);
              console.log(result);

              var countVal = document.getElementById("box").value;

              finalResult = countVal * result['Cost'];
              
              //Insert rows and columns dynamically 
              
                var table = document.getElementById("bill");
                var row = table.insertRow(-1);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);                
                cell1.innerHTML = ++cnt;
                cell2.innerHTML = result['Id'];
                cell3.innerHTML = result['Name'];
                cell4.innerHTML =  result['Cost'];
                cell5.innerHTML = countVal;
                cell6.innerHTML = finalResult;
                amount = amount + finalResult;

          } else {
              console.log(e);
          }
      };
      request.send(data);

      //-------------------------------------------------------------
    
    } else {
      clearphoto();
    }
  }

  window.addEventListener('load', startup, false);
})();


//Function for finding the Total Rupees

function sum(){
  var table = document.getElementById("bill");
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
  var cell5 = row.insertCell(4);
  var cell6 = row.insertCell(5);
  cell1.innerHTML = "";
                cell2.innerHTML ="";
                cell3.innerHTML = "";
                cell4.innerHTML =  "";
                cell5.innerHTML = "Rupees";
                cell6.innerHTML = amount;
}



// JSPDF for downloading Bill as Pdf

function downloadPdf(){
  source = $('#bill-div')[0];

  var pdf = new jsPDF('p', 'pt', 'letter');


    specialElementHandlers = {

        '#bypassme': function (element, renderer) {
      
            return true
        }
    };
    margins = {
        top: 80,
        bottom: 60,
        left: 40,
        width: 522
    };

    pdf.fromHTML(
    source, 
    margins.left, // x coord
    margins.top, { // y coord
        'width': margins.width, 
        'elementHandlers': specialElementHandlers
    },

    function (dispose) {
        pdf.save('ProductBill.pdf');
    }, margins);
}