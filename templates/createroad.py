import sys
import subprocess
import shutil
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
default='''
{% extends 'base.html' %}

{% block content %}

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
<script src=
"https://cdnjs.cloudflare.com/ajax/libs/sweetalert/2.1.0/sweetalert.min.js">
  </script>

<nav class="navbar navbar-expand-sm">
  <div class="container-fluid">
    <a class="d-flex align-items-center fs-4 ml-4 mb-4 link-underline link-underline-opacity-0" id="myLink" href="{% url 'dashboard' %}">
      <i class="bi bi-chevron-left"></i>
      Back
      <span class="mx-3 spinner-border spinner-border-sm" role="status" id="mySpinner" style="display: none;"></span>
    </a>
  </div>
</nav>


<div class="text-center card mx-auto p-1 bg-body-secondary " style="width:80vw; border-width: 0px; font-size: 24px">
<div class="card-body">
'''

defaultend='''

</div>
</div>
<div class="d-flex justify-content-center">
<div class="text-center rounded-pill bg-body-secondary btn-group m-5 p-2 ">
<button id="incrementButton" class="btn tiny  mb-1">
    <i class="ph ph-x-square h4"></i><br>Hide More</button>

<button id="finishButton" class="btn tiny h6 mb-1">
    <i class="ph ph-flag-checkered h4"></i><br>Finish verse</button>

<button id="nextButton" class="btn tiny mb-1">
    <i class="ph ph-arrow-square-right h4"></i><br>Next Verse</button>


  <button 
    class="btn tiny mb-1" id="backButton">
    <i class="ph ph-arrow-square-left h4"></i><br>Previous

  </button>
  </div>
</div>
<div class="progress-container">
<div class="progress">
  <div id="progressBar" class="progress-bar lrm-5" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
</div>
<style>
nav{
  margin:0;
}
.hide-word {
         
        color: transparent;
        text-shadow: 0 0 13px #000;
}
.tiny {
  font-size: 0.8rem;
}
  html,
  body {
    overflowX: hidden;
  }

  body {
    padding-bottom: 40px;
    
    overflow-x: hidden;
  }
hr.rounded {
  border-top: 8px solid #bbb;
  border-radius: 5px;
}
.progress-container {
  padding: 0 15vw; /* Adjust the padding as needed */
  max-width: 600vw; /* Set a maximum width for the progress bar container */
  margin: 0 auto; /* Center the container on the screen  </script>
  {% endblock %}*/
}
bb {
  background-color: #343A40;
}


</style>

<script src="
https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/dist/js.cookie.min.js
"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the link and spinner elements
    const link = document.getElementById('myLink');
    const spinner = document.getElementById('mySpinner');

    // Attach click event listener to the link
    link.addEventListener('click', function() {
      // Show the spinner
      spinner.style.display = 'block';

      // Simulate some asynchronous task
      setTimeout(function() {
        // Hide the spinner after the task is completed
        spinner.style.display = 'none';
      }, 2000); // Replace this with your actual task
    });
  });
  var sentences = document.querySelectorAll("p[id^='sentence']");
  var currentSentenceIndex = 0;
  var hiddenWordIndices = [];
  // Other JavaScript code...

  // Function to save the user's progress using AJAX
var sentences = document.querySelectorAll("p[id^='sentence']");
var currentSentenceIndex = 0;
var hiddenWordIndices = [];
var hideButton = document.getElementById("incrementButton"); // Get the hide button element
var nextButton = document.getElementById("nextButton"); // Get the next button element
var finishButton = document.getElementById("finishButton"); // Get the finish button element
var progressBar = document.getElementById("progressBar"); // Get the progress bar element

hideButton.addEventListener('click', function () {
  hideRandomWords(3);
}, true);

nextButton.addEventListener('click', function () {
  moveToNextSentence();
  var username = "Anonymous"; // You should get the actual username from your Django backend if the user is authenticated.
  saveUserProgress(username, currentSentenceIndex);
}, true);

var finishButtonClicks = 0; // Variable to track the number of finish button clicks

finishButton.addEventListener('click', function () {
  finishButtonClicks++;
  if (finishButtonClicks === 1) {
    hideAllWords();
  } else if (finishButtonClicks === 2) {
    revealAllWords();

    var randomIndices = [];

    isHidden = false;
      
    finishButtonClicks = 0; // Reset the click counter
  }
}, true);

function hideRandomWords(numWords) {
  var currentSentence = sentences[currentSentenceIndex];
  var sentenceText = currentSentence.textContent;

  var words = sentenceText.split(" ");

  var visibleWordIndices = words
    .map(function (_, index) {
      return index;
    })
    .filter(function (index) {
      return hiddenWordIndices.indexOf(index) === -1;
    });

  if (visibleWordIndices.length === 0) {
    console.log("No visible words left to hide.");
    hideButton.disabled = true; // Disable the hide button if there are no visible words
    return;
  }

  // Adjust numWords to ensure it doesn't exceed the number of visible words
  numWords = Math.min(numWords, visibleWordIndices.length);

  var randomIndices = [];
  while (randomIndices.length < numWords && visibleWordIndices.length > 0) {
    var randomIndex = Math.floor(Math.random() * visibleWordIndices.length);
    var randomVisibleIndex = visibleWordIndices[randomIndex];
    randomIndices.push(randomVisibleIndex);
    visibleWordIndices.splice(randomIndex, 1);
  }

  hiddenWordIndices = hiddenWordIndices.concat(randomIndices);

  for (var i = 0; i < words.length; i++) {
    if (hiddenWordIndices.indexOf(i) !== -1) {
      words[i] = '<span class="hide-word">' + words[i] + "</span>";
    }
  }

  currentSentence.innerHTML = words.join(" ");

  console.log("Total Hidden Words in Sentence " + (currentSentenceIndex + 1) + ": " + hiddenWordIndices.length);

  if (hiddenWordIndices.length === words.length) {
    hideButton.disabled = true;
  }
}

function hideAllWords() {
  var currentSentence = sentences[currentSentenceIndex];
  var words = currentSentence.textContent.split(" ");

  hiddenWordIndices = [];
  for (var i = 0; i < words.length; i++) {
    hiddenWordIndices.push(i);
    words[i] = '<span class="hide-word">' + words[i] + "</span>";
  }

  currentSentence.innerHTML = words.join(" ");
  hideButton.disabled = true;
}

function revealAllWords() {
  var currentSentence = sentences[currentSentenceIndex];
  var words = currentSentence.getElementsByTagName("span");

  for (var i = 0; i < words.length; i++) {
    words[i].classList.remove("hide-word");
  }

  hideButton.disabled = false;

}

function moveToNextSentence() {
  currentSentenceIndex++;

  if (currentSentenceIndex >= sentences.length) {
    console.log("You have finished all the sentences.");
    hideButton.disabled = true;
    nextButton.disabled = true;
    swal("You Finished this road!", {
    title:"Good job!",
    icon:"success",
    buttons: {
    catch: {
      text: "Back to dashboard",
      value: "catch",
    },
      text : "try again",
  },
})
.then((value) => {
  switch (value) {
 
    
 
    case "catch":
      window.location.href = "{% url 'dashboard' %}";
      break;
 
    default:

    location.reload();
  }
});    finishButton.disabled = true;
    return;
  }
   

  // Reset hiddenWordIndices array and enable the buttons
  hiddenWordIndices = [];
  hideButton.disabled = false;
  nextButton.disabled = false;
  finishButton.disabled = false;

  // Hide the current sentence
  var currentSentence = sentences[currentSentenceIndex - 1];
  currentSentence.style.display = "none";

  // Show the next sentence
  var nextSentence = sentences[currentSentenceIndex];
  nextSentence.style.display = "block";
  
  // Update the progress bar
  var progressWidth = ((currentSentenceIndex + 1) / sentences.length) * 100;
  progressBar.style.width = progressWidth + "%";
  progressBar.setAttribute("aria-valuenow", progressWidth);
}
  

// Hide all sentences except the first one
for (var i = 1; i < sentences.length; i++) {
  sentences[i].style.display = "none";
}

var USERNAME_COOKIE_NAME = "user_progress_username";
var SENTENCE_COOKIE_NAME = "user_progress_sentence";

function saveUserProgress(username, sentenceIndex) {
  Cookies.set(USERNAME_COOKIE_NAME, username, { expires: 7 }); // Set the username cookie to expire in 7 days
  Cookies.set(SENTENCE_COOKIE_NAME, sentenceIndex);
}

function restoreUserProgress() {
  var username = Cookies.get(USERNAME_COOKIE_NAME);
  var sentenceIndex = Cookies.get(SENTENCE_COOKIE_NAME);
  
  if (username && sentenceIndex) {
    // Restore the user's progress
    currentSentenceIndex = parseInt(sentenceIndex);
    
    // Find the sentence element and hide all sentences except the current one
    for (var i = 0; i < sentences.length; i++) {
      if (i === currentSentenceIndex) {
        sentences[i].style.display = "block";
      } else {
        sentences[i].style.display = "none";
      }
    }
    
    // Update the progress bar
    var progressWidth = ((currentSentenceIndex + 1) / sentences.length) * 100;
    progressBar.style.width = progressWidth + "%";
    progressBar.setAttribute("aria-valuenow", progressWidth);
  }
}

var backButton = document.getElementById("backButton"); // Get the back button element

backButton.addEventListener('click', function () {
  moveToPreviousSentence();
}, true);

function moveToPreviousSentence() {
  currentSentenceIndex--;

  if (currentSentenceIndex < 0) {
    console.log("You are already at the beginning.");
    currentSentenceIndex = 0; // Make sure the index doesn't go below 0
    backButton.disabled = true;
    return;
  }

  // Reset hiddenWordIndices array and enable the buttons
  hiddenWordIndices = [];
  hideButton.disabled = false;
  nextButton.disabled = false;
  finishButton.disabled = false;

  // Hide the current sentence if it exists
  if (currentSentenceIndex + 1 < sentences.length) {
    var currentSentence = sentences[currentSentenceIndex + 1];
    currentSentence.style.display = "none";
  }

  // Show the previous sentence
  var previousSentence = sentences[currentSentenceIndex];
  previousSentence.style.display = "block";

  // Update the progress bar
  var progressWidth = (currentSentenceIndex / (sentences.length - 1)) * 100;
  progressBar.style.width = progressWidth + "%";
  progressBar.setAttribute("aria-valuenow", progressWidth);

  // Enable/disable the back button based on the current sentence index
  backButton.disabled = (currentSentenceIndex === 0);
}
function moveToNextSentence() {
  currentSentenceIndex++;

  if (currentSentenceIndex >= sentences.length) {
    console.log("You have finished all the sentences.");
    currentSentenceIndex = sentences.length - 1; // Make sure the index doesn't go beyond the last sentence
    hideButton.disabled = true;
    nextButton.disabled = true;
    finishButton.disabled = true;
     swal("You Finished this road!", {

    title:"Good job!",
    icon:"success",

    buttons: {
    catch: {
      text: "Back to dashboard",
      value: "catch",
    },
      text : "try again",
  },

allowOutsideClick: false
})
.then((value) => {
  switch (value) {
 
    
 
    case "catch":
      window.location.href = "{% url 'dashboard' %}";
      break;
 
    default:

    location.reload();
  }
});  
    return;
  }

  // Reset hiddenWordIndices array and enable the buttons
  hiddenWordIndices = [];
  hideButton.disabled = false;
  nextButton.disabled = false;
  finishButton.disabled = false;

  // Hide the current sentence if it exists
  if (currentSentenceIndex - 1 >= 0) {
    var currentSentence = sentences[currentSentenceIndex - 1];
    currentSentence.style.display = "none";
  }

  // Show the next sentence
  var nextSentence = sentences[currentSentenceIndex];
  nextSentence.style.display = "block";

  // Update the progress bar
  var progressWidth = (currentSentenceIndex / (sentences.length - 1)) * 100;
  progressBar.style.width = progressWidth + "%";
  progressBar.setAttribute("aria-valuenow", progressWidth);

  // Enable/disable the back button based on the current sentence index
  backButton.disabled = (currentSentenceIndex === 0);
}

// Hide all sentences except the first one
for (var i = 1; i < sentences.length; i++) {
  sentences[i].style.display = "none";
}

// Check for an existing localStorage entry and restore the user's progress
restoreUserProgress();
 </script>
  {% endblock %}'''
