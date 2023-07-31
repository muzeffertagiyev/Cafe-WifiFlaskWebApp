// Function to add "active" class to the appropriate link
function setActiveLink() {
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
      const linkUrl = link.getAttribute('href');
      if (currentLocation === linkUrl) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }

  // Call the function to set the active link initially
  setActiveLink();


