from transformers import pipeline

unmasker = pipeline("fill-mask", model="bert-base-german-cased")


def sentence_correction(sentence: str):
    print(f"Original Sentence: {sentence} \n")
    delimeter = " "
    sentence = sentence.split(delimeter)
    all_recommendations = []
    for idx, original_word in enumerate(sentence):
        masked_sentence_list = sentence.copy()
        masked_sentence_list[idx] = "[MASK]"
        masked_sentence = delimeter.join(masked_sentence_list)
        # print(f'  Masked Sentence: {masked_sentence}')
        sentence_recommendations = _get_masked_sentence_results(
            masked_sentence, original_word
        )
        all_recommendations.extend(sentence_recommendations)
        # print('---------')
    return all_recommendations


def _get_masked_sentence_results(masked_sentence, original_word, max_difference=0.3):
    unmasked_list = unmasker(masked_sentence)
    true_score = 0
    better_word_replacements = []
    better_word_replacement_scores = []

    sentence_recommendations = []

    for potential_replacement in unmasked_list:
        # unmasked_sentence is in sorted order from highest score to lowest score.
        if potential_replacement["token_str"] == original_word:
            true_score = float(potential_replacement["score"])
            break

    sentence_and_score_list = [
        (word["token_str"], word["score"], word["sequence"])
        for word in unmasked_list
        if word["score"] - true_score > max_difference
    ]
    # print(f"    Score for original word {original_word.upper()} is {true_score}")

    for idx in range(len(sentence_and_score_list)):
        # print(f"      Recommended word/score/sentence: {sentence_and_score_list[idx]}")
        sentence_recommendations.append(
            sentence_and_score_list[idx][2].replace("[CLS]", "").replace("[SEP]", "")
        )

    return sentence_recommendations
