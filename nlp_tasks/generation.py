from transformers import pipeline

text_generator = pipeline("text-generation")

def create_generated_text(initial_input, max_length):
    return text_generator(initial_input, max_length=max_length)[0]['generated_text']
