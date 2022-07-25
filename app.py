# Importing flask module

from flask import Flask, render_template, request

# Importing Keras Modules

from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import decode_predictions

app = Flask(__name__)

#The Model
model = VGG16()

# Get Route
@app.route('/', methods=['GET'])
def hello_world():
    #Render Template
    return render_template('app.html')

# Receive input and post to model
@app.route('/', methods=['POST'])
def predict():
    fileImage = request.files['fileImage']
    image_path = "./images/" + fileImage.filename
    fileImage.save(image_path)
    
    #Load Image
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    
    #Process Image
    image = preprocess_input(image)
    
    #Make Predictions
    yhat = model.predict(image)
    label = decode_predictions(yhat)
    label = label[0][0]
    
    #Make Classifications    
    classification = '%s (%.2f%%)' % (label[1], label[2]*100)
    
    return render_template('app.html', prediction=classification)
    
# Intitalise Port
if __name__ == '__main__':
    app.run(port=3000, debug=False)

