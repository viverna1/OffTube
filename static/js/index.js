function fetch_thumbnail(el) {
    const placeholder = el.querySelector('.video-thumbnail-placeholder');
    if (!placeholder) return;

    const videoId = el.getAttribute('data-id');
    
    fetch('/generate-thumbnails-ajax', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_id: videoId })
    })
    .then(response => response.json())
    .then(data => {
        const img = document.createElement('img');
        img.className = 'video-thumbnail';
        img.src = data.thumbnail_path;
        img.alt = "▶";

        setTimeout(() => {
            placeholder.remove();
            el.prepend(img);
        }, 200);
    })
}


function main() {
    videos = document.querySelectorAll('.video');

    videos.forEach(video => {
        fetch_thumbnail(video);
    });
}

// main();