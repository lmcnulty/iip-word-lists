// Utility Functions
function create(elementType) {
	let newElement = document.createElement(elementType);
	for (let i = 1; i < arguments.length; i++) {
		let currentArgument = arguments[i];		
		if (typeof(currentArgument) === 'string') {
			newElement.innerHTML += currentArgument;
		} else if (Array.isArray(currentArgument)) {
			for (let j = 0; j < arguments[i].length; j++) {
				if (typeof(arguments[i][j]) === 'string') {
					newElement.innerHTML += currentArgument[j];		
				} else {	
					newElement.appendChild(currentArgument[j]);
				}
			}
		} else if (currentArgument instanceof Element) {
			newElement.appendChild(currentArgument);
		} else {
			Object.getOwnPropertyNames(currentArgument).forEach(
				function (val, idx, array) {
					newElement.setAttribute(val, currentArgument[val]);
				}
			);
		}
	}
	return newElement;
}
function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}
function insertBefore(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode);
}

// Create a searchbar
let searchbar = create("input", {
	type: "text", 
	placeholder: "Search for matching words..."
})

// Create checkbox for toggling visibility of suspicious words
let showSuspiciousCheck = create("input", {
	type: "checkbox", 
	id: "showSuspiciousCheck"
});
showSuspiciousCheck.addEventListener("click", render, false);
let showSuspiciousLabel = create("label", "Show suspicious words", 
                                 {for: showSuspiciousCheck});

// Create a <select> for choosing sort method
let sortSelect = create("select", {id: "sortSelect"}, [
	create("option", "Alphabet", {value: "alphabet"}),
	create("option", "Occurences", {value: "occurences"})
]);
sortSelect.addEventListener("change", () => {
	sortWordList();
	render();
}, false);
let sortByLabel = create("label", "Sort by", {for: "sortSelect"});

// Add created elements to document
let words = document.getElementById("words");
words.parentNode.insertBefore(searchbar, words);
insertAfter(sortByLabel, searchbar);
insertAfter(sortSelect, sortByLabel);
insertAfter(showSuspiciousCheck, sortSelect);
insertAfter(showSuspiciousLabel, showSuspiciousCheck);
insertAfter(document.createElement("br"), searchbar);

// Global Variables
let wordsPerPage = 60; 
let after = 0;
let wordList = []
let regionsSet = new Set();

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

for (let i = 0; i < wordsArray.length; i++) {
	if (wordsArray[i].regions != null) {
		for (let j = 0; j < wordsArray[i].regions.length; j++) {
			regionsSet.add(wordsArray[i].regions[j]);
		}
	}
	let newWord = create("li", 
		{"data-num-occurences": wordsArray[i].occurences, 
		 "data-regions": wordsArray[i].regions},
		[create("a", wordsArray[i].text, 
		        {href: wordsArray[i].text + "_.html"})]
	);
	if (wordsArray[i].suspicious) { newWord.classList = "suspicious"; }
	wordList.push(newWord);
}

let regionSelect = create("select", {id: "regionSelect"}, create("option", "All", {value: "all"}));
let regionLabel = create("label", "Region", {for: "regionSelect"});
for (var i of regionsSet) {
	regionSelect.appendChild(create("option", i, {value: i}));
}
insertBefore(regionSelect, sortByLabel);
insertBefore(regionLabel, regionSelect);

regionSelect.addEventListener("change", () => {
	render();
}, false);

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
	if (regionSelect.value != "all") {
		if (word.getAttribute("data-regions").indexOf(regionSelect.value) == -1) {
			return true;
		}
	}
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
