from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

tokenizer = AutoTokenizer.from_pretrained(
    "bert-large-uncased-whole-word-masking-finetuned-squad"
)
model = AutoModelForQuestionAnswering.from_pretrained(
    "bert-large-uncased-whole-word-masking-finetuned-squad"
)

def generate_answers(
    context,
    questions
):
    answers = []
    for question in questions:
        inputs = tokenizer.encode_plus(
            question, context, add_special_tokens=True, return_tensors="pt", max_length=1024, truncation=True
        )
        input_ids = inputs["input_ids"].tolist()[0]

        text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
        answer_start_scores, answer_end_scores = model(**inputs)

        answer_start = torch.argmax(
            answer_start_scores
        )  # Get the most likely beginning of answer with the argmax of the score
        answer_end = (
            torch.argmax(answer_end_scores) + 1
        )  # Get the most likely end of answer with the argmax of the score

        answer = tokenizer.convert_tokens_to_string(
            tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end])
        )
        answers.append(answer)
    return answers
