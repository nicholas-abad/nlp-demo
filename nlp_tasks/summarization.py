from transformers import pipeline

summarizer = pipeline("summarization")

def summarize_article(input_article):
    return summarizer(input_article, max_length=130, min_length=30)
