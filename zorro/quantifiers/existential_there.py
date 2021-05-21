import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

NUM_ADJECTIVES = 50
NUM_NOUNS = 50

template1 = 'there {} {} {} about {} {} .'
template2 = 'there {} {} {} that {} made .'

plural = inflect.engine()


def main():
    """
    example:
    "there was a documentary about dogs ." vs. "there was each documentary about dogs ."

    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN', num_words_in_sample=NUM_NOUNS)
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    quantifiers_good = ['a', 'no', 'some', 'many', 'few']
    quantifiers_bad = ['each', 'most', 'all', 'every']

    template1_subjects_s_and_p = [
        ('movie', 'movies'),
        ('book', 'books'),
        ('story', 'stories'),
        ('sign', 'signs'),
    ]

    vowels = {'a', 'e', 'i', 'o', 'u'}

    copula_p = ['were', 'are', "weren't", 'are not']
    copula_s = ['was', 'is', 'was not', 'is not']

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    while True:

        # random choices
        noun_s, noun_p = random.choice(nouns_s_and_p)
        adj = random.choice(adjectives)
        quantifier_b = random.choice(quantifiers_bad)
        quantifier_g = random.choice(quantifiers_good)
        subj_s, sub_p = random.choice(template1_subjects_s_and_p)
        name = random.choice(names)

        # plural vs. singular copula
        if quantifier_g in {'some', 'many', 'few'}:
            copula = random.choice(copula_p)
            subj1 = sub_p   # for template 1
            subj2 = noun_p  # for template 2
        else:
            copula = random.choice(copula_s)
            subj1 = subj_s
            subj2 = noun_s

        # "a" vs. "an"
        if subj1[0] in vowels and quantifier_g == 'a':
            quantifier_g = 'an'

        # prevent double negation
        if quantifier_g == 'no' and 'not' in copula:
            copula = copula.replace(' not', '')

        yield template1.format(copula, quantifier_b, subj1, adj, noun_p)  # bad
        yield template1.format(copula, quantifier_g, subj1, adj, noun_p)  # good

        yield template2.format(copula, quantifier_b, subj2, name)  # bad
        yield template2.format(copula, quantifier_g, subj2, name)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
