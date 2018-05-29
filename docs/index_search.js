function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}
function insertBefore(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode);
}

let wordsPerPage = 60; 
let after = 0;
let words = document.getElementById("words");

let searchbar = document.createElement("input");
searchbar.type = "text";
searchbar.placeholder = "Search for matching words...";

let showSuspiciousCheck = document.createElement("input");
showSuspiciousCheck.type = "checkbox";
showSuspiciousCheck.id = "showSuspiciousCheck"
showSuspiciousCheck.checked = false;
showSuspiciousCheck.addEventListener("click", render, false);
let showSuspiciousLabel = document.createElement("label");
showSuspiciousLabel.for = "showSuspiciousCheck";
showSuspiciousLabel.innerHTML = "Show suspicious words";

let sortSelect = document.createElement("select");
let alphabet = document.createElement("option");
alphabet.value = "alphabet";
alphabet.innerHTML = "Alphabet"
sortSelect.appendChild(alphabet)
let numOccurences = document.createElement("option");
numOccurences.value = "occurences";
numOccurences.innerHTML = "Occurences"
sortSelect.appendChild(numOccurences)
sortSelect.addEventListener("change", () => {
	sortWordList();
	render();
}, false);
sortSelect.id = "sortSelect";
let sortByLabel = document.createElement("label");
sortByLabel.for = "sortSelect";
sortByLabel.innerHTML = "Sort by"

words.parentNode.insertBefore(searchbar, words);
insertAfter(sortByLabel, searchbar);
insertAfter(sortSelect, sortByLabel);

insertAfter(showSuspiciousCheck, sortSelect);
insertAfter(showSuspiciousLabel, showSuspiciousCheck);
insertAfter(document.createElement("br"), searchbar);



let wordList = []

function sortWordList() {
	if (sortSelect.value == "occurences") {
		wordList.sort((a, b) => {
			return b.getAttribute("data-num-occurences") - 
			       a.getAttribute("data-num-occurences");
		});
	} else if (sortSelect.value = "alphabet") {
		wordList.sort((a, b) => {
			return a.children[0].innerHTML.localeCompare(b.children[0].innerHTML);
		});
	}
}
/*
for (let i = 0; i < words.childNodes.length; i++) {
	word = words.childNodes[i];
	wordList.push(word)
}*/

console.log(wordsArray);
for (let i = 0; i < wordsArray.length; i++) {
	let newWord = document.createElement("li");
	let newLink = document.createElement("a");
	newWord.appendChild(newLink);
	newLink.innerHTML = wordsArray[i].text;
	newLink.href = wordsArray[i].text + "_.html";
	newWord.setAttribute("data-num-occurences", wordsArray[i].occurences);
	if (wordsArray[i].suspicious) {
		console.log(wordsArray[i].text + ": suspicious");
		newWord.classList = "suspicious";
	}
	wordList.push(newWord);
}

let prev = document.createElement("button");
let next = document.createElement("button");
prev.innerHTML = "Prev"
next.innerHTML = "Next"
prev.id = "previous-button";
next.id = "next-button";
insertAfter(prev, words);
insertAfter(next, prev);
prev.addEventListener("click", () => {
	after = Math.max(after - wordsPerPage, 0); 
	render();
}, false);
next.addEventListener("click", () => {
	after += wordsPerPage; 
	render();
}, false);

function checkSkip(word) {
	if (!showSuspiciousCheck.checked) {
		if (word.classList.contains("suspicious")) {return true;}
	}
	if (word.children[0].innerHTML.length < 1) {return true;}
	return false;
}

function render() {
	while (words.firstChild) {
		words.removeChild(words.firstChild);
	}
	let added = 0; let seen = 0;
	prev.disabled = true; next.disabled = true;
	
	for (let i = 0; i < wordList.length; i++) {
		if (added == wordsPerPage) {
			next.disabled = false;
			break;
		}
		let word = wordList[i]
		if (checkSkip(word)) {continue;}
		let text = word.children[0].innerHTML.toLowerCase();
		if (text.startsWith(searchbar.value.toLowerCase())) {
			seen += 1;
			if (seen > after) {
				added += 1;
				words.appendChild(word)
			}
		}
	}
	if (after > 0) {
		prev.disabled = false;
	}
}

searchbar.addEventListener("input", () => {after = 0; render();}, false);
sortWordList();
render();
