'''
yeekit translate for free as in beer
'''

import sys
import logging
from typing import Callable, Any, Tuple
import json
from time import time
from random import randint
import pytest  # type: ignore
# import mock
# import urllib3

from ratelimit import limits, sleep_and_retry  # type: ignore
import requests
from fuzzywuzzy import fuzz, process  # type: ignore
import coloredlogs  # type: ignore
from jmespath import search  # type: ignore

# urllib3.disable_warnings()
# logging.captureWarnings(True)
# logging.getLogger('requests.packages.urllib3.connectionpool').level = 30

LOGGER = logging.getLogger(__name__)
FMT = '%(filename)-14s[%(lineno)-3d] %(message)s [%(funcName)s]'
coloredlogs.install(level=20, logger=LOGGER, fmt=FMT)

# en-ar en-zhcn
LANG_CODES = (
    "zh,en,ru,de,fr,pt,ja,es"
).split(',')  # + ['auto']

# zh-ko ko-zh probably only these pairs for ko are supported

URL = 'https://www.yeekit.com/site/dotranslate'

# UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'  # noqa
# HEADERS = {"User-Agent": UA}
HEADERS = {
    'origin': 'https://www.yeekit.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'authority': 'www.yeekit.com',
    'referer': 'https://www.yeekit.com/site/translate?locale=zh',
}

SESS = requests.Session()
SESS.get('https://www.yeekit.com/site/translate', headers=HEADERS)  # , verify=0


def with_func_attrs(**attrs: Any) -> Callable:
    ''' with_func_attrs '''
    def with_attrs(fct: Callable) -> Callable:
        for key, val in attrs.items():
            setattr(fct, key, val)
        return fct
    return with_attrs


@with_func_attrs(text='')
def _yeekit_tr(
        text: str,
        from_lang: str = 'en',
        to_lang: str = 'zh',
        timeout: Tuple[float, float] = (55, 66),
) -> str:
    ''' yeekit_tr

    text = 'test one two three'
    from_lang = 'auto'
    to_lang = 'zh'
    timeout = (55, 66)
    '''

    try:
        from_lang = from_lang.lower()
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("%s", exc)
        from_lang = 'en'
    try:
        to_lang = to_lang.lower()
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("%s", exc)
        to_lang = 'zh'

    if from_lang in ['chinese', 'zhongwen']:
        from_lang = 'zh'
    if to_lang in ['chinese', 'zhongwen']:
        to_lang = 'zh'

    try:
        from_lang = process.extractOne(from_lang, LANG_CODES, scorer=fuzz.UWRatio)[0]  # noqa
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("%s", exc)
        from_lang = 'en'
    try:
        to_lang = process.extractOne(to_lang, LANG_CODES, scorer=fuzz.UWRatio)[0]  # noqa
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("%s", exc)
        to_lang = 'en'

    if from_lang == to_lang:
        LOGGER.warning("from_lang [%s] and to_lang [%s] are the same, returing the origial text", from_lang, to_lang)
        return text

    from_lang = 'n' + from_lang
    to_lang = 'n' + to_lang

    data = {
        'content[]': text,
         'sourceLang': from_lang,
         'targetLang': to_lang,
    }

    try:
        resp = SESS.post(  # type: ignore  # data  # expected "Union[None, bytes, MutableMapping[str, str], IO[Any]]  # noqa
            URL,
            # data=data2,
            data=data,
            headers=HEADERS,
            timeout=timeout,
        )
        resp.raise_for_status()
    except Exception as exc:  # pragma: no cover
        LOGGER.error('%s', exc)

    try:
        # jdata = resp.json()
        jdata = json.loads(resp.json()[0])
    except Exception as exc:  # pragma: no cover
        LOGGER.error('%s', exc)
        jdata = {'error': str(exc)}

    yeekit_tr.text = resp.text

    try:
        # res = search('[0].translations[0].text', jdata)
        # res = search('d.result', jdata)
        res, = search('translation[].translated[].text', jdata)
    except Exception as exc:  # pragma: no cover
        LOGGER.error('%s', exc)
        res = {'error': str(exc)}

    return res


@sleep_and_retry
@limits(calls=30, period=20, raise_on_limit=True)  # raise_on_limit probably superfluous
def _rl_yeekit_tr(*args, **kwargs):
    ''' be nice and throttle'''
    LOGGER.info(' rate limiting 3 calls/2 secs... ')
    return _yeekit_tr(*args, **kwargs)


@with_func_attrs(calls=0, call_tick=-1)
def yeekit_tr(*args, **kwargs):
    ''' exempt first 200 calls from rate limiting '''

    # increase calls unto 210
    if yeekit_tr.calls < 210:
        yeekit_tr.calls += 1

    # reset rate limit if the last call was 2 minutes ago
    tick = time()
    if tick - yeekit_tr.calls > 120:
        yeekit_tr.calls = 1
    yeekit_tr.call_tick = tick

    if yeekit_tr.calls < 200:
        return _yeekit_tr(*args, **kwargs)

    return _rl_yeekit_tr(*args, **kwargs)


def test_simple():
    ''' test simple '''
    res = yeekit_tr('test ', 'en', 'zh')
    assert res == '测试'


@pytest.mark.parametrize(
    'to_lang', LANG_CODES
    # 'to_lang', ['zh', 'de', 'fr', 'it', 'ko', 'ja', 'ru']
)
def test_sanity(to_lang):
    'sanity test'

    numb = str(randint(1, 10000))
    text = 'test ' + numb
    assert numb in yeekit_tr(text, to_lang=to_lang)


def test_calls():
    ''' test calls '''
    calls = yeekit_tr.calls
    _ = yeekit_tr('test ')
    assert yeekit_tr.calls == calls + 1


def main():  # pragma: no cover
    ''' main '''

    text = sys.argv[1:]
    text1 = ''
    if not text:
        print(' Provide something to translate, testing with some random text\n')
        text = 'test tihs and that' + str(randint(1, 1000))
        text1 = 'test tihs and that' + str(randint(1, 1000))

    print(f'{text} translated to:')
    for to_lang in ['zh', 'de', 'fr', ]:
        print(f'{to_lang}: {yeekit_tr(text, to_lang=to_lang)}')
        if not text1:
            print(f'{to_lang}: {yeekit_tr(text1, to_lang=to_lang)}')


def init():
    ''' attempted to pytest __name__ == '__main__' '''
    LOGGER.debug('__name__: %s', __name__)
    if __name__ == '__main__':
        sys.exit(main())


init()

# test_init()
