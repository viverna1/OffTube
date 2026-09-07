import { api } from "../api.js";
import { format_duration } from "../utils.js";


async function fetch_thumbnail(el) {
    const placeholder = el.querySelector('.video-thumbnail-placeholder');
    if (!placeholder) return;

    const thumbnail_wrapper = el.querySelector('.thumbnail-wrapper');
    const videoId = el.getAttribute('data-id');

    try {
        const data = await api(`/videos/${videoId}/thumbnail`);
        
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
            <div class="video-thumbnail video-thumbnail-placeholder">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="48" fill="white"/>
                    <polygon points="38,28 38,72 72,50" fill="#434343"/>
                </svg>
            </div>
        </div>
        <p class="video-title">${video.name}</p>
    `;

    return video_el;
}
