
var ls = localStorage.getItem('namespace.visited');
if (ls == null) {
    swal({
    title: "Hey!"
  }) 
    localStorage.setItem('namespace.visited', 1)
}
else {
    swal({
   title: "Hey!",
   text: "Looks like it is your first visit! Here is a quick tour.",
   buttons: ["Cancel", "Start tour"],
  })
.then((willDelete) => {
  if (willDelete) {
    swal( {
          title: "Overview",
          text: "The main place to be is here, the dashboard. Here you can memorize the verse of the day or pick a road to memorize further. Roads are groups of at least five verses. Roads currently has 1 mode, the random hidden words mode. When you click the hide more button, Some words will be hidden. ", 
          buttons: ["Cancel", "Next"]
    })
.then((next) => {
  if (next) {
  console.log("HELLO")
    }
}

const url = "https://beta.ourmanna.com/api/v1/get";

  const xhr = new XMLHttpRequest();
  xhr.open("GET", url);
  xhr.responseType = "text";

  // Show the spinner before making the request
  document.getElementById("mySpinner").style.display = "block";

  xhr.onload = function() {
    if (xhr.status === 200) {
      const text = xhr.responseText;
      document.getElementById("sentence").innerHTML = text;

      // Hide the spinner and show the content once it is loaded
      document.getElementById("mySpinner").style.display = "none";
      document.getElementById("sentence").style.display = "block";
    } else {
      console.log("Error: " + xhr.status);
    }
  };

  xhr.send();
const arrayOfStrings = [
    "Psalm100",
    "romans-road",
    "Psalm23",
    "Psalm95",
    "Verses to live by",
    
  ];
function clearCacheAndReload() {
    
    console.log('Clicked on "Update" link');
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.getRegistrations().then(function (registrations) {
        for (let registration of registrations) {
          registration.unregister();
        }
        window.location.reload();
      }).catch(function (error) {
        console.error('Error clearing service worker cache:', error);
      });
    }
  }

function revealAllWords() {
  var currentSentence = sentence;
  var words = currentSentence.getElementsByTagName("span");

  for (var i = 0; i < words.length; i++) {
    words[i].classList.remove("hide-word");
  }

  incrementButton.disabled = false;
}
  function searchArray() {
    const searchInput = document.getElementById("searchInput").value.toLowerCase();
    const searchResults = [];

    for (let i = 0; i < arrayOfStrings.length; i++) {
      if (arrayOfStrings[i].toLowerCase().includes(searchInput)) {
        searchResults.push(arrayOfStrings[i]);
      }
    }

    const resultContainer = document.getElementById("searchResults");
    resultContainer.innerHTML = "";

    if (searchResults.length > 0) {
      for (let i = 0; i < searchResults.length; i++) {
        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.href = "#" + searchResults[i];
        link.textContent = searchResults[i];
    'whitenoise.middleware.WhiteNoiseMiddleware',
        listItem.appendChild(link);
        resultContainer.appendChild(listItem);
      }
    } else {
      const noResultsItem = document.createElement("li");
      noResultsItem.textContent = "No results found.";
      resultContainer.appendChild(noResultsItem);
    }
  }

  function activateTopItem() {
    const topItem = document.querySelector("#searchResults li:first-child a");
    if (topItem) {
      window.location.hash = topItem.getAttribute("href");
    }
  }

  document.getElementById("searchInput").addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      activateTopItem();
    } else {
      searchArray();
    }
  });var hiddenWordIndices = [];
function hideRandomWords(numWords) {
  var sentence = document.getElementById("sentence");

  var sentenceText = sentence.textContent;

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
  sentence.innerHTML = words.join(" ");

  console.log("Total Hidden Words: " + hiddenWordIndices.length);

  if (hiddenWordIndices.length === words.length) {
    document.getElementById("incrementButton").disabled = true;
  }
}
function handleButtonClick() {
  hideRandomWords(3);
}

var button = document.getElementById("incrementButton");
button.addEventListener("click", handleButtonClick);

function handleFinishButtonClick() {
  hideRandomWords(Number.MAX_SAFE_INTEGER);
}

var finishButton = document.getElementById("finishButton");
var clickCounter = 0;
var isHidden = false;

// Remove the extra closing brace on line 287
finishButton.addEventListener('click', function () {
  if (!isHidden) {
    hideRandomWords(Number.MAX_SAFE_INTEGER);
    isHidden = true;
    hideButton.disabled = true;
  } else {
    swal({
      title: "Are you sure?",
      text: "You are about to unhide all the words. Are you sure you want to do this?",
      icon: "info",
      buttons: ["Cancel", "Yes"],
      closeOnClickOutside: false,
    }).then(function (result) {
      if (result) {
        revealAllWords();
        hiddenWordIndices = []; // Clear the index cache
        isHidden = false;
        hideButton.disabled = false;
      }
    });
  }
}, true);

function isIOS() {
  // Get the user agent string.
  var userAgent = navigator.userAgent;

  // Check if the user agent contains any of the following strings.
  var isIOS = /iPad|iPhone|iPod/.test(userAgent);

  // Return true if the user is on iOS, false otherwise.
  return isIOS;
}
  function showToast() {
      // Get the toast element.
      var toast = document.getElementById('toast');
      
      
      toast.classList.replace('byebye','show');
      // Show the toast.
    }
function isPWA() {
  // Get the user agent string.

  if (window.matchMedia('(display-mode: standalone)').matches) {  

     return isPWA;
  }
}
// Check if the user is on iOS and not on the PWA.
if (isIOS() && !isPWA()) {
  showToast();
}