#getting input

from PIL import Image, ImageDraw, ImageFont


rawname = input('template name(no spaces): ')
imgname = input('Image title(spaces):')
img = Image.open('gradient.jpg')

msg = imgname
font = ImageFont.truetype('Arial.ttf', 170)

# Get text dimensions using ImageFont.getsize
text_width, text_height = font.getsize(msg)

# Get image dimensions
image_width, image_height = img.size

# Create a drawing object
draw = ImageDraw.Draw(img)

# Calculate the starting point for the centered text
x = (image_width - text_width) // 2
y = (image_height - text_height) // 2

# Draw the text at the centered position
draw.text((x, y), msg, font=font, fill=(255, 255, 255))
imgfilename = rawname +'.png'
img.save(imgfilename)
subprocess.run(['cp', imgfilename, '/Users/jadong/roads_bible_vercel/static/'])
print('Press Control-d to exit.')
print('-------> Verse 1')
content1 = sys.stdin.read() 

print('-------> Verse 2')


content2 = sys.stdin.read()

print('-------> Verse 3')
content3= sys.stdin.read()

print('-------> Verse 4')
content4= sys.stdin.read()

print('-------> Verse 5')
content5= sys.stdin.read()

print('-------> Verse 6')

content6= sys.stdin.read()

print('-------> Verse 7')

