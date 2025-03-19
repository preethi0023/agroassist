// JavaScript for the marketplace functionality

document.addEventListener('DOMContentLoaded', function() {
    // Price formatting for input fields
    const priceInput = document.getElementById('price');
    if (priceInput) {
        priceInput.addEventListener('blur', function() {
            // Format to 2 decimal places if value exists
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    }
    
    // Category filter behavior
    const categorySelect = document.querySelector('select[name="category"]');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            // If using AJAX filtering, we could handle it here
            // For now, we'll rely on the form submission to filter products
        });
    }
    
    // Search input behavior
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        // Add clear button functionality
        searchInput.addEventListener('input', function() {
            // Show clear button when text is entered
            const clearBtn = this.parentElement.querySelector('.clear-search');
            if (clearBtn) {
                clearBtn.style.display = this.value ? 'block' : 'none';
            }
        });
        
        // Add search suggestions functionality (this would be expanded in a real implementation)
        searchInput.addEventListener('focus', function() {
            console.log('Search input focused - could show recent searches or popular terms');
        });
    }
    
    // Product form validation
    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) {
        addProductForm.addEventListener('submit', function(event) {
            // Basic form validation
            const name = document.getElementById('name').value.trim();
            const price = document.getElementById('price').value;
            const category = document.getElementById('category').value;
            
            let hasError = false;
            
            // Clear any existing error messages
            document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
            document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
            
            // Validate name (minimum length)
            if (name.length < 3) {
                const nameInput = document.getElementById('name');
                nameInput.classList.add('is-invalid');
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback';
                errorDiv.textContent = 'Product name must be at least 3 characters';
                
                nameInput.parentNode.appendChild(errorDiv);
                hasError = true;
            }
            
            // Validate price (must be positive)
            if (price <= 0) {
                const priceInput = document.getElementById('price');
                priceInput.classList.add('is-invalid');
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback';
                errorDiv.textContent = 'Price must be greater than zero';
                
                priceInput.parentNode.appendChild(errorDiv);
                hasError = true;
            }
            
            // Validate category selection
            if (!category) {
                const categoryInput = document.getElementById('category');
                categoryInput.classList.add('is-invalid');
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback';
                errorDiv.textContent = 'Please select a category';
                
                categoryInput.parentNode.appendChild(errorDiv);
                hasError = true;
            }
            
            // Prevent form submission if errors exist
            if (hasError) {
                event.preventDefault();
            }
        });
    }
    
    // Initialize product deletion confirmation
    const deleteButtons = document.querySelectorAll('button[onclick*="return confirm"]');
    deleteButtons.forEach(button => {
        button.onclick = function() {
            return confirm('Are you sure you want to delete this product?');
        };
    });
    
    // Add lazy loading for product images (if applicable)
    document.querySelectorAll('.product-image').forEach(img => {
        img.loading = 'lazy';
    });
});
