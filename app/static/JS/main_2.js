// Select the button, form, and overlay
const contactButton = document.getElementById('contactUsButton');
const contactForm = document.getElementById('contact-us');
const overlay = document.getElementById('overlay');
const closeButton = document.getElementById('closeForm');

// Add event listener to the "Contact Us" button
contactButton.addEventListener('click', function() {
    contactForm.style.display = 'flex';  // Show the contact form
    overlay.style.display = 'block';     // Show the overlay
});

// Add event listener to the "Close" button
closeButton.addEventListener('click', function() {
    contactForm.style.display = 'none';  // Hide the contact form
    overlay.style.display = 'none';      // Hide the overlay
});

document.getElementById('contactForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    const form = event.target;
    const formData = new FormData(form);
    const flashMessageContainer = document.getElementById('flashMessageContainer');
    const contactForm = document.getElementById('contact-us');
    const overlay = document.getElementById('overlay');

    fetch('/contact-us/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Clear any existing messages
        flashMessageContainer.innerHTML = '';

        // Create a new Bootstrap alert
        const alertType = data.status === 'success' ? 'alert-success' : 'alert-danger';
        const alertMessage = `
            <div class="alert ${alertType} alert-dismissible fade show" role="alert">
                ${data.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        flashMessageContainer.innerHTML = alertMessage;

        if (data.status === 'success') {
            form.reset(); // Clear the form fields
            setTimeout(() => {
                contactForm.style.display = 'none';  // Hide the contact form
                overlay.style.display = 'none';      // Hide the overlay
            }, 3000); // Close the form after 3 seconds
        }
    })
    .catch(error => {
        // Clear any existing messages
        flashMessageContainer.innerHTML = '';

        // Create a new Bootstrap alert for errors
        const alertMessage = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                An error occurred. Please try again.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        flashMessageContainer.innerHTML = alertMessage;
    });
});
