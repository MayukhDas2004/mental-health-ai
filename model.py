from transformers import pipeline

classifier = pipeline("sentiment-analysis")

MENTAL_MAP = {
    'POSITIVE': '😊 Normal/Good',
    'NEUTRAL': '😐 Mild Stress', 
    'NEGATIVE': '😟 Depression/High Stress'
}

def predict_mental_health(text):
    result = classifier(text)[0]
    emotion = MENTAL_MAP.get(result['label'], result['label'])
    confidence = result['score']
    return {
        'emotion': emotion,
        'confidence': f"{confidence:.1%}",
        'risk_level': 'HIGH' if confidence > 0.9 and result['label']=='NEGATIVE' else 'LOW'
    }

if __name__ == "__main__":
    tests = [
        "I am so stressed about work",
        "Feeling great today!",
        "I want to give up on life"
    ]
    
    for text in tests:
        result = predict_mental_health(text)
        print(f"Text: {text}")
        print(f"Result: {result}")
        print("---")