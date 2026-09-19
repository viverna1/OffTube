import { api } from "../api.js";
import { format_duration } from "../utils.js";

const MAX_METADATA_REQUESTS = 5;
const metadata_queue = [];
let active_metadata_requests = 0;


function process_metadata_queue() {
    while (
        active_metadata_requests < MAX_METADATA_REQUESTS &&
        metadata_queue.length > 0
    ) {
        const load_metadata = metadata_queue.shift();
        active_metadata_requests += 1;

        load_metadata().finally(() => {
            active_metadata_requests -= 1;
            process_metadata_queue();
        });
    }
}


function enqueue_metadata(load_metadata) {
    metadata_queue.push(load_metadata);
    process_metadata_queue();
}



function load_thumbnail_image(el, data) {
    return new Promise((resolve) => {
        const videoId = el.getAttribute('data-id');
        const thumbnail_wrapper = el.querySelector('.thumbnail-wrapper');
        if (!thumbnail_wrapper) return resolve();

        const img = document.createElement('img');
        img.className = 'video-thumbnail';
        img.alt = '▶';
        img.decoding = 'async';

        img.addEventListener('load', () => {
            thumbnail_wrapper.prepend(img);
            setTimeout(() => el.classList.remove('loading'), 500);
            resolve();
        }, { once: true });

        img.addEventListener('error', () => {
            el.classList.remove('loading');
            resolve();
        }, { once: true });

        img.src = data.thumbnail_path;
    });
}


async function fetch_thumbnail(el) {
    const videoId = el.getAttribute('data-id');
    el.classList.add('loading');
    try {
        const data = await api(`/videos/${videoId}/thumbnail`);
        await load_thumbnail_image(el, data);
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
    enqueue_metadata(() => fetch_thumbnail(video_el));
    enqueue_metadata(() => fetch_duration(video_el));
}


export function create_video_el(video) {
    const video_el = document.createElement('a');

    video_el.className = 'video';
    video_el.href = `/watch/${video.id}`;
    video_el.dataset.id = video.id;

    video_el.innerHTML = `
        <div class="thumbnail-wrapper">
            <div class="video-thumbnail-placeholder"></div>
        </div>
        <p class="video-title">${video.name}</p>
    `;

    return video_el;
}
