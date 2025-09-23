document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('browse-all-btn');
    if (!btn) return;

    btn.addEventListener('click', function() {
        fetch('?show_all=1', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('posts-container');
            container.innerHTML = '';

            data.posts.forEach(post => {
                const article = document.createElement('article');
                article.innerHTML = `
                    <a href="/posts/${post.slug}/" class="image"><img src="${post.image_url}" alt="" /></a>
                    <h3 class="major">${post.name}</h3>
                    <p>${post.description}</p>
                    <a href="/posts/${post.slug}/" class="special">Learn more</a>
                `;
                container.appendChild(article);
            });

            btn.style.display = 'none';

            const actionsUl = btn.closest('ul.actions');
            if (actionsUl) {
                actionsUl.innerHTML = '<li><a href="." class="button">Show less</a></li>';
            }
        })
        .catch(err => {
            console.error('Error loading all posts:', err);
        });
    });
});