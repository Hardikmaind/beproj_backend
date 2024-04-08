
import torch
from torch.nn.functional import softmax
from transformers import BertForSequenceClassification, BertTokenizer
import pickle, os
from django.conf import settings
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer




def classify_sentiment(compound_score):
    if compound_score >= 0.05:
        return 1  # Positive sentiment
    elif compound_score <= -0.05:
        return -1  # Negative sentiment
    else:
        return 0  # Neutral sentiment
    
    
    
    
    
def grammar(path):
    # Load the saved model and tokenizer
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, 'bert_model_tokenizer.pkl')
    with open(file_path, 'rb') as file:
        saved_data = pickle.load(file)

    # Load the model and tokenizer
    loaded_model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
    loaded_model.load_state_dict(saved_data['model'])
    loaded_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Read the text file
    base_dir = settings.BASE_DIR
    transcript_file_path = os.path.join(base_dir, 'media', 'transcript.txt')
    print(transcript_file_path, "this is the path of the file")
    with open(transcript_file_path, 'r') as text_file:
        transcribed_text = text_file.read()

    # Tokenize the input text
    encoded_dict = loaded_tokenizer.encode_plus(
        transcribed_text,
        add_special_tokens=True,
        padding=True,
        return_attention_mask=True,
        return_tensors='pt',
    )

    # Move inputs to the device (CPU in this case)
    input_id = encoded_dict['input_ids']
    attention_mask = encoded_dict['attention_mask'] 
    input_id = input_id.to('cpu')
    attention_mask = attention_mask.to('cpu')

    # Model inference
    with torch.no_grad():
        outputs = loaded_model(input_id, token_type_ids=None, attention_mask=attention_mask)

    logits = outputs.logits
    predicted_probabilities = torch.sigmoid(logits)

    # Directly extract the probability of the positive class (label 1)
    probability_positive_class = predicted_probabilities[:, 1].item()

    # Get the grammar score
    grammar_score = probability_positive_class

    # Set up grammar score categories
    excellent_threshold = 0.8
    good_threshold = 0.6
    fair_threshold = 0.4
    
    
    #this is for the sentiment analysis
    analyzer = SentimentIntensityAnalyzer()
    
    vs = analyzer.polarity_scores(transcribed_text)
    compound_score = vs['compound']
    sentiment_label = classify_sentiment(compound_score)
    # print("transcribed_text:", transcribed_text)
    # print("Compound Score:", compound_score)
    # print("Sentiment Label:", sentiment_label)
    # print()
    
    
    

    # Classify the grammar score
    if grammar_score >= excellent_threshold:
        suggestion = "Your grammar is excellent! Keep up the good work."
    elif grammar_score >= good_threshold:
        suggestion = "Your grammar is good, but there's always room for improvement. Consider focusing on a few areas."
    elif grammar_score >= fair_threshold:
        suggestion = "Your grammar needs some improvement. Try paying attention to sentence structure and grammar rules."
    else:
        suggestion = "Your grammar needs significant improvement. Consider seeking additional resources or guidance."

    # Write the output to 'bertoutput.txt'
    bertoutput = os.path.join(base_dir, 'media', 'bertoutput.txt')
    with open(bertoutput, 'a') as bertoutput:
        bertoutput.write(f"Grammar Score: {grammar_score}\n")
        bertoutput.write(f"Suggestion: {suggestion}\n")
        bertoutput.write(f"Sentiment Label: {sentiment_label}\n")

    return {'Grammar Score': grammar_score, 'Suggestion': suggestion, 'SentimentLabel': sentiment_label}


