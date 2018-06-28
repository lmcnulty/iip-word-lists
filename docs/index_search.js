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

let controlsBar = create("div", {id: "controlsBar"}, [
	create("input", {
		type: "text", 
		placeholder: "Search for matching words...",
		id: "searchBar"
	}),
	//create("br"),
	create("label", "Region", {id: "regionLabel", for: "regionSelect"}),
	create("div", {class: "select-wrapper"}, [
		create("select", {id: "regionSelect"}, [
			create("option", "All", {value: "all"})
		]),
	]),
	create("label", "Sort by", {id: "sortByLabel", for: "sortSelect"}),
	create("div", {class: "select-wrapper"}, [
		create("select", {id: "sortSelect"}, [
			create("option", "Occurences", {value: "occurences"}),
			create("option", "Alphabet", {value: "alphabet"})
		])
	]),
	create("input", {
		type: "checkbox", 
		id: "showSuspiciousCheck"
	}),
	create("label", "Show suspicious words", {
		id: "showSuspiciousLabel", for: "showSuspiciousCheck"
	}),
]);

// Add created elements to document
let words = document.getElementById("words");
words.parentNode.insertBefore(controlsBar, words);

// Create a searchbar
let searchbar = document.getElementById("searchBar");

// Create checkbox for toggling visibility of suspicious words
let showSuspiciousCheck = document.getElementById("showSuspiciousCheck");
showSuspiciousCheck.addEventListener("click", render, false);
let showSuspiciousLabel = document.getElementById("showSuspiciousLabel");

// Create a <select> for choosing sort method
let sortSelect = document.getElementById("sortSelect");
sortSelect.addEventListener("change", () => {
	sortWordList();
	render();
}, false);

let sortByLabel = document.getElementById("sortByLabel");



/*
insertAfter(sortByLabel, searchbar);
insertAfter(sortSelect, sortByLabel);
insertAfter(showSuspiciousCheck, sortSelect);
insertAfter(showSuspiciousLabel, showSuspiciousCheck);
insertAfter(document.createElement("br"), searchbar);
*/

// Global Variables
let wordsPerPage = 60; 
let after = 0;
let wordList = []
let regionsSet = new Set();

function sortWordList() {
	after = 0;
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

let regionSelect = document.getElementById("regionSelect");
let regionLabel = document.getElementById("regionLabel");
for (var i of regionsSet) {
	regionSelect.appendChild(create("option", i, {value: i}));
}
//insertBefore(regionSelect, sortByLabel);
//insertBefore(regionLabel, regionSelect);

regionSelect.addEventListener("change", () => {
	render();
}, false);

let prev = document.createElement("button");
let next = document.createElement("button");
prev.innerHTML = "PREV"
next.innerHTML = "NEXT"
prev.id = "previous-button";
next.id = "next-button";

let alphabetSelect = create("div", {id: "alphabet-select"});

let bottomControls = create("div", {id: "bottomControls"}, [
	alphabetSelect, prev, next
]);

insertAfter(bottomControls, words);
//insertAfter(prev, words);
//insertAfter(next, prev);


function jumpToLetter(evt) {
	sortSelect.value = "alphabet";
	sortWordList();
	for (let i = 0; i < wordList.length - wordsPerPage; i += wordsPerPage) {
		if (wordList[i].children[0].innerHTML[0]
		    < evt.target.innerHTML[0]
		) {
			after = i;
		}
	}
	render();
}

let letters = new Set();
for (let i = 0; i < wordList.length; i++) {
	letters.add(wordList[i].children[0].innerHTML[0]);
}
sortedLetters = Array.from(letters).sort();
for (let i = 0; i < sortedLetters.length; i++) {
	let link = create("a", "" + sortedLetters[i]);
	link.addEventListener("click", jumpToLetter, false);
	alphabetSelect.appendChild(link);
}

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

let lastRender = 0;

let standardSort = true;
function render() {
	//let timeDif = Date.now() - lastRender;
	//if (timeDif < 500) {setTimeout(render, 500 - timeDif); return;}
	//lastRender = Date.now();
	while (words.firstChild) {
		words.removeChild(words.firstChild);
	}
	let re = new RegExp(searchbar.value);
	if (searchbar.value != "") {
		standardSort = false;
		wordList.sort((a, b) => {
			a.text = a.children[0].innerHTML;
			b.text = b.children[0].innerHTML;	
			a.regexMatch = false;
			b.regexMatch = false;		
			if (a.text.match(re) != null) {
				a.regexMatch = true; 
			}
			if (b.text.match(re) != null) { b.regexMatch = true; }
			a.levEdit = Levenshtein.get(a.text, searchbar.value);
			b.levEdit = Levenshtein.get(b.text, searchbar.value)
			if (a.regexMatch && !b.regexMatch) { return -1;}
			if (b.regexMatch && !a.regexMatch) { return 1;}
			
			return a.levEdit - b.levEdit;
		});
	} else {
		if (!standardSort) {
			sortWordList();
			standardSort = true;
		}
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
		let searchText = searchbar.value.toLowerCase();
		if (text.startsWith(searchText) || 
		    wordList[i].levEdit < 4 ||
		    wordList[i].regexMatch) {
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
