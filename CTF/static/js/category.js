document.addEventListener('DOMContentLoaded', function() {
    const difficultyFilter = document.getElementById('difficulty');
    const statusFilter = document.getElementById('status');
    const categoryFilter = document.getElementById('sort');
    const searchInput = document.getElementById('search');
    const challengeCards = document.querySelectorAll('.challenge-card');
    
    if (difficultyFilter) difficultyFilter.addEventListener('change', applyFilters);
    if (statusFilter) statusFilter.addEventListener('change', applyFilters);
    if (categoryFilter) categoryFilter.addEventListener('change', applyFilters);
    
    if (searchInput) searchInput.addEventListener('input', applyFilters);
    
    function applyFilters() {
        const difficulty = difficultyFilter ? difficultyFilter.value : 'all';
        const status = statusFilter ? statusFilter.value : 'all';
        const category = categoryFilter ? categoryFilter.value : 'all';
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
            
            if (difficultyMatch && statusMatch && categoryMatch && searchMatch) 
                card.style.display = 'block';
            else 
                card.style.display = 'none';
        });
    }
    
    // Hint toggle functionality for category page
    document.addEventListener('click', function(e) {
        const hintHeader = e.target.closest('.hint-header');
        if (hintHeader) {
            const hintItem = hintHeader.closest('.hint-item');
            if (hintItem) {
                const hintContent = hintItem.querySelector('.hint-content');
                if (hintContent)
                    hintContent.classList.toggle('active');
            }
        }
    });
});