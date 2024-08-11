document.addEventListener("DOMContentLoaded", function() {
    initializeLists();
    updateLog();

    // Lore Button Setup
    const loreButton = document.getElementById('loreButton');
    chrome.storage.local.get('lore', (result) => {
        loreButton.textContent = `Lore (${result.lore || 0})`;
    });

    loreButton.addEventListener('click', function() {
        incrementLore();
        updateLoreDisplay();
    });

    loreButton.addEventListener('contextmenu', function(event) {
        event.preventDefault();
        decrementLore();
        updateLoreDisplay();
    });

    // Populate file dropdown with files from the "decklists" folder
    const dropdown = document.getElementById('fileDropdown');
    const decklistsFolder = chrome.runtime.getURL('decklists/');

    // Since fetching the directory directly won't work as expected, you need to manually list files
    const files = ['deck1.txt', 'deck2.txt'];  // Replace with actual file names
    files.forEach(file => {
        const option = document.createElement('option');
        option.value = chrome.runtime.getURL('decklists/' + file);
        option.textContent = file;
        dropdown.appendChild(option);
    });

    dropdown.addEventListener('change', function() {
        const selectedFile = this.value;
        if (selectedFile) {
            resetAll();
            fetch(selectedFile)
                .then(response => response.text())
                .then(content => {
                    document.querySelector('textarea[name="user_input"]').value = content;
                });
        }
    });
});

function initializeLists() {
    chrome.storage.local.get(['deck', 'hand', 'board', 'discard', 'ink'], function(result) {
        populateList('deckList', result.deck || []);
        populateList('handList', result.hand || []);
        populateList('boardList', result.board || []);
        populateList('discardList', result.discard || []);
        populateList('inkList', result.ink || []);
    });
}

function populateList(listId, items) {
    const listElement = document.getElementById(listId);
    listElement.innerHTML = ''; // Clear previous items

    if (Array.isArray(items)) {
        items.forEach(item => {
            const listItem = document.createElement('div');
            listItem.textContent = item.name; // Customize this to your needs
            listElement.appendChild(listItem);
        });
    } else {
        console.error(`Expected an array for ${listId}, but got:`, items);
    }
}

function updateLog() {
    chrome.storage.local.get('log', (result) => {
        const logTextArea = document.getElementById('logTextArea');
        logTextArea.value = result.log || '';

        // Move the cursor to the end
        logTextArea.scrollTop = logTextArea.scrollHeight;
        logTextArea.setSelectionRange(logTextArea.value.length, logTextArea.value.length);
    });
}

function updateLoreDisplay() {
    chrome.storage.local.get('lore', (result) => {
        document.getElementById('loreButton').textContent = `Lore (${result.lore || 0})`;
    });
}

function incrementLore() {
    chrome.storage.local.get('lore', (result) => {
        let lore = (result.lore || 0) + 1;
        chrome.storage.local.set({ lore: lore }, () => updateLoreDisplay());
    });
}

function decrementLore() {
    chrome.storage.local.get('lore', (result) => {
        let lore = Math.max((result.lore || 0) - 1, 0);
        chrome.storage.local.set({ lore: lore }, () => updateLoreDisplay());
    });
}
