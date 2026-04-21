    document.addEventListener("DOMContentLoaded", () => {
      const fadeDiv = document.getElementById('content-area');
      const links = document.querySelectorAll('a');
      

      

      links.forEach(link => {
        link.addEventListener('click', (e) => {
          // Only apply to internal links
          if (link.hostname === window.location.hostname) {
            e.preventDefault();
            const targetUrl = link.href;

            // Add the fade-out class
            fadeDiv.classList.add('fade-out');
            
            const activeelemnt = document.getElementById("active");
    if (activeelemnt) {
      activeelemnt.classList.add('caro-navbar-inactive')
    }


            // Wait for the animation to finish (match CSS duration)
            setTimeout(() => {
              window.location.href = targetUrl;
            }, 500);
          }
        });
      });
    });