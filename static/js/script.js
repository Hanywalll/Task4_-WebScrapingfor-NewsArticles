document.getElementById('search-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const query = document.getElementById('query-input').value;
    const resultsContainer = document.getElementById('results-container');
    const loadingDiv = document.getElementById('loading');
    const noResultsP = document.getElementById('no-results');

    loadingDiv.classList.remove('hidden');
    resultsContainer.innerHTML = '';
    noResultsP.classList.add('hidden');

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ 'query': query })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const articles = await response.json();

        loadingDiv.classList.add('hidden');

        if (Array.isArray(articles) && articles.length > 0) {
            articles.forEach(article => {
                if (!article.title || !article.body_text) {
                    console.warn('Artikel tidak valid:', article);
                    return;
                }
                
                const articleCard = document.createElement('div');
                articleCard.className = 'article-card';
                
                const imageUrl = article.image_link && article.image_link !== "N/A" 
                    ? article.image_link 
                    : 'https://via.placeholder.com/150';
                
                articleCard.innerHTML = `
                    <div class="article-image">
                        <img src="${imageUrl}" alt="${article.title}" onerror="this.onerror=null;this.src='https://via.placeholder.com/150'">
                    </div>
                    <div class="article-content">
                        <h2>${article.title}</h2>
                        <p>${article.body_text.substring(0, 250)}...</p>
                        <span class="meta">${article.publication_time}</span>
                        <a href="${article.url || '#'}" target="_blank" class="read-more">Baca selengkapnya</a>
                    </div>
                `;
                resultsContainer.appendChild(articleCard);
            });
        } else {
            noResultsP.classList.remove('hidden');
        }

    } catch (error) {
        console.error('Terjadi kesalahan:', error);
        loadingDiv.classList.add('hidden');
        resultsContainer.innerHTML = `<p class="error">Terjadi kesalahan: ${error.message}</p>`;
    }
});