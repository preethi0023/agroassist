// JavaScript for messaging functionality

document.addEventListener('DOMContentLoaded', function() {
    // Handle expert search
    const expertSearchInput = document.getElementById('expert-search-input');
    const searchExpertBtn = document.getElementById('search-expert-btn');
    const expertSearchResults = document.getElementById('expert-search-results');
    
    if (expertSearchInput && searchExpertBtn && expertSearchResults) {
        // Search button click handler
        searchExpertBtn.addEventListener('click', function() {
            searchExperts(expertSearchInput.value);
        });
        
        // Search input enter key handler
        expertSearchInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                searchExperts(this.value);
            }
        });
        
        // Search for experts function
        function searchExperts(query) {
            if (query.trim() === '') {
                expertSearchResults.innerHTML = '<div class="alert alert-info">Please enter a search term</div>';
                return;
            }
            
            // Show loading indicator
            expertSearchResults.innerHTML = '<div class="text-center py-3"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
            
            // Fetch expert search results from API
            fetch(`/api/search/experts?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length === 0) {
                        expertSearchResults.innerHTML = '<div class="alert alert-info">No experts found matching your search</div>';
                    } else {
                        // Create result items
                        let resultsHtml = '';
                        data.forEach(expert => {
                            resultsHtml += `
                                <a href="/messages/${expert.id}" class="list-group-item list-group-item-action">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <strong>${expert.name}</strong>
                                            <span class="badge bg-info ms-2">Expert</span>
                                        </div>
                                        <button class="btn btn-sm btn-outline-primary">Message</button>
                                    </div>
                                </a>
                            `;
                        });
                        expertSearchResults.innerHTML = resultsHtml;
                    }
                })
                .catch(error => {
                    console.error('Error searching experts:', error);
                    expertSearchResults.innerHTML = '<div class="alert alert-danger">Error searching for experts. Please try again.</div>';
                });
        }
    }
    
    // Handle new message functionality
    const recipientSearch = document.getElementById('recipient-search');
    const searchRecipientBtn = document.getElementById('search-recipient-btn');
    const recipientSearchResults = document.getElementById('recipient-search-results');
    const selectedRecipient = document.getElementById('selected-recipient');
    const recipientName = document.getElementById('recipient-name');
    const recipientId = document.getElementById('recipient-id');
    const clearRecipient = document.getElementById('clear-recipient');
    const sendMessageBtn = document.getElementById('send-message-btn');
    
    if (recipientSearch && searchRecipientBtn && recipientSearchResults && selectedRecipient && 
        recipientName && recipientId && clearRecipient && sendMessageBtn) {
        
        // Search for recipients
        searchRecipientBtn.addEventListener('click', function() {
            searchRecipients(recipientSearch.value);
        });
        
        recipientSearch.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                searchRecipients(this.value);
            }
        });
        
        // Clear selected recipient
        clearRecipient.addEventListener('click', function() {
            selectedRecipient.classList.add('d-none');
            recipientId.value = '';
            recipientSearch.value = '';
            sendMessageBtn.disabled = true;
        });
        
        // Enable/disable send button based on form completion
        const messageContent = document.getElementById('message-content');
        if (messageContent) {
            messageContent.addEventListener('input', checkFormCompletion);
        }
        
        function checkFormCompletion() {
            sendMessageBtn.disabled = recipientId.value === '' || 
                                     (messageContent && messageContent.value.trim() === '');
        }
        
        // Handle send message button
        sendMessageBtn.addEventListener('click', function() {
            if (recipientId.value && messageContent && messageContent.value.trim()) {
                // Create a form and submit it programmatically
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = `/messages/${recipientId.value}`;
                
                // Add content field
                const contentField = document.createElement('input');
                contentField.type = 'hidden';
                contentField.name = 'content';
                contentField.value = messageContent.value;
                form.appendChild(contentField);
                
                // Add to document and submit
                document.body.appendChild(form);
                form.submit();
            }
        });
        
        // Search for recipients function
        function searchRecipients(query) {
            if (query.trim() === '') {
                recipientSearchResults.innerHTML = '<div class="alert alert-info">Please enter a username or name</div>';
                return;
            }
            
            // Show loading indicator
            recipientSearchResults.innerHTML = '<div class="text-center py-3"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
            
            // In a real implementation, this would call an API endpoint
            // For simplicity, we're simulating the behavior with a setTimeout
            setTimeout(() => {
                // Simulate API response
                const mockResults = [
                    { id: 1, name: 'Farmer John', user_type: 'farmer' },
                    { id: 2, name: 'Dr. Smith', user_type: 'expert' },
                    { id: 3, name: 'Jane Doe', user_type: 'farmer' }
                ];
                
                // Filter based on query (in a real implementation, this would be done server-side)
                const filteredResults = mockResults.filter(user => 
                    user.name.toLowerCase().includes(query.toLowerCase())
                );
                
                if (filteredResults.length === 0) {
                    recipientSearchResults.innerHTML = '<div class="alert alert-info">No users found matching your search</div>';
                } else {
                    // Create result items
                    let resultsHtml = '';
                    filteredResults.forEach(user => {
                        resultsHtml += `
                            <a href="#" class="list-group-item list-group-item-action recipient-item" data-id="${user.id}" data-name="${user.name}">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <strong>${user.name}</strong>
                                        <span class="badge bg-${user.user_type === 'expert' ? 'info' : 'success'} ms-2">${user.user_type.charAt(0).toUpperCase() + user.user_type.slice(1)}</span>
                                    </div>
                                    <button class="btn btn-sm btn-outline-primary">Select</button>
                                </div>
                            </a>
                        `;
                    });
                    recipientSearchResults.innerHTML = resultsHtml;
                    
                    // Add click handler to recipient items
                    document.querySelectorAll('.recipient-item').forEach(item => {
                        item.addEventListener('click', function(e) {
                            e.preventDefault();
                            
                            // Set selected recipient
                            const id = this.dataset.id;
                            const name = this.dataset.name;
                            
                            recipientId.value = id;
                            recipientName.textContent = name;
                            selectedRecipient.classList.remove('d-none');
                            recipientSearchResults.innerHTML = '';
                            
                            checkFormCompletion();
                        });
                    });
                }
            }, 500); // Simulate network delay
        }
    }
    
    // Handle active conversation highlighting
    const contactItems = document.querySelectorAll('.contact-item');
    if (contactItems.length > 0) {
        // Get the current URL
        const currentUrl = window.location.href;
        
        // Find and highlight the active conversation
        contactItems.forEach(item => {
            if (currentUrl.includes(item.getAttribute('href'))) {
                item.classList.add('active', 'bg-light');
            }
        });
    }
});
