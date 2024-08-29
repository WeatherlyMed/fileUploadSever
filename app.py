import os
from quart import Quart, request, jsonify, render_template
import aiofiles
import asyncio

app = Quart(__name__)
UPLOAD_FOLDER = 'uploads'

# Route to render the HTML template
@app.route('/upload', methods=['GET'])
async def upload_form():
    return await render_template('uploads.html')

# Existing route for file upload handling
@app.route('/', methods=['POST'])
async def upload_chunk():
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        # Extract parameters from the request
        form = await request.form
        resumableChunkNumber = form.get('resumableChunkNumber')
        resumableTotalChunks = form.get('resumableTotalChunks')
        folder_choice = form.get('folder')

        # Validate form data
        if not resumableChunkNumber or not resumableTotalChunks or not folder_choice:
            return jsonify({'error': 'Missing form data'}), 400

        if folder_choice == 'folder1':
            save_path = os.path.join(UPLOAD_FOLDER, 'folder1')
        elif folder_choice == 'folder2':
            save_path = os.path.join(UPLOAD_FOLDER, 'folder2')
        else:
            return jsonify({'error': 'Invalid folder choice'}), 400

        os.makedirs(save_path, exist_ok=True)

        files = await request.files  # Await to get the files dictionary
        file = files.get('file')
        if not file:
            return jsonify({'error': 'File is missing'}), 400

        chunk_number = int(resumableChunkNumber)

        chunk_path = os.path.join(save_path, f'{file.filename}.part{chunk_number}')
        async with aiofiles.open(chunk_path, 'wb') as f:
            await f.write(file.read())

        files = await asyncio.to_thread(os.listdir, save_path)
        if len([f for f in files if f.startswith(file.filename) and '.part' in f]) == int(resumableTotalChunks):
            async with aiofiles.open(os.path.join(save_path, file.filename), 'wb') as f:
                for i in range(1, int(resumableTotalChunks) + 1):
                    chunk_path = os.path.join(save_path, f'{file.filename}.part{i}')
                    async with aiofiles.open(chunk_path, 'rb') as chunk_file:
                        await f.write(await chunk_file.read())
                    await asyncio.to_thread(os.remove, chunk_path)

        return jsonify({'status': 'Chunk received'})
    else:
        return jsonify({'error': 'Invalid content type'}), 400

if __name__ == '__main__':
    import asyncio
    asyncio.run(app.run(debug=True))
