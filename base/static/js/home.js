document.addEventListener('DOMContentLoaded', function() {
  // Automatically close the success message after 2 seconds
  setTimeout(function() {
    var successMessage = document.getElementById('successMessage');
    if (successMessage) {
      successMessage.style.display = 'none';
    }
  }, 2000);

  // Initialize a variable to track image processing status
  let isImageProcessingComplete = false;

  // Attach the click event listener to the 'Process Images' button
  document.getElementById('processImages').addEventListener('click', function() {
    // Trigger the image processing on button click
    fetch('/process_images/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
      },
      body: JSON.stringify({}),
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Set image processing status to true
        isImageProcessingComplete = true;

       
        // Display success message
        var successMessage = document.getElementById('successMessage');
        if (successMessage) {
          successMessage.innerHTML = 'Images processed successfully!';
          successMessage.className = 'alert alert-success fade show';
          successMessage.style.display = 'block';

          // Close the success message after 2 seconds with fade-out effect
          setTimeout(function() {
            successMessage.style.opacity = 0;
            setTimeout(function() {
              successMessage.style.display = 'none';
            }, 1000); // Adjusted the fade-out duration for image processing completion
          }, 2000);
        }
      } else {
        alert('Error processing images: ' + data.error);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while processing images.');
    });
  });

  // Attach the click event listener to the 'View Cleaned JSON' button
  document.getElementById('viewJsonButton').addEventListener('click', function() {
    // Redirect to the view_cleaned_json page only if image processing is complete
    if (isImageProcessingComplete) {
      // Check if JSON files are stored in the "json" folder
      fetch('/check_json_files/')
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            window.location.href = '/view_cleaned_json/';
          } else {
            alert('No JSON files found. Please process images first.');
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    } else {
      alert('Please process images first.');
    }
  });

  // Fade out the "Image Uploaded Completed" message after 2 seconds
  setTimeout(function() {
    var uploadSuccessMessage = document.getElementById('uploadSuccessMessage');
    if (uploadSuccessMessage) {
      uploadSuccessMessage.style.opacity = 0;
      setTimeout(function() {
        uploadSuccessMessage.style.display = 'none';
      }, 1000); // Adjusted the fade-out duration for image upload completion
    }
  }, 2000);
});
