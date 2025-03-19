// Main JavaScript for Agro Assist application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Check for unread messages for authenticated users
    if (document.getElementById('unread-count')) {
        fetchUnreadMessageCount();
        // Check every 30 seconds for new messages
        setInterval(fetchUnreadMessageCount, 30000);
    }
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Activate tab based on hash URL if present
    const url = document.location.toString();
    if (url.includes('#')) {
        const tabId = url.split('#')[1];
        const tab = document.querySelector(`a[href="#${tabId}"]`);
        if (tab) {
            new bootstrap.Tab(tab).show();
        }
    }
    
    // Handle form validations
    validateForms();
});

// Fetch unread message count and update badge
function fetchUnreadMessageCount() {
    fetch('/api/messages/unread')
        .then(response => response.json())
        .then(data => {
            const unreadBadge = document.getElementById('unread-count');
            if (data.count > 0) {
                unreadBadge.textContent = data.count;
                unreadBadge.classList.remove('d-none');
            } else {
                unreadBadge.classList.add('d-none');
            }
        })
        .catch(error => console.error('Error fetching unread messages:', error));
}

// Add custom form validations
function validateForms() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Utility function to format numbers with commas as thousands separators
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Function to show alert messages
function showAlert(message, type = 'info') {
    const alertPlaceholder = document.getElementById('alert-placeholder');
    if (!alertPlaceholder) return;
    
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    alertPlaceholder.append(wrapper);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = bootstrap.Alert.getInstance(wrapper.querySelector('.alert'));
        if (alert) {
            alert.close();
        }
    }, 5000);
}

// Handle confirmation dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}
