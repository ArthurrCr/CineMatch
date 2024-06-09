document.getElementById('preferencesForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = {
        userId: document.getElementById('userId').value,
        favoriteMovie: document.getElementById('favoriteMovie').value,
        genres: document.getElementById('genres').value,
        tags: document.getElementById('tags').value
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById('recommendations').innerHTML = '<p>Recomendações: ' + JSON.stringify(data) + '</p>';
        } else {
            throw new Error(data.message || 'Erro ao obter recomendações');
        }
    } catch (error) {
        document.getElementById('recommendations').innerHTML = '<p>Erro: ' + error.message + '</p>';
    }
});

function searchMovies() {
    const query = document.getElementById('searchQuery').value;
    fetch('/search?query=' + encodeURIComponent(query))
    .then(response => response.json())
    .then(data => {
        document.getElementById('searchResults').innerHTML = '<p>Resultados da busca: ' + JSON.stringify(data) + '</p>';
    })
    .catch(error => {
        document.getElementById('searchResults').innerHTML = '<p>Erro: ' + error.message + '</p>';
    });
}
