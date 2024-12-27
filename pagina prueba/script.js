document.getElementById('downloadButton').addEventListener('click', function () {
    // Obtén el código del textarea
    const code = document.getElementById('codeInput').value;

    // Crea un Blob con el contenido del código
    const blob = new Blob([code], { type: 'text/javascript' });

    // Crea una URL para el Blob
    const url = URL.createObjectURL(blob);

    // Crea un elemento <a> para descargar el archivo
    const a = document.createElement('a');
    a.href = url;
    a.download = 'code.js';
    document.body.appendChild(a);
    a.click();

    // Limpia la URL del Blob y remueve el elemento <a>
    setTimeout(() => {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 0);
});
