import sys
import shutil
default='''
{% extends 'base.html' %}

{% block content %}

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
<script src=
"https://cdnjs.cloudflare.com/ajax/libs/sweetalert/2.1.0/sweetalert.min.js">
</script>
<nav class="navbar navbar-expand-sm">
  <div class="container-fluid">
    <a class=" link-text display-5" style="color: #adb5b1" href ="{% url "dashboard" %}"><i class="bi bi-caret-left-fill "></i></a>
  
    <span class="navbar-text"><i class="bi bi-book-fill display-6" style="color: #adb5b1"></i></span>
  </div>
</nav>
<div class="text-center card mx-auto p-1 " style="width:80vw; background-color: #343A40; border-color:  #343A40; font-size: 24px">
<div class="card-body">
'''

defaultend='''
</div>
</div>
<div class="mx-auto text-center p-5">
<button id="incrementButton" class="btn btn-primary mb-2">Hide More</button>
<button id="finishButton" class="btn btn-primary mb-2">Finish Verse</button>

<button id="nextButton" class="btn btn-primary mb-2">Next Verse</button>

</div>
<div class="progress-container">
<div class="progress">
  <div id="progressBar" class="progress-bar lrm-5" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
</div>
</div>
</div>
<style>
nav{
  margin:0;
}
.hide-word {
         
        color: transparent;
        text-shadow: 0 0 13px #000;
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
  margin: 0 auto; /* Center the container on the screen */
}
</style>
<script>

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
}, true);

var finishButtonClicks = 0; // Variable to track the number of finish button clicks

finishButton.addEventListener('click', function () {
  finishButtonClicks++;
  if (finishButtonClicks === 1) {
    hideAllWords();
  } else if (finishButtonClicks === 2) {
    revealAllWords();
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
    swal({
  title: "Good job!",
  text: "You Finished this road!",
  icon: "success",
});
    finishButton.disabled = true;
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
}</script>
{% endblock %}
'''
#getting input
rawname = input('template name: ')
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
print('DONE!!')
name= rawname + ".html"
#adding stuff.
verse1= '<p id="sentence">' + content1 + '</p>'

verse2= '<p id="sentence2">' + content2 + '</p>'

verse3= '<p id="sentence3">' + content3 + '</p>'

verse4= '<p id="sentence4">' + content4 + '</p>'

verse5= '<p id="sentence5">' + content5 + '</p>'
stuff_to_cat =  default + verse1 + verse2 + verse3 +verse4 +verse5 + defaultend 

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
file_path = '/home/jadong/roads_bible_vercel/road_bible/urls.py'
target_string = urls
line_number = 40
write_string_to_line(file_path, target_string, line_number)
