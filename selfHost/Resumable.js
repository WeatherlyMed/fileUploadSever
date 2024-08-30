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
  r.on('fileProgress', function (file) {
        const progressElements = document.querySelectorAll('.file-progress');
        progressElements.forEach(function (element) {
            if (element.querySelector('span').innerText === file.fileName) {
                const progressBar = element.querySelector('.progress-bar');
                progressBar.innerText = Math.floor(file.progress() * 100) + '%';
            }
        });
    });

    r.on('fileSuccess', function (file) {
        console.log(`${file.fileName} uploaded successfully.`);
    });

    r.on('fileError', function (file, message) {
        console.error(`Error uploading ${file.fileName}: ${message}`);
    });
    window.startUpload = function () {
        if (!document.getElementById('tosCheckbox').checked) {
            alert('You must agree to the Terms of Service.');
            return;
        }
        r.upload();
    };
});
