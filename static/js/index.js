function fetch_thumbnail(el) {
    const placeholder = el.querySelector('.video-thumbnail-placeholder');
    if (!placeholder) return;

    const thumbnail_wrapper = el.querySelector('.thumbnail-wrapper');
    const videoId = el.getAttribute('data-id');
    
    fetch('/fetch-thumbnail-ajax', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_id: videoId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response === "error")
            return;

        const img = document.createElement('img');
        img.className = 'video-thumbnail';
        img.src = data.thumbnail_path;
        img.alt = "▶";

        if (data.generated) {
            setTimeout(() => {
                placeholder.remove();
                thumbnail_wrapper.prepend(img);
            }, 200);
        } else {
            placeholder.remove();
            thumbnail_wrapper.prepend(img);
        }
    })
}

function fetch_duration(el) {
    const duration = el.querySelector('.duration');
    if (duration) return;

    const thumbnail_wrapper = el.querySelector('.thumbnail-wrapper');
    const videoId = el.getAttribute('data-id');

    fetch('/fetch-duration-ajax', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_id: videoId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response === "error")
            return;

        const img = document.createElement('div');
        img.className = 'duration';
        img.textContent = data.duration;

        if (data.generated) {
            setTimeout(() => {
                thumbnail_wrapper.prepend(img);
            }, 200);
        } else {
            thumbnail_wrapper.prepend(img);
        }
    })
}


const video_observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            
            fetch_thumbnail(el);
            fetch_duration(el);
            
            video_observer.unobserve(el);
        }
    });
});


document.querySelectorAll('.video').forEach(video => {
    video_observer.observe(video);
});