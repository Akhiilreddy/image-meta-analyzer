document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.querySelector('form');
    const fileInput = document.querySelector('input[type="file"]');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const fileSize = file.size / 1024 / 1024; // Convert to MB
                if (fileSize > 16) {
                    alert('File size must be less than 16MB');
                    this.value = '';
                }
            }
        });
    }
});
