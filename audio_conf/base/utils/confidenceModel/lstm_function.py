
# import librosa
# import numpy as np
# import warnings
# from keras.models import load_model

# # Load the model
# model = load_model('lstm_model.keras')


# warnings.filterwarnings('ignore')

# #variables declaration
# n_mfcc = 5
# n_fft=2048
# hop_length=8192
# #sr =22050 


# #model.summary()

# def extract_mfcc(audio_file):
#     """Extract MFCC features from the audio file.
#     """
#     y,sr = librosa.load(audio_file)
#     mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc,n_fft=n_fft, hop_length=hop_length)
#     new_mfcc = mfcc.flatten()   
#     mean = np.mean(new_mfcc)
#     std = np.std(new_mfcc)
#     z_score_normalized = (new_mfcc - mean) / std
#     normalized_mfcc = z_score_normalized 
#     pre_mfcc = normalized_mfcc.tolist()    
#     mfcc = np.zeros(59)

#     # Replace the first elements with the values from pre_mfcc
#     if len(pre_mfcc) < 59:
#         mfcc[:len(pre_mfcc)] = pre_mfcc
#     else:
#         mfcc[:] = pre_mfcc[:59]
#     mfcc=np.round(mfcc,4)
#     final_mfcc=mfcc[:59]
#     final_mfcc = np.expand_dims(final_mfcc, axis=1)
#     return (final_mfcc)


# warnings.filterwarnings('ignore')

        

# def classify_audio(audio_file, model):
#     """Classify the audio using the pre-trained model."""
#     mfccs = extract_mfcc(audio_file)
#     prediction = np.argmax(model.predict(mfccs),axis = -1)
#     predictions=np.argmin(model.predict(mfccs), axis = -1)
#     #print(predictions)
#     #print(prediction)
#     mp_prediction = np.maximum(prediction, predictions)
#     if (predictions[1] == 2):
#         mp_prediction[1] = 2
#     return mp_prediction




# if __name__ == "__main__":
#     # Paths to the keras model and audio file
#     model_file = "lstm_model.h5"
#     audio_file = "268767_audio.wav"


#     # Classify the audio file
#     print(audio_file)
#     prediction = classify_audio(audio_file, model)
#     print(prediction[1])

    

    


import librosa
import numpy as np
from keras.models import load_model
model_path = "base/utils/confidenceModel/lstm_model.keras"
model = load_model(model_path)


def extract_mfcc(audio_file_path):
    """Extract MFCC features from the audio file."""
    y, sr = librosa.load(audio_file_path)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=5, n_fft=2048, hop_length=8192)
    new_mfcc = mfcc.flatten()   
    mean = np.mean(new_mfcc)
    std = np.std(new_mfcc)
    z_score_normalized = (new_mfcc - mean) / std
    normalized_mfcc = z_score_normalized 
    pre_mfcc = normalized_mfcc.tolist()    
    mfcc = np.zeros(59)
    if len(pre_mfcc) < 59:
        mfcc[:len(pre_mfcc)] = pre_mfcc
    else:
        mfcc[:] = pre_mfcc[:59]
    mfcc=np.round(mfcc,4)
    final_mfcc=mfcc[:59]
    final_mfcc = np.expand_dims(final_mfcc, axis=1)
    return (final_mfcc)

def classify_audio(mfccs):
    """Classify the audio using the pre-trained model."""
    prediction = np.argmax(model.predict(mfccs), axis=-1)
    predictions = np.argmin(model.predict(mfccs), axis=-1)
    mp_prediction = np.maximum(prediction, predictions)
    if predictions[1] == 2:
        mp_prediction[1] = 2
    return mp_prediction


