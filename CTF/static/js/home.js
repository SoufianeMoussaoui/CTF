document.addEventListener('DOMContentLoaded', function() {
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    const navbarAuth = document.querySelector('.navbar-auth');
    
    if (navbarToggle) {
      navbarToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        if (navbarMenu) navbarMenu.classList.toggle('active');
        if (navbarAuth) navbarAuth.classList.toggle('active');
      });
    }
    const navbar = document.querySelector('.navbar'); 
    if (navbar) {
      window.addEventListener('scroll', function() {
        if (window.scrollY > 50) 
          navbar.classList.add('scrolled');
        else 
          navbar.classList.remove('scrolled');
        
      });
    }

    const codeLines = document.querySelectorAll('.code-line');
    const codeBody = document.querySelector('.code-body');
    if (codeBody && codeLines.length > 0) {
      codeLines.forEach((line, index) => {
        if (!line.classList.contains('code-cursor')) {
          line.style.display = 'none';
        }
      });

      let currentLine = 0;
      function showNextLine() {
        if (currentLine < codeLines.length - 1) {
          const line = codeLines[currentLine];
          line.style.display = 'block';
          if (line.querySelector('.code-command')) {
            const command = line.querySelector('.code-command');
            const originalText = command.textContent;
            command.textContent = '';
            
            let charIndex = 0;
            const typingInterval = setInterval(() => {
              if (charIndex < originalText.length) {
                command.textContent += originalText.charAt(charIndex);
                charIndex++;
              } else {
                clearInterval(typingInterval);
                setTimeout(() => {
                  currentLine++;
                  showNextLine();
                }, 5000);
              }
            }, 50);
          } else {
            // If it's not a command, show it after a delay
            setTimeout(() => {
              currentLine++;
              showNextLine();
            }, 1000);
          }
        }
      }
      
      // Start the animation after a short delay
      setTimeout(showNextLine, 1000);
    }
    
    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
      newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const emailInput = this.querySelector('input[type="email"]');
        const email = emailInput.value.trim();
        
        if (email) {
          alert('Thank you for subscribing to our newsletter!'); // just for test
          emailInput.value = '';
        }
      });
    }
  });