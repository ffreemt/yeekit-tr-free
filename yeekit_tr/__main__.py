''' __main__, to run:
python -m yeekit_tr
'''
import sys
from random import randint

from yeekit_tr import yeekit_tr, LANG_CODES


# pragma: no cover
def main():
    '''main'''

    from_lang = 'auto'
    to_lang = 'zh'
    text = 'test ' + str(randint(0, 10000))

    if not sys.argv[1:]:
        print('Provide some English text, with an optional to_lang')
        print('E.g., python -m yeekit_tr test this and that de')
        print('Testing with some random text\n')
    else:
        argv = sys.argv[1:]
        len_ = len(argv)

        if len_ == 1:
            if argv[0] in LANG_CODES:
                to_lang = argv[0]
            else:
                text = argv[0]
        elif argv[-1] in LANG_CODES:
            to_lang = argv[-1]
            text = ' '.join(argv[:-1])
        else:
            text = ' '.join(argv)

    for to_lang in ['zh', 'de', 'fr', 'it', 'es']:
        resu = yeekit_tr(text, from_lang, to_lang)
        print(f'[{text}] translated to [{to_lang}]: [{resu}]')


if __name__ == '__main__':
    main()
