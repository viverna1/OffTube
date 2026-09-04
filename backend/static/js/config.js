import { api } from "./api.js";

export async function get_config() {
    const data = await api(`/config`);
    return data.config
}