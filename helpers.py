import os
from app import app


def recover_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'game_{id}' in filename:
            return filename

    return 'capa_padrao.jpg'


def delete_image(id):
    filename = recover_image(id)
    if filename != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))
