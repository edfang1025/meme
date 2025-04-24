from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os

from PIL import ImageFont

#font = ImageFont.truetype("Arimo.ttf", size=40)  # <- change size here
font_path = "font/Arimo.ttf"
font = ImageFont.truetype(font_path,size=500)

app = Flask(__name__)

# Path to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_meme():
    if 'image' not in request.files:
        return redirect(request.url)
    
    image_file = request.files['image']
    if image_file.filename == '':
        return redirect(request.url)

    # Save the image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    # Get the text from the form
    top_text = request.form['top_text']
    bottom_text = request.form['bottom_text']

    # Open the uploaded image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Define font size (choose your own font)
    #font = ImageFont.load_default()
    font = ImageFont.truetype("font/Arimo.ttf", size = 100)
   
    # Load the uploaded image first
    #image = Image.open(image_path)
    
    # THEN you can use image.size
    image_width, image_height = img.size

    # Add top text
    #draw.text((10, 10), top_text, font=font, fill="white")
    #bbox = draw.textbbox((0,0), top_text, font=font)
    #text_width = bbox[2] - bbox[0]
    #text_height = bbox[3] - bbox[1]
    #top_position = ((image_width - text_width)/2, 10)
    top_bbox = draw.textbbox((0, 0), top_text, font=font)
    top_text_width = top_bbox[2] - top_bbox[0]
    top_text_height = top_bbox[3] - top_bbox[1]
    top_position = ((image_width - top_text_width) / 2, 10)
    draw.text(top_position, top_text, font=font, fill="white")
    
    # Add bottom text
    #text_width, text_height = draw.textsize(bottom_text, font=font)
    #bbox = draw.textbbox((0, 0), bottom_text, font=font)
    #text_width = bbox[2] - bbox[0]
    #text_height = bbox[3] - bbox[1]
    #position = (img.width - text_width - 10, img.height - text_height - 10)
    bottom_bbox = draw.textbbox((0, 0), bottom_text, font=font)
    bottom_text_width = bottom_bbox[2] - bottom_bbox[0]
    bottom_text_height = bottom_bbox[3] - bottom_bbox[1]
    bottom_position = ((image_width - bottom_text_width) / 2, image_height - bottom_text_height - 50)
    draw.text(bottom_position, bottom_text, font=font, fill="white")

    # Save the meme image
    meme_path = os.path.join(app.config['UPLOAD_FOLDER'], f"meme_{image_file.filename}")
    img.save(meme_path)

    return render_template('result.html', meme_path=meme_path)

if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))  # default to 5000 locally
    app.run(host="0.0.0.0", port=port)
