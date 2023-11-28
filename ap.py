from flask import Flask, render_template, request
import base64
import os
import time

app = Flask(__name__)
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    try:
        data = request.get_json()
        image_data = data.get('image')

        # Convertir la chaîne base64 en données binaires
        image_data = base64.b64decode(image_data.split(',')[1])

        # Créer un répertoire s'il n'existe pas
        if not os.path.exists('images_cap'):
            os.makedirs('images_cap')

        # Enregistrer l'image dans le répertoire images_cap
        image_path = os.path.join('images_cap', f'image_{int(time.time())}.jpeg')
        with open(image_path, 'wb') as f:
            f.write(image_data)

        return 'Image saved successfully'
    except Exception as e:
        return f'Error saving image: {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
