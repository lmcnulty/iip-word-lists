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
words.parentNode.insertBefore(searchbar, words);

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

function render() {
	while (words.firstChild) {
		words.removeChild(words.firstChild);
	}
	let added = 0;
	let seen = 0;
	prev.disabled = true; next.disabled = true;
	for (let i = 0; i < wordList.length; i++) {
		if (added > wordsPerPage - 1) {
			next.disabled = false;
			break;
		}
		let word = wordList[i]
		let text = word.children[0].innerHTML.toLowerCase();
		if (text.startsWith(searchbar.value.toLowerCase())) {
			seen += 1;
			if (seen > after && word.children[0].innerHTML.length > 1) {
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
