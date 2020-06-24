"""
Score predictions made by BERT.
calculate 5 measures,
 each quantifying the proportion of model-predictions that correspond to a particular kind of answer:
1. correct noun number
2. false noun number
3. ambiguous noun number ("sheep", "fish")
4. non-noun
5. [UNK] (this means "unknown", which means the model doesn't want to commit to an answer)
it can handle a file that has sentences with different amounts of adjectives (1, 2, 3) .
And sentences with "look at ..." and without.
"""
from pathlib import Path

from babeval.visualizer import Visualizer
from babeval.scoring import score_predictions
from babeval.io import get_group2predictions_file_paths

DUMMY = True

task_name = Path(__file__).parent.name
group2predictions_file_paths = get_group2predictions_file_paths(DUMMY, task_name)

start_words_singular = ["this", "that"]
start_words_plural = ["these", "those"]
start_words = start_words_singular + start_words_plural

templates = ['Sentence with 1 Adjective(s)',
             'Sentence with 2 Adjective(s)',
             'Sentence with 3 Adjective(s)',
             ]

prediction_categories = ("[UNK]", "correct\nnoun", "false\nnoun", "ambiguous\nnoun", "non-noun")

# load word lists
with (Path().cwd() / 'nouns_annotator2.txt').open() as f:
    nouns_list = f.read().split("\n")
with (Path().cwd() / 'nouns_singular_annotator2.txt').open() as f:
    nouns_singular = f.read().split("\n")
with (Path().cwd() / 'nouns_plural_annotator2.txt').open() as f:
    nouns_plural = f.read().split("\n")
with (Path().cwd() / 'nouns_ambiguous_number_annotator2.txt').open() as f:
    ambiguous_nouns = f.read().split("\n")

assert '[NAME]' in nouns_singular

for w in nouns_singular:
    assert w not in nouns_plural

for w in nouns_plural:
    assert w not in nouns_singular


def categorize_templates(test_sentence_list):

    res = {}
    for sentence in test_sentence_list:
        predicted_noun = sentence[-2]
        for word in sentence:
            if word in start_words:
                start_word = word
                adj = sentence[sentence.index(start_word) + 1:sentence.index(predicted_noun)]

                if len(adj) == 1:  # 1 adjective
                    res.setdefault(templates[0], []).append(sentence)

                if len(adj) == 2:  # 2 adjectives
                    res.setdefault(templates[1], []).append(sentence)

                if len(adj) == 3:  # 3 adjectives
                    res.setdefault(templates[2], []).append(sentence)

                break  # exit inner for loop

    return res


def categorize_predictions(test_sentence_list):
    res = {'u': [], 'c': [], 'f': [], 'a': [], 'n': []}

    for sentence in test_sentence_list:
        predicted_word = sentence[-2]
        start_word = [w for w in sentence if w in start_words][0]

        # [UNK]
        if predicted_word == "[UNK]":
            res['u'].append(sentence)

        # correct Noun Number
        elif predicted_word in nouns_plural and start_word in start_words_plural:
            res['c'].append(sentence)

        elif predicted_word in nouns_singular and start_word in start_words_singular:
            res['c'].append(sentence)

        # false Noun Number
        elif predicted_word in nouns_plural and start_word in start_words_singular:
            res['f'].append(sentence)

        elif predicted_word in nouns_singular and start_word in start_words_plural:
            res['f'].append(sentence)

        # Ambiguous Noun
        elif predicted_word in ambiguous_nouns:
            res['a'].append(sentence)

        # Non_Noun
        else:
            res['n'].append(sentence)

    return res


def print_stats(sentences):
    num_singular = 0
    num_plural = 0
    num_ambiguous = 0
    num_total = 0
    for s in sentences:
        for w in s:
            if w in nouns_list:
                num_total += 1
                if w in nouns_singular:
                    num_singular += 1
                elif w in nouns_plural:
                    num_plural += 1
                elif w in ambiguous_nouns:
                    num_ambiguous += 1
                else:
                    raise RuntimeError(f'{w} is neither in plural or singular or ambiguous nouns list')
    print(f'Sing: {num_singular / num_total:.2f} Plural: {num_plural / num_total:.2f}')


# score
template2group_name2props = score_predictions(group2predictions_file_paths,
                                              templates,
                                              categorize_templates,
                                              categorize_predictions,
                                              print_stats)

# plot
visualizer = Visualizer()
visualizer.make_barplot(prediction_categories, template2group_name2props)