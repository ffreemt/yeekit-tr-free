# yeekit-tr-free

Yeekit translate for free: be gentle and rate-limit to 3 calls/2 seconds, first 200 calls exempted

### Installation

```pip install -U yeekit-tr-free```

or

* Install (pip or whatever) necessary requirements, e.g. ```
pip install requests fuzzywuzzy pytest jmespath coloredlogs``` or ```
pip install -r requirements.txt```
* Drop the file yeekit_tr.py in any folder in your PYTHONPATH (check with import sys; print(sys.path)
* or clone the repo (e.g., ```git clone https://github.com/ffreemt/yeekit-tr-free.git``` or download https://github.com/ffreemt/yeekit-tr-free/archive/master.zip and unzip) and change to the yeekit-tr-free folder and do a ```
python setup.py develop```

### Usage

```
from yeekit_tr import yeekit_tr

print(yeekit_tr('hello world', to_lang='zh'))  # ->'你好世界'
print(yeekit_tr('hello world', to_lang='de'))  # ->'Hallo Welt'
print(yeekit_tr('hello world', to_lang='fr'))  # ->'Bonjour le monde'
print(yeekit_tr('hello world', to_lang='ja'))  # ->'ハローワールド'
print(yeekit_tr('Diese sind Teste', 'de', 'zh'))  # ->'这是测试'
print(yeekit_tr('Diese sind Teste', 'de', 'en'))  # ->'These are tests'
```

Languages supported: ar, ca, zhcn, nl, fi, fr, de, el, he, hi, it, ja, kk, ko, pt, ru, es, tr, uk.
Consult the official website for details.

### Acknowledgments

* Thanks to everyone whose code was used
