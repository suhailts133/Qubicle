import cv2
import pytesseract
import os
import re
import json
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from django.conf import settings

BASE_DIR = settings.BASE_DIR

def combined_function(images_folder):
    # Process images and extract filtered lines
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    nlp = spacy.load("en_core_web_sm")

    # Create 'json' folder if it doesn't exist
    json_folder = os.path.join(BASE_DIR, 'json')
    os.makedirs(json_folder, exist_ok=True)

    # Output JSON file for filtered lines
    filtered_output_json_file = os.path.join(json_folder, 'questions.json')
    
    filtered_results = {}

    # Construct the path to the images folder
    images_folder = os.path.join(BASE_DIR, images_folder)

    for filename in os.listdir(images_folder):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            image_path = os.path.join(images_folder, filename)
            image = cv2.imread(image_path)
            text = pytesseract.image_to_string(image)
            text_without_numerics = re.sub(r'\d', '', text)
            text_cleaned = re.sub(r'^[.,_]+', '', text_without_numerics, flags=re.MULTILINE)
            text_cleaned = re.sub(r'\n+', '\n\n', text_cleaned)
            doc = nlp(text_cleaned)
            organized_text = "\n\n".join([sent.text for sent in doc.sents])
            keywords = ['differentiate', 'what', 'explain', 'how', 'why', 'mention', 'when', 'design', 'discuss', 'write', 'compare', 'describe', 'illustrate', 'state']
            filtered_lines = [re.sub(r'[^a-zA-Z ]', '', line.strip(string.punctuation).strip().replace('_', '').lower()) for line in organized_text.split('\n') if any(line.strip().lower().startswith(keyword) and (line.strip().endswith('.') or line.strip().endswith('?')) for keyword in keywords)]
            filtered_lines = [line for line in filtered_lines if f"File: {filename}" not in line]
            filtered_lines = [line for line in filtered_lines if len(line.split()) > 2]
            filtered_results[filename] = filtered_lines

    with open(filtered_output_json_file, 'w', encoding='utf-8') as filtered_json_file:
        json.dump(filtered_results, filtered_json_file, ensure_ascii=False, indent=2)

    # Preprocess text and perform TF-IDF analysis
    stopwords_path = os.path.join(BASE_DIR, 'scripts', 'stopwords.txt')
    with open(stopwords_path, 'r', encoding='utf-8') as stopword_file:
        additional_stopwords = stopword_file.read().splitlines()
    with open(filtered_output_json_file, 'r', encoding='utf-8') as f:
        filtered_data = json.load(f)

    sentences = [sentence for filename, lines in filtered_data.items() for sentence in lines]

    def preprocess_text(text):
        doc = nlp(text)
        tokens = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop and token.lemma_.lower() not in additional_stopwords]
        return ' '.join(tokens)

    preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_sentences)
    feature_names = vectorizer.get_feature_names_out()

    word_occurrences = {}

    for i, sentence in enumerate(sentences):
        for j, word in enumerate(feature_names):
            tfidf_score = tfidf_matrix[i, j]
            if tfidf_score > 0:
                if word in word_occurrences:
                    word_occurrences[word].append({'sentence': sentence, 'tfidf_score': tfidf_score})
                else:
                    word_occurrences[word] = [{'sentence': sentence, 'tfidf_score': tfidf_score}]

    repeated_output_json_file = os.path.join(json_folder, 'repeated.json')
    with open(repeated_output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(word_occurrences, json_file, ensure_ascii=False, indent=4)

    # Create modified copy of JSON file
    with open(repeated_output_json_file, 'r') as file:
        data = json.load(file)

    keys_to_remove_single = [key for key, value in data.items() if len(value) == 1]
    keys_to_remove_double = [key for key, value in data.items() if len(value) == 2]
    keys_to_remove_more_than_five = [key for key, value in data.items() if len(value) > 5]

    for key in keys_to_remove_single:
        del data[key]

    for key in keys_to_remove_double:
        del data[key]

    for key in keys_to_remove_more_than_five:
        del data[key]

    cleaned_output_json_file = os.path.join(json_folder, 'cleaned.json')
    with open(cleaned_output_json_file, 'w') as output_file:
        json.dump(data, output_file, indent=2)

    cleaned_data = {}
    for key, value in data.items():
        max_tfidf_question = max(value, key=lambda x: x['tfidf_score'])
        cleaned_data[key] = max_tfidf_question['sentence']

    # Combine topics with the same questions
    combined_data = {}

    for topic, question in cleaned_data.items():
        # Remove punctuation and convert to lowercase for comparison
        cleaned_question = ''.join(e for e in question if e.isalnum() or e.isspace()).lower()

        # Check if the question exists in combined_data
        if cleaned_question in combined_data:
            # Combine topics
            combined_data[cleaned_question].append(topic)
        else:
            # Add the question with the corresponding topic
            combined_data[cleaned_question] = [topic]

    # Create a new dictionary with combined topics
    result_data = {}
    for cleaned_question, topics in combined_data.items():
        result_data['_'.join(topics)] = cleaned_question

    # Save the combined data to a new file
    combined_json_path = os.path.join(json_folder, 'final_output.json')
    with open(combined_json_path, 'w', encoding='utf-8') as output_file:
        json.dump(result_data, output_file, indent=2)

    print(f"Results saved in '{combined_json_path}'.")
    return combined_json_path

# Provide the relative path to the folder containing images
# combined_function('media/uploaded_images/')
