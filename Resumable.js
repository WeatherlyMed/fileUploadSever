document.addEventListener("DOMContentLoaded", function () {
    const r = new Resumable({
        target: '/',
        query: function () {
            return {
                folder: document.getElementById('folderSelect').value,
                tos: document.getElementById('tosCheckbox').checked ? 'agree' : ''
            };
        },
        chunkSize: 1 * 1024 * 1024,//1MB
        simultaneousUploads: 5,
        testChunks: false,
        throttleProgressCallbacks: 1
    });

    r.assignBrowse(document.getElementById('fileInput'));

    r.on('fileAdded', function (file) {
        const progressElement = document.createElement('div');
        progressElement.className = 'file-progress';
        progressElement.innerHTML = `<span>${file.fileName}</span> <span class="progress-bar">0%</span>`;
        document.getElementById('uploadProgress').appendChild(progressElement);
    });
