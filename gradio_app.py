#from transformers import pipeline

def initialize_ner_pipeline():
    ner_pipeline = pipeline(
        "ner",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple"
    )
    print("✅ Hugging Face NER Model Initialized Successfully!")
    return ner_pipeline

def initialize_classifier_pipeline():
    classifier_pipeline = pipeline(
        "zero-shot-classification",
        model='facebook/bart-large-mnli'
    )
    print("✅ Hugging Face Zero-Shot Classifier Initialized Successfully!")
    return classifier_pipeline

def get_entities(text, ner_pipeline):
    entities = ner_pipeline(text[:3000]) # Limit input text for NER for performance

    people = set()
    organizations = set()
    locations = set()

    for entity in entities:
        if entity["entity_group"] == "PER":
            people.add(entity["word"])
        elif entity["entity_group"] == "ORG":
            organizations.add(entity["word"])
        elif entity["entity_group"] == "LOC":
            locations.add(entity["word"])

    result = f"""
👤 People
{', '.join(people) if people else 'None'}

🏢 Organizations
{', '.join(organizations) if organizations else 'None'}

📍 Locations
{', '.join(locations) if locations else 'None'}
"""

    return result

def classify_document(text, classifier_pipeline):
    labels = [
        "Research Paper",
        "Resume",
        "Legal contract",
        "Medical Report",
        "News Article",
        "Business Report",
        "Technical Documentation",
        "Education Material"
    ]
    result = classifier_pipeline(
        text[:2000], # Limit input text for classification for performance
        candidate_labels=labels
    )
    return f"{result['labels'][0]} ({result['scores'][0]:.2%})"