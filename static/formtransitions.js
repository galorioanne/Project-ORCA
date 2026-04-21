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

            // Wait for the animation to finish (match CSS duration)
            setTimeout(() => {
              window.location.href = targetUrl;
            }, 500);
          }
        });
      });

      const form = document.getElementById('main-form');

      form.addEventListener('submit', function(e) {
          // 1. Prevent immediate submission
          e.preventDefault();

          // 2. Trigger the exit animation (fade out the content area)
          fadeDiv.classList.add('fade-out');

          // 3. Wait for the animation to finish, then submit the form
          setTimeout(() => {
              form.submit();
          }, 500);
      });
    });