content7= sys.stdin.read()
print('DONE!!')
name= rawname + ".html"
#adding stuff.
verse1= '<p id="sentence">' + content1 + '</p>'

verse2= '<p id="sentence2">' + content2 + '</p>'

verse3= '<p id="sentence3">' + content3 + '</p>'

verse4= '<p id="sentence4">' + content4 + '</p>'

verse5= '<p id="sentence5">' + content5 + '</p>'

verse6= '<p id="sentence6">' + content6 + '</p>'

verse7= '<p id="sentence7">' + content7 + '</p>'
stuff_to_cat =  default + verse1 + verse2 + verse3 +verse4 +verse5 + verse6 + verse7 +defaultend 

file1 = open(name, "a")
file1.write(stuff_to_cat)
file1.close()
############################################3

def write_string_to_line(file_path, target_string, line_number):
    
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if 1 <= line_number <= len(lines):
            lines[line_number - 1] = target_string + '\n'
        else:
            print(f'Error: Line number {line_number} is out of range.')
            return

        # Use a temporary file to store the modified content
        temp_file_path = file_path + '.tmp'
        with open(temp_file_path, 'w') as temp_file:
            temp_file.writelines(lines)

        # Replace the original file with the temporary one
        shutil.move(temp_file_path, file_path)


urls = '    path("dashboard/' + rawname +'", TemplateView.as_view(template_name="'+name +'"), name=' '"' + rawname+ '"'+'),'
file_path = '/Users/jadong/roads_bible_vercel/road_bible/urls.py'
target_string = urls
line_number = 40
write_string_to_line(file_path, target_string, line_number)
