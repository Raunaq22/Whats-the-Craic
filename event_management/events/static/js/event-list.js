

// Function to handle messages for selected filter
function messageselectedfilter(countySelect){
    var countyMessage = document.getElementById('county-message');
        countySelect.addEventListener('change', function() {
            countyMessage.textContent = "In search of activities in " + this.value + "? We offer a ton of fantastic events and information, regardless of whether you're a native, new in town, or just passing through. You can search by area, popular items, our best recommendations, freebies, and more. You can do this. All set?";
        });
}

// Call the function with the select element
messageselectedfilter(document.getElementById('county-filter'));
