var sentences = document.querySelectorAll("p[id^='sentence']");
alert("hello");
var currentSentenceIndex = 0;
var hiddenWordIndices = [];
var hideButton = document.getElementById("incrementButton") as HTMLButtonElement;
var nextButton = document.getElementById("nextButton") as HTMLButtonElement;

hideButton.disabled = true;
nextButton.disabled = false;
hideButton.addEventListener('click', function () {
  hideRandomWords(3);
});

nextButton.addEventListener('click', function () {
  moveToNextSentence();
});

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
    return;
  }

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
  nextButton.disabled = false; // Enable the next button after hiding words
}

function moveToNextSentence() {
  if (currentSentenceIndex >= sentences.length - 1) {
    console.log("You have reached the end of the sentences.");
    nextButton.disabled = true;
    return;
  }

  currentSentenceIndex++;

  // Clear the previous sentence
  sentences[currentSentenceIndex - 1].innerHTML = "";

  // Show the next sentence
  var nextSentence = sentences[currentSentenceIndex];
  var sentenceText = nextSentence.textContent;
  nextSentence.innerHTML = '<span>' + sentenceText + '</span>';

  // Reset hiddenWordIndices array and enable the hide button
  hiddenWordIndices = [];
  hideButton.disabled = false;
  hideButton.focus(); // Set focus to the hide button
}
