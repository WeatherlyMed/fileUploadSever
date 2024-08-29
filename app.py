import os
from quart import Quart, request, jsonify
import aiofiles

app = Quart(__name__)
UPLOAD_FOLDER = 'uploads'

@app.route('/', methods=['POST'])
async def upload_chunk():
    if request.content_type.startswith('multipart/form-data'):
        resumableChunkNumber = request.form['resumableChunkNumber']
        resumableTotalChunks = request.form['resumableTotalChunks']
        folder_choice = request.form['folder']

        if folder_choice == 'folder1':
            save_path = os.path.join(UPLOAD_FOLDER, 'folder1')
        elif folder_choice == 'folder2':
            save_path = os.path.join(UPLOAD_FOLDER, 'folder2')
        else:
            return jsonify({'error': 'Invalid folder choice'}), 400
        
        os.makedirs(save_path, exist_ok=True)

        file = request.files['file']
        chunk_number = int(resumableChunkNumber)

        chunk_path = os.path.join(save_path, f'{file.filename}.part{chunk_number}')
        async with aiofiles.open(chunk_path, 'wb') as f:
            await f.write(await file.read())

        if len([f for f in os.listdir(save_path) if f.startswith(file.filename) and '.part' in f]) == int(resumableTotalChunks):
            async with aiofiles.open(os.path.join(save_path, file.filename), 'wb') as f:
                for i in range(1, int(resumableTotalChunks) + 1):
                    chunk_path = os.path.join(save_path, f'{file.filename}.part{i}')
                    async with aiofiles.open(chunk_path, 'rb') as chunk_file:
                        await f.write(await chunk_file.read())
                    os.remove(chunk_path)

        return jsonify({'status': 'Chunk received'})

if __name__ == '__main__':
    app.run(debug=True)
