from flask import Flask, render_template, request, jsonify
from matplotlib import pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No image selected!", 400

    image = request.files['image']

    if image.filename == '':
        return "No image selected!", 400

    # Read the uploaded image and convert to grayscale
    image_data = image.read()
    image_array = io.BytesIO(image_data)

    # Import any image processing libraries you may need
    from PIL import Image
    img = Image.open(image_array).convert('L')

    # Calculate the histogram of pixel values
    histogram = img.histogram()

    # Plot the histogram using matplotlib
    plt.figure(figsize=(8, 6))
    plt.hist(histogram, bins=256, range=(0, 256), color='gray', alpha=0.8)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Pixel Values')
    plt.grid(True)
    
    # Save the plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the plot to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the plot data to the client
    return jsonify({'plot_data': plot_data})

if __name__ == '__main__':
    app.run(debug=True)
