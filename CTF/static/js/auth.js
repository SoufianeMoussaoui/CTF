const navbar = document.querySelector('.navbar');
const navbarToggle = document.querySelector('.navbar-toggle');
const passwordField = document.getElementById('password1');
const passwordConfirmField = document.getElementById('password2');
const strengthBar = document.querySelector('.strength-bar');
const strengthText = document.querySelector('.strength-text');
const requirementItems = document.querySelectorAll('.password-requirements li');

/**
 * Mobile menu toggle functionality
 */
if (navbarToggle) {
  navbarToggle.addEventListener('click', () => {
    navbar.classList.toggle('active');
  });
}


/**
 * Evaluates password strength 
 */

function checkPasswordStrength(password) {
  if (!password) return 0;  
  let strength = 0;

  if (password.length >= 8) {
    strength += 1;
    document.querySelector('[data-requirement="length"]')?.classList.add('met');
  } 
  else 
    document.querySelector('[data-requirement="length"]')?.classList.remove('met');

  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) {
    strength += 1;
    document.querySelector('[data-requirement="uppercase"]')?.classList.add('met');
  } 
  else 
    document.querySelector('[data-requirement="uppercase"]')?.classList.remove('met');
  
  if (/\d/.test(password)) {
    strength += 1;
    document.querySelector('[data-requirement="number"]')?.classList.add('met');
  } 
  else 
    document.querySelector('[data-requirement="number"]')?.classList.remove('met');

  if (/[^A-Za-z0-9]/.test(password)) {
    strength += 1;
    document.querySelector('[data-requirement="special"]')?.classList.add('met');
  } 
  else 
    document.querySelector('[data-requirement="special"]')?.classList.remove('met');
  
  return strength;
}

/**
 * Updates the password strength indicator
 */
function updatePasswordStrength(password) {
  if (!strengthBar || !strengthText) return;
  
  const strength = checkPasswordStrength(password);
  strengthBar.setAttribute('data-strength', strength);

  switch (strength) {
    case 0:
      strengthText.textContent = 'Too weak';
      break;
    case 1:
      strengthText.textContent = 'Weak';
      break;
    case 2:
      strengthText.textContent = 'Medium';
      break;
    case 3:
      strengthText.textContent = 'Good';
      break;
    case 4:
      strengthText.textContent = 'Strong';
      break;
  }
}


/**
 * Check if passwords match (for signup form just for the style)
 */

function checkPasswordsMatch() {
  if (!passwordField || !passwordConfirmField) return;
  
  const password = passwordField.value;
  const passwordConfirm = passwordConfirmField.value;
  if (passwordConfirm.length === 0) return;
  
  if (password === passwordConfirm) 
    passwordConfirmField.style.borderColor = 'var(--success)'; 
  else 
    passwordConfirmField.style.borderColor = 'var(--danger)';
}

/**
 * Initialize code typing animation effect
 */
function initCodeTypingEffect() {
  const codeLines = document.querySelectorAll('.code-line');
  const typingDelay = 50; // milliseconds per character
  
  codeLines.forEach((line, index) => {
    const text = line.textContent;
    line.textContent = '';
    line.style.opacity = '0';
    
    // Show lines with a delay
    setTimeout(() => {
      line.style.opacity = '1';
      let charIndex = 0;
      
      // Skip typing animation for comment and empty lines
      if (line.classList.contains('code-comment') || text.trim() === '') {
        line.textContent = text;
        return;
      }
      
      // Type out text character by character
      const typeInterval = setInterval(() => {
        if (charIndex < text.length) {
          line.textContent += text.charAt(charIndex);
          charIndex++;
        } 
        else 
          clearInterval(typeInterval);
      }, typingDelay);
    }, index * 300);
  });
}

/**
 * Show form validation messages
 */
function showValidationMessage(input, message, isError = true) {
  // Remove any existing validation message
  const existingMessage = input.parentNode.querySelector('.validation-message');
  if (existingMessage) {
    existingMessage.remove();
  }
  
  // Create and add new validation message
  const messageElement = document.createElement('div');
  messageElement.classList.add('validation-message');
  messageElement.classList.add(isError ? 'error' : 'success');
  messageElement.textContent = message;
  
  input.parentNode.insertAdjacentElement('afterend', messageElement);
}


/**
 * Initialize event listeners
 */

function initEventListeners() {
  if (passwordField) {
    passwordField.addEventListener('input', () => {
      updatePasswordStrength(passwordField.value);
    });
  }
  
  // Password confirmation matching
  if (passwordConfirmField)
    passwordConfirmField.addEventListener('input', checkPasswordsMatch);
  
  // Email validation
  const emailField = document.getElementById('email');
  if (emailField) {
    emailField.addEventListener('blur', () => {
      if (emailField.value && !validateEmail(emailField.value)) {
        showValidationMessage(emailField, 'Please enter a valid email address');
      } else if (emailField.value) {
        emailField.parentNode.querySelector('.validation-message')?.remove();
      }
    });
  }
  
  // Username validation
  const usernameField = document.getElementById('username');
  if (usernameField) {
    usernameField.addEventListener('blur', () => {
      if (usernameField.value && usernameField.value.length < 3)
        showValidationMessage(usernameField, 'Username must be at least 3 characters');
      else if (usernameField.value) 
        usernameField.parentNode.querySelector('.validation-message')?.remove();
    });
  }
}

/**
 * Initialize form animations
 */

function initFormAnimations() {
  const formGroups = document.querySelectorAll('.form-group');
  formGroups.forEach((group, index) => {
    group.style.opacity = '0';
    group.style.transform = 'translateY(20px)';
    group.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    
    setTimeout(() => {
      group.style.opacity = '1';
      group.style.transform = 'translateY(0)';
    }, 100 + (index * 100));
  });
}

/**
 * Initialize fake login/registration request simulation
 */
function initFormSubmission() {
  const authForm = document.querySelector('.auth-form');
  if (!authForm) return;
  
  authForm.addEventListener('submit', function(e) {
    if (window.location.href.includes('demo')) {
      e.preventDefault();
      const submitButton = this.querySelector('button[type="submit"]');
      const originalText = submitButton.textContent;
      submitButton.disabled = true;
      submitButton.innerHTML = '<div class="spinner"></div> Processing...';
      
      setTimeout(() => {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
        
        // Show success message - in a real app, this would depend on the response
        const message = document.createElement('div');
        message.classList.add('auth-success');
        message.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <p>Success! Redirecting you...</p>
        `;
        authForm.insertBefore(message, authForm.firstChild);
        
        // Redirect after a short delay
        setTimeout(() => {
          window.location.href = '/dashboard';
        }, 1500);
      }, 2000);
    }
  });
}



/**
 * Initialize everything 
 */

document.addEventListener('DOMContentLoaded', function() {
  initEventListeners();
  initFormAnimations();
  initFormSubmission();
  // Only run the code typing effect on non-mobile devices
  if (window.innerWidth > 767) 
    setTimeout(initCodeTypingEffect, 500);
  else {
      document.querySelectorAll('.code-line').forEach(line => {
      line.style.opacity = '1';
    });
  }
});