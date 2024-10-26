from flask import Flask, request, render_template
from datetime import datetime
import os
import threading
from analysis import analyze_image
from send_email import send_email
from config import UPLOAD_FOLDER

def analyze_and_send_email(image_path):
    response_text = analyze_image(image_path)
    send_email(response_text, image_path)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the POST request has image
    if request.content_type == "image/jpeg":
        # Record timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"img_{timestamp}.jpg"

        # Save image
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as f:
            f.write(request.data)

        # Start LLM analysis and email sending in a new thread
        analysis_thread = threading.Thread(target=analyze_and_send_email, args=(file_path,))
        analysis_thread.start()

        # Return a success response
        return "Ok. thanks!", 200
    else:
        # If the request does not contain an image
        return "No image found in request", 400

# Route to display uploaded images
@app.route('/')
def index():
    # Get list of image filenames in the uploads folder
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    image_urls = [os.path.join(app.config['UPLOAD_FOLDER'], img) for img in images]
    return render_template('index.html', images=image_urls)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
