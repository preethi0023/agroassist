// Image preview functionality for disease identification page

document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('plant_image');
    const imagePreview = document.getElementById('image-preview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            // Check if a file is selected
            if (this.files && this.files[0]) {
                // Check file size
                const maxSize = 5 * 1024 * 1024; // 5MB
                if (this.files[0].size > maxSize) {
                    alert('Error: Image size exceeds 5MB. Please select a smaller image.');
                    this.value = ''; // Clear the input
                    imagePreview.style.display = 'none';
                    return;
                }
                
                // Check file type
                const fileType = this.files[0].type;
                if (fileType !== 'image/jpeg' && fileType !== 'image/png' && fileType !== 'image/jpg') {
                    alert('Error: Please select a JPEG or PNG image.');
                    this.value = ''; // Clear the input
                    imagePreview.style.display = 'none';
                    return;
                }
                
                // Create a FileReader to read the image
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // Set the src attribute of the preview image
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                }
                
                // Read the image file as a data URL
                reader.readAsDataURL(this.files[0]);
            } else {
                // No file selected, hide the preview
                imagePreview.style.display = 'none';
            }
        });
        
        // Add image preview tips
        const previewContainer = imagePreview.parentElement;
        const tipsList = document.createElement('div');
        tipsList.className = 'mt-2 small text-muted';
        tipsList.innerHTML = `
            <p class="mb-1"><i class="fas fa-info-circle me-1"></i> Taking good photos will improve disease identification accuracy:</p>
            <ul class="ps-3 mb-0">
                <li>Ensure the affected area is clearly visible</li>
                <li>Take photos in good lighting conditions</li>
                <li>Include both healthy and diseased parts for comparison</li>
            </ul>
        `;
        
        // Insert tips after the image preview
        previewContainer.appendChild(tipsList);
    }
    
    // Additional functionality to handle plant type selection
    const plantTypeSelect = document.getElementById('plant_type');
    if (plantTypeSelect) {
        plantTypeSelect.addEventListener('change', function() {
            // Get the selected plant type
            const selectedPlant = this.value;
            
            // Optional: You could add plant-specific instructions here
            // For example, showing common diseases for the selected plant
            if (selectedPlant) {
                // This could be expanded to show specific guidance for each plant
                console.log(`Plant type selected: ${selectedPlant}`);
            }
        });
    }
});
