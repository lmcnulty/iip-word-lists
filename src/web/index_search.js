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


words.parentNode.insertBefore(searchbar, words);
insertAfter(showSuspiciousCheck, searchbar);
insertAfter(showSuspiciousLabel, showSuspiciousCheck);
insertAfter(document.createElement("br"), searchbar);

let wordList = []
for (let i = 0; i < words.childNodes.length; i++) {
	word = words.childNodes[i];
	wordList.push(word)
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
render();
