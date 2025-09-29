document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('browse-all-btn');
    let message = document.querySelector(".messages");

    if (btn) {
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
                        <a href="/details/${post.slug}/" class="image"><img src="${post.image_url}" alt="" /></a>
                        <h3 class="major">${post.name}</h3>
                        <p>${post.description}</p>
                        <a href="/details/${post.slug}/" class="special">Learn more</a>
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
    }

    if (message) {
        message.style.transition = "opacity 0.5s ease-in";
        message.style.opacity = "1";

        setTimeout(() => {
            message.style.transition = "opacity 1.2s ease-out";
            message.style.opacity = "0";
            setTimeout(() => {
                message.remove();
            }, 1200)
        }, 3900);
    }
});