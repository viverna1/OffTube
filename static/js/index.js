async function api(path, options = {}) {
    const response = await fetch(`/api/${path}`, options);

    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error(
            response.ok
                ? 'Сервер вернул некорректный JSON'
                : `HTTP ${response.status}: ${response.statusText}`
        );
    }

    if (!response.ok) {
        throw new Error(data.error || `HTTP ${response.status}`);
    }

    if (!data.ok) {
        throw new Error(data.error || 'Неизвестная ошибка API');
    }

    return data.data;
}


async function fetch_thumbnail(el) {
    const placeholder = el.querySelector('.video-thumbnail-placeholder');
    if (!placeholder) return;

    const thumbnail_wrapper = el.querySelector('.thumbnail-wrapper');
    const videoId = el.getAttribute('data-id');

    try {
        const data = await api(`videos/${videoId}/thumbnail`);
        
        const img = document.createElement('img');
        img.className = 'video-thumbnail';
        img.src = data.thumbnail_path;
        img.alt = '▶';

        if (data.generated) {
            setTimeout(() => {
                placeholder.remove();
                thumbnail_wrapper.prepend(img);
            }, 200);
        } else {
            placeholder.remove();
            thumbnail_wrapper.prepend(img);
        }
    } catch (error) {
        console.log('Не удалось загрузить thumbnail:', error);
    }
}


async function fetch_duration(el) {
    if (el.querySelector('.duration')) return;

    const thumbnail_wrapper = el.querySelector('.thumbnail-wrapper');
    const videoId = el.getAttribute('data-id');

    try {
        const data = await api(`videos/${videoId}/duration`);

        const duration = document.createElement('div');
        duration.className = 'duration';
        duration.textContent = data.duration;

        if (data.generated) {
            setTimeout(() => {
                thumbnail_wrapper.prepend(duration);
            }, 200);
        } else {
            thumbnail_wrapper.prepend(duration);
        }
    } catch (error) {
        console.log('Не удалось загрузить duration:', error);
    }
}


const videos_container = document.getElementById("videos");
let loading_videos = false;
let has_more_videos = true;

async function load_more_videos() {
    if (loading_videos || !has_more_videos) return;

    loading_videos = true;

    try {
        const data = await api('videos');

        if (data.videos.length === 0) {
            has_more_videos = false;
            return;
        }

        for (const video of data.videos) {
            const video_el = create_video_el(video);

            videos_container.appendChild(video_el);

            fetch_thumbnail(video_el);
            fetch_duration(video_el);
        }
    } catch (error) {
        console.error('Не удалось загрузить видео:', error);
    } finally {
        loading_videos = false;
    }

    if (should_load_more()) {
        load_more_videos();
    }
}


function should_load_more() {
    return (
        window.innerHeight + window.scrollY >=
        document.documentElement.scrollHeight - 300
    );
}


function create_video_el(video_state) {
    const video_el = document.createElement('a');

    video_el.className = 'video';
    video_el.href = `/watch/${video_state.id}`;
    video_el.dataset.id = video_state.id;

    video_el.innerHTML = `
        <div class="thumbnail-wrapper">
            <div class="video-thumbnail video-thumbnail-placeholder">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="48" fill="white"/>
                    <polygon points="38,28 38,72 72,50" fill="#434343"/>
                </svg>
            </div>
        </div>
        <p class="video-title">${video_state.name}</p>
    `;

    return video_el;
}


function init_video(video_el) {
    fetch_thumbnail(video_el);
    fetch_duration(video_el);
}



function handle_scroll() {
    if (should_load_more()) {
        load_more_videos();
    }
}


function main() {
    document.querySelectorAll('.video').forEach(init_video);
    window.addEventListener('scroll', handle_scroll);
    load_more_videos();
}


main();