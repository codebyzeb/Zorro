import random

from zorro.filter import collect_unique_pairs
from zorro.vocab import get_vocab_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template = '{} {} {} {} .'


def main():
    """
    example:
    "a big dog fell down the stairs ." vs. "a big dog fallen down the stairs ."

    """

    vocab = get_vocab_words()
    modifiers = ['over there', 'some time ago', 'this morning', 'at home', 'last night']

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    irr_over_args = [

        # Overregularised present
        ('fell', 'falled', ['down the stairs']),
        ('went', 'goed', ['to the store', 'to the theater', 'down the road']),
        ('made', 'maked', ['a lot of things', 'something', 'a bird']),
        ('threw', 'throwed', ['his ball', 'the paper ball', 'the trash out', 'some away']),
        ('dreamt', 'dreamed', ['nice things', 'something sweet']),
        ('took', 'taked', ['a paper', 'some food', 'the bell', 'it', 'them']),
        ('eat', 'eated', ['a lot', 'more than me', 'some ice cream']),
        ('drew', 'drawed', ['a picture', 'a map', 'a round circle']),
        ('did', 'doed', ['nothing wrong', 'something bad', 'the best she could ']),
        ('caught', 'catched', ['her ball', 'a bird', 'it']),
        ('heard', 'heared', ['the song', 'a nice story', 'my favorite song']),
        ('grew', 'growed', ['quickly']),
        ('broke', 'breaked', ['the bowl', 'the table', 'the plate']),
        ('blew', 'blowed', ['out the candle', 'away the dirt']),
        ('woke', 'waked', ['up the baby', 'the dog']),
        ('bought', 'buyed', ['a horse', 'a cart', 'some milk']),
        ('came', 'comed', ['to the store', 'just in time', 'when we needed her', 'too late']),
        ('told', 'telled', ['me a story', 'her a secret']),
        ('did', 'doed', ['that very well', 'that yesterday', 'something']),

        # Overregularised past
        ('got', 'gotted', ['a bird', 'a dog', 'some juice']),
    ]

    while True:

        # random choices
        name = random.choice(names)
        mod = random.choice(modifiers)
        irr, over, args = random.choice(irr_over_args)
        arg = random.choice(args)

        # if (vbd not in vocab or vbn not in vocab) or vbd == vbn:
            # print(f'"{verb_base:<22} excluded due to some forms not in vocab')
        #     continue
        if arg == '':
            continue

        # vbd is correct
        yield template.format(name, over, arg, mod)  # bad
        yield template.format(name, irr, arg, mod)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
