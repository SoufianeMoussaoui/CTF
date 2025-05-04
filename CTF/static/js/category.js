document.addEventListener('DOMContentLoaded', function() {
  // Modal elements
  const modal = document.getElementById('challenge-modal');
  const modalClose = document.querySelector('.modal-close');
  const modalTitle = document.getElementById('modal-title');
  const modalDifficulty = document.getElementById('modal-difficulty');
  const modalPoints = document.getElementById('modal-points');
  const modalSolves = document.getElementById('modal-solves');
  const modalDescription = document.getElementById('modal-description');
  const modalFiles = document.getElementById('modal-files');
  const modalHints = document.getElementById('modal-hints');
  const modalMessages = document.getElementById('modal-messages');
  const flagForm = document.getElementById('flag-form');
  const submissionArea = document.getElementById('submission-area');
  
  // Current challenge ID
  let currentChallengeId = null;
  
  // Filter functionality
  const difficultyFilter = document.getElementById('difficulty');
  const statusFilter = document.getElementById('status');
  const sortFilter = document.getElementById('sort'); // This is now the category filter
  const searchInput = document.getElementById('search');
  const challengeCards = document.querySelectorAll('.challenge-card');
  
  // Apply filters when changed - with null checks
  if (difficultyFilter) difficultyFilter.addEventListener('change', applyFilters);
  if (statusFilter) statusFilter.addEventListener('change', applyFilters);
  if (sortFilter) sortFilter.addEventListener('change', applyFilters);
  
  // Apply filters on search input
  if (searchInput) searchInput.addEventListener('input', applyFilters);
  
  function applyFilters() {
      const difficulty = difficultyFilter ? difficultyFilter.value : 'all';
      const status = statusFilter ? statusFilter.value : 'all';
      const category = sortFilter ? sortFilter.value : 'all';
      const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
      
      // Filter challenges
      challengeCards.forEach(card => {
          const cardDifficulty = card.dataset.difficulty;
          const cardStatus = card.dataset.status;
          const cardCategory = card.dataset.category; 
          
          // Add null checks for these elements
          const cardTitle = card.querySelector('.challenge-title')?.textContent.toLowerCase() || '';
          const cardDescription = card.querySelector('.challenge-description')?.textContent.toLowerCase() || '';
          
          let difficultyMatch = difficulty === 'all' || cardDifficulty === difficulty;
          let categoryMatch = category === 'all' || cardCategory === category;
          let statusMatch = status === 'all' || cardStatus === status;
          let searchMatch = cardTitle.includes(searchTerm) || cardDescription.includes(searchTerm);
          
          if (difficultyMatch && statusMatch && categoryMatch && searchMatch) {
              card.style.display = 'block';
          } else {
              card.style.display = 'none';
          }
      });
  }
  
  // Challenge card click handler
  document.addEventListener('click', function(e) {
      const challengeLink = e.target.closest('.challenge-link');
      if (challengeLink) {
          e.preventDefault();
          const challengeId = challengeLink.dataset.id;   
          if (challengeId) loadChallengeDetails(challengeId);
      }
  });
  
  // Close modal when clicking the close button
  if (modalClose && modal) {
      modalClose.addEventListener('click', function() {
          modal.style.display = 'none';
      });
  }
  
  // Close modal when clicking outside the modal content
  window.addEventListener('click', function(event) {
      if (event.target === modal) {
          modal.style.display = 'none';
      }
  });
  
  // Flag submission
  if (flagForm) {
      flagForm.addEventListener('submit', function(e) {
          e.preventDefault();
          if (!currentChallengeId) return;
          
          const flagInput = document.getElementById('flag-input');
          if (flagInput) {
              const flag = flagInput.value.trim();
              submitFlag(currentChallengeId, flag);
          }
      });
  }
  
  // Hint toggle functionality
  document.addEventListener('click', function(e) {
      const hintHeader = e.target.closest('.hint-header');
      if (hintHeader) {
          const hintItem = hintHeader.closest('.hint-item');
          if (hintItem) {
              const hintContent = hintItem.querySelector('.hint-content');
              if (hintContent) {
                  hintContent.classList.toggle('active');
              }
          }
      }
      
      // Handle hint unlock button clicks
      const unlockButton = e.target.closest('.unlock-hint-btn');
      if (unlockButton) {
          const hintId = unlockButton.dataset.hintId;
          if (hintId) {
              unlockHint(hintId);
          }
      }
  });
  
  // Load challenge details via AJAX
  function loadChallengeDetails(challengeId) {
      currentChallengeId = challengeId;
      
      // Clear previous content
      if (modalMessages) modalMessages.innerHTML = '';
      if (modalFiles) modalFiles.innerHTML = '';
      if (modalHints) modalHints.innerHTML = '';
      
      // Show loading state
      if (modalTitle) modalTitle.textContent = 'Loading...';
      if (modalDescription) modalDescription.textContent = 'Loading challenge details...';
      if (modal) modal.style.display = 'block';
      
      // Get CSRF token
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
      
      // Fetch challenge details
      fetch(`/api/challenges/${challengeId}/`, {
          headers: {
              'X-CSRFToken': csrftoken,
              'X-Requested-With': 'XMLHttpRequest'
          }
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          // Update modal with challenge data
          if (modalTitle) modalTitle.textContent = data.title;
          if (modalDifficulty) {
              modalDifficulty.textContent = data.difficulty.charAt(0).toUpperCase() + data.difficulty.slice(1);
              modalDifficulty.className = 'value ' + data.difficulty;
          }
          if (modalPoints) modalPoints.textContent = data.points;
          if (modalSolves) modalSolves.textContent = data.solves;
          if (modalDescription) modalDescription.textContent = data.description;
          
          // Update submission area based on solved status
          if (submissionArea) {
              if (data.solved) {
                  submissionArea.innerHTML = `
                      <div class="solved-message">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                              <polyline points="22 4 12 14.01 9 11.01"></polyline>
                          </svg>
                          <span>You've already solved this challenge!</span>
                      </div>
                  `;
              } else {
                  submissionArea.innerHTML = `
                      <form id="flag-form" class="flag-form">
                          <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                          <input type="text" id="flag-input" placeholder="Enter flag (e.g., CTF{flag_here})" required>
                          <button type="submit" class="btn btn-primary">Submit</button>
                      </form>
                  `;
                  
                  // Re-attach event listener to the new form
                  const newFlagForm = document.getElementById('flag-form');
                  if (newFlagForm) {
                      newFlagForm.addEventListener('submit', function(e) {
                          e.preventDefault();
                          const flagInput = document.getElementById('flag-input');
                          if (flagInput) {
                              const flag = flagInput.value.trim();
                              submitFlag(currentChallengeId, flag);
                          }
                      });
                  }
              }
          }
          
          // Populate files
          if (modalFiles) {
              if (data.files && data.files.length > 0) {
                  data.files.forEach(file => {
                      const fileItem = document.createElement('div');
                      fileItem.className = 'file-item';
                      fileItem.innerHTML = `
                          <div class="file-icon">
                              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                  <polyline points="14 2 14 8 20 8"></polyline>
                                  <line x1="16" y1="13" x2="8" y2="13"></line>
                                  <line x1="16" y1="17" x2="8" y2="17"></line>
                                  <polyline points="10 9 9 9 8 9"></polyline>
                              </svg>
                          </div>
                          <div class="file-name">${file.name}</div>
                          <div class="file-size">${formatFileSize(file.size)}</div>
                          <a href="${file.url}" class="file-download" download>Download</a>
                      `;
                      modalFiles.appendChild(fileItem);
                  });
              } else {
                  modalFiles.innerHTML = '<p>No files for this challenge</p>';
              }
          }
          
          // Populate hints
          if (modalHints) {
              if (data.hints && data.hints.length > 0) {
                  data.hints.forEach((hint, index) => {
                      const hintItem = document.createElement('div');
                      hintItem.className = 'hint-item';
                      
                      if (hint.unlocked) {
                          hintItem.innerHTML = `
                              <div class="hint-header">
                                  <div class="hint-title">Hint ${index + 1}</div>
                                  <div class="hint-status unlocked">Unlocked</div>
                              </div>
                              <div class="hint-content active">
                                  <p class="hint-text">${hint.content}</p>
                              </div>
                          `;
                      } else {
                          hintItem.innerHTML = `
                              <div class="hint-header">
                                  <div class="hint-title">Hint ${index + 1}</div>
                                  <div class="hint-cost">${hint.cost} points</div>
                              </div>
                              <div class="hint-unlock">
                                  <button class="btn btn-outline unlock-hint-btn" data-hint-id="${hint.id}">
                                      Unlock Hint (${hint.cost} pts)
                                  </button>
                              </div>
                          `;
                      }
                      
                      modalHints.appendChild(hintItem);
                  });
              } else {
                  modalHints.innerHTML = '<p>No hints available for this challenge</p>';
              }
          }
      })
      .catch(error => {
          console.error('Error loading challenge details:', error);
          if (modalTitle) modalTitle.textContent = 'Error';
          if (modalDescription) modalDescription.textContent = 'Failed to load challenge details. Please try again.';
      });
  }
  
  // Submit flag via AJAX
  function submitFlag(challengeId, flag) {
      // Get CSRF token
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
      
      // Create form data
      const formData = new FormData();
      formData.append('flag', flag);
      
      // Submit flag
      fetch(`/api/submit/${challengeId}/`, {
          method: 'POST',
          headers: {
              'X-CSRFToken': csrftoken,
              'X-Requested-With': 'XMLHttpRequest'
          },
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          // Show message
          showMessage(data.message, data.success ? 'success' : 'error');
          
          // Clear input
          const flagInput = document.getElementById('flag-input');
          if (flagInput) flagInput.value = '';
          
          // If solved, update UI
          if (data.success) {
              // Update the challenge card
              const challengeCard = document.querySelector(`.challenge-card[data-id="${challengeId}"]`);
              if (challengeCard) {
                  challengeCard.classList.add('solved');
                  challengeCard.dataset.status = 'solved';
                  
                  // Add solved badge if it doesn't exist
                  if (!challengeCard.querySelector('.challenge-solved-badge')) {
                      const solvedBadge = document.createElement('div');
                      solvedBadge.className = 'challenge-solved-badge';
                      solvedBadge.innerHTML = `
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                              <polyline points="22 4 12 14.01 9 11.01"></polyline>
                          </svg>
                          <span>Solved</span>
                      `;
                      challengeCard.appendChild(solvedBadge);
                  }
              }
              
              // Update submission area
              if (submissionArea) {
                  submissionArea.innerHTML = `
                      <div class="solved-message">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                              <polyline points="22 4 12 14.01 9 11.01"></polyline>
                          </svg>
                          <span>You've solved this challenge!</span>
                      </div>
                  `;
              }
              
              // Update solves count
              if (modalSolves) {
                  const solvesValue = parseInt(modalSolves.textContent) + 1;
                  modalSolves.textContent = solvesValue;
                  
                  // Update challenge card solves count
                  if (challengeCard) {
                      const cardSolves = challengeCard.querySelector('.challenge-solves span');
                      if (cardSolves) {
                          cardSolves.textContent = solvesValue + ' solves';
                      }
                  }
              }
          }
      })
      .catch(error => {
          console.error('Error submitting flag:', error);
          showMessage('Error submitting flag. Please try again.', 'error');
      });
  }
  
  // Unlock hint via AJAX
  function unlockHint(hintId) {
      // Get CSRF token
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
      
      // Submit request to unlock hint
      fetch(`/challenges/api/hint/unlock/${hintId}/`, {
          method: 'POST',
          headers: {
              'X-CSRFToken': csrftoken,
              'X-Requested-With': 'XMLHttpRequest'
          }
      })
      .then(response => response.json())
      .then(data => {
          // Show message
          showMessage(data.message, data.success ? 'success' : 'error');
          
          // If hint was unlocked, update UI
          if (data.success && data.content) {
              const hintButton = document.querySelector(`.unlock-hint-btn[data-hint-id="${hintId}"]`);
              if (hintButton) {
                  const hintItem = hintButton.closest('.hint-item');
                  if (hintItem) {
                      const hintHeader = hintItem.querySelector('.hint-header');
                      if (hintHeader) {
                          // Update header
                          hintHeader.innerHTML = `
                              <div class="hint-title">${hintHeader.querySelector('.hint-title').textContent}</div>
                              <div class="hint-status unlocked">Unlocked</div>
                          `;
                      }
                      
                      // Replace unlock button with hint content
                      const hintUnlock = hintItem.querySelector('.hint-unlock');
                      if (hintUnlock) {
                          hintUnlock.outerHTML = `
                              <div class="hint-content active">
                                  <p class="hint-text">${data.content}</p>
                              </div>
                          `;
                      }
                  }
              }
          }
      })
      .catch(error => {
          console.error('Error unlocking hint:', error);
          showMessage('Error unlocking hint. Please try again.', 'error');
      });
  }
  
  // Show message in modal
  function showMessage(message, type) {
      if (!modalMessages) return;
      
      const messageDiv = document.createElement('div');
      messageDiv.className = `message ${type}`;
      messageDiv.textContent = message;
      
      modalMessages.innerHTML = '';
      modalMessages.appendChild(messageDiv);
      
      // Auto-remove message after 5 seconds
      setTimeout(() => {
          messageDiv.style.opacity = '0';
          setTimeout(() => {
              if (modalMessages && modalMessages.contains(messageDiv)) {
                  modalMessages.removeChild(messageDiv);
              }
          }, 500);
      }, 5000);
  }
  
  // Format file size
  function formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
});