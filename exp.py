import spacy

nlp = spacy.load("en_core_web_sm")

user_input = input("Enter your query: ")
doc = nlp(user_input)
    
intent = extract_intent(doc)
entities = extract_entities(doc)

context = fetch_context(intent, entities)