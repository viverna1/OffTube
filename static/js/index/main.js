import { api } from "../api.js";
import { get_config } from "../config.js";
import { create_video_el, init_video } from "./video.js";

let loading_videos = false;
let has_more_videos = true;

const config = await get_config();
let current_offset = config.init_videos_count || 0;
const VIDEOS_PER_LOAD = config.videos_per_load || 10;


const videos_container = document.getElementById("videos");


function should_load_more() {
    return (
        window.innerHeight + window.scrollY >=
        document.documentElement.scrollHeight - 300
    );
}


async function load_more_videos() {
    if (loading_videos || !has_more_videos) return;

    loading_videos = true;

    try {
        const data = await api(`/videos?offset=${current_offset}&limit=${VIDEOS_PER_LOAD}`);

        if (!data.videos || data.videos.length === 0) {
            has_more_videos = false;
            return;
        }

        current_offset += data.videos.length;

        for (const video of data.videos) {
            const video_el = create_video_el(video);
            videos_container.appendChild(video_el);
            init_video(video_el);
        }

        if (data.videos.length < VIDEOS_PER_LOAD) {
            has_more_videos = false;
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