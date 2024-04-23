document.querySelectorAll('.gallery a').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const lightboxImage = document.createElement('div');
        lightboxImage.id = 'lightbox';
        lightboxImage.innerHTML = `
            <div class="lightbox-content">
                <img src="${this.href}" alt="${this.dataset.title}">
                <p>${this.dataset.title}</p>
            </div>
        `;
        lightboxImage.addEventListener('click', () => {
            lightboxImage.remove();
        });
        document.body.appendChild(lightboxImage);
    });
});
