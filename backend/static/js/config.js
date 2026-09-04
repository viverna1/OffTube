import { api } from "./api.js";

export async function get_config() {
    const data = await api(`/config`);
    console.log(data.config);
    
    return data.config
}