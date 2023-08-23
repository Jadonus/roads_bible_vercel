function hideEverythingExceptFirstLetter() {
    var sentences = document.querySelectorAll("p[id^='sentence']");
    for (var i = 0; i < sentences.length; i++) {
        var sentenceText = sentences[i].textContent;
        var firstLetter = sentenceText.charAt(0);

        // Replace the sentence with the first letter
        sentences[i].textContent = firstLetter;
    }
}
function switchToFirstLetterMode() {
    // Hide buttons specific to the random word mode
    document.getElementById("incrementButton").style.display = "none";
    document.getElementById("finishButton").style.display = "none";

    // Call the function to activate First Letter Mode
    hideEverythingExceptFirstLetter();

    // Hide other irrelevant buttons if needed

    // Apply mode-specific behavior
    // ...
}