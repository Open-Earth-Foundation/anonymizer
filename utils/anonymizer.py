import spacy
import copy
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Global variables for lazy loading of models
huggingface_ner = None
nlp_en = None
nlp_pt = None
nlp_es = None
nlp_multi = None


def setup_huggingface():
    global huggingface_ner

    if huggingface_ner is None:
        print("Setting up Hugging Face NER pipeline...")
        tokenizer = AutoTokenizer.from_pretrained(
            "Babelscape/wikineural-multilingual-ner"
        )
        model = AutoModelForTokenClassification.from_pretrained(
            "Babelscape/wikineural-multilingual-ner"
        )

        huggingface_ner = pipeline(
            "ner",
            model=model,
            tokenizer=tokenizer,
            aggregation_strategy="simple",
        )


def setup_spacy():
    global nlp_en, nlp_pt, nlp_es, nlp_multi

    if nlp_en is None or nlp_pt is None or nlp_es is None or nlp_multi is None:
        print("Setting up SpaCy models...")
        # Load two different SpaCy models
        nlp_en = spacy.load("en_core_web_sm")  # English model
        nlp_pt = spacy.load("pt_core_news_sm")  # Portuguese model
        nlp_es = spacy.load("es_core_news_sm")  # Spanish model
        nlp_multi = spacy.load("xx_ent_wiki_sm")  # Multi-language model


# Helper function to anonymize text using Hugging Face NER
def anonymize_with_huggingface(text):
    setup_huggingface()
    hf_entities = huggingface_ner(text)

    # Extract entity text and label, and replace recognized entities with <PERSON> or <LOC>
    anonymized_content = text
    for ent in hf_entities:
        if ent["entity_group"] in [
            "PER",
            "LOC",
            "QUANTITY",
        ]:  # Hugging Face entity labels
            anonymized_content = anonymized_content.replace(
                ent["word"], f"<{ent['entity_group']}>"
            )

    return anonymized_content


# Function to merge entities from multiple pipelines
def anonymize_with_multiple_pipelines(text):
    setup_spacy()
    # Process text with each model
    doc_en = nlp_en(text)
    doc_pt = nlp_pt(text)
    doc_es = nlp_es(text)
    doc_multi = nlp_multi(text)

    # Combine the entities from all pipelines, avoid duplicates
    combined_ents = list(doc_en.ents)  # Start with entities from the English model

    # Add non-overlapping entities from the other models
    for doc in [doc_pt, doc_es, doc_multi]:
        combined_ents.extend(ent for ent in doc.ents if ent not in combined_ents)

    # Perform anonymization based on combined entities
    anonymized_content = text
    for ent in combined_ents:
        if ent.label_ in ["PERSON", "GPE", "LOC"]:
            anonymized_content = anonymized_content.replace(ent.text, f"<{ent.label_}>")

    return anonymized_content


# Function to anonymize the messages inside the object
def anonymize_messages_object(data, method="huggingface"):
    # Create a deep copy of the object to avoid mutating the original object
    anonymized_data = copy.deepcopy(data)

    for message in anonymized_data["messages"]:
        if method == "huggingface":
            message["content"] = anonymize_with_huggingface(message["content"])
        elif method == "spacy":
            message["content"] = anonymize_with_multiple_pipelines(message["content"])
        else:
            raise ValueError("Invalid anonymization method specified.")

    return anonymized_data
