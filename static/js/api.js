export async function api(path, options = {}) {
    const response = await fetch(`/api${path}`, options);

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
