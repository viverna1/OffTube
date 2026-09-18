import { api } from "../api.js";
import { format_duration } from "../utils.js";


async function fetch_thumbnail(el) {
    const placeholder = el.querySelector('.video-thumbnail-placeholder');
    if (!placeholder) return;

    const thumbnail_wrapper = el.querySelector('.thumbnail-wrapper');
    const videoId = el.getAttribute('data-id');

    try {
        el.classList.add('loading');
        const data = await api(`/videos/${videoId}/thumbnail`);
        
        const img = document.createElement('img');
        img.className = 'video-thumbnail';
        img.src = data.thumbnail_path;
        img.alt = '▶';

        if (data.generated) {
            setTimeout(() => {
                // placeholder.remove();
                thumbnail_wrapper.prepend(img);
                el.classList.remove('loading');
            }, 200);
        } else {
            // placeholder.remove();
            thumbnail_wrapper.prepend(img);
            el.classList.remove('loading');
        }
    } catch (error) {
        console.log('Не удалось загрузить thumbnail:', error);
        el.classList.remove('loading');
    }
}


async function fetch_duration(el) {
    if (el.querySelector('.duration')) return;

    const thumbnail_wrapper = el.querySelector('.thumbnail-wrapper');
    const videoId = el.getAttribute('data-id');

    try {
        const data = await api(`/videos/${videoId}/duration`);

        const duration = document.createElement('div');
        duration.className = 'duration';
        duration.textContent = format_duration(data.duration);

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


export function init_video(video_el) {
    fetch_thumbnail(video_el);
    fetch_duration(video_el);
}


export function create_video_el(video) {
    const video_el = document.createElement('a');

    video_el.className = 'video';
    video_el.href = `/watch/${video.id}`;
    video_el.dataset.id = video.id;

    video_el.innerHTML = `
        <div class="thumbnail-wrapper">
            <div class="video-thumbnail-placeholder"></div>
            <div class="duration">12:43</div>
        </div>
        <p class="video-title">${video.name}</p>
    `;

    return video_el;
}
