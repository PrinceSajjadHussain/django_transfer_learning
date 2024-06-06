import os
import numpy as np
from django.shortcuts import render
from django.conf import settings
from .forms import UploadFileForm
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load the model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'cats_and_dogs_model.h5')
model = tf.keras.models.load_model(MODEL_PATH)

def index(request):
    predictions = []
    error_message = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            for file in files:
                try:
                    # Save uploaded file
                    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
                    with open(file_path, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                    
                    # Prepare image for prediction
                    img = image.load_img(file_path, target_size=(128, 128))
                    img_array = image.img_to_array(img)
                    img_array = np.expand_dims(img_array, axis=0)
                    img_array = preprocess_input(img_array)

                    # Predict
                    prediction = model.predict(img_array)
                    prediction_label = 'Dog' if prediction[0][0] > 0.5 else 'Cat'
                    predictions.append((os.path.join(settings.MEDIA_URL, file.name), prediction_label))
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
        else:
            error_message = "Invalid form submission"
    else:
        form = UploadFileForm()

    return render(request, 'app/index.html', {'form': form, 'predictions': predictions, 'error_message': error_message})
