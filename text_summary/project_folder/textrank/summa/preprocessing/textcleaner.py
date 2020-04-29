import string
import unicodedata
import logging
import spacy
# from cube.api import Cube
# cube=Cube(verbose=True)
# cube.load("ja")
nlp = spacy.load('ja_ginza')

logger = logging.getLogger('summa.preprocessing.cleaner')

try:
    from pattern.en import tag
    logger.info("'pattern' package found; tag filters are available for English")
    HAS_PATTERN = True
except ImportError:
    logger.info("'pattern' package not found; tag filters are not available for English")
    HAS_PATTERN = False

import re

from textrank.summa.preprocessing.snowball import SnowballStemmer
from textrank.summa.preprocessing.stopwords import get_stopwords_by_language
from textrank.summa.syntactic_unit import SyntacticUnit


# Utility functions adapted from Gensim v0.10.0:
# https://github.com/RaRe-Technologies/gensim/blob/0.10.0/gensim/utils.py
# https://github.com/RaRe-Technologies/gensim/blob/0.10.0/gensim/parsing/preprocessing.py


SEPARATOR = r"@"
RE_SENTENCE = re.compile('(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)')
AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)\s(\w)")
AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)\s(\w)")
AB_ACRONYM_LETTERS = re.compile("([a-zA-Z])\.([a-zA-Z])\.")
UNDO_AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)" + SEPARATOR + "(\w)")
UNDO_AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)" + SEPARATOR + "(\w)")

STEMMER = None
STOPWORDS = None


def set_stemmer_language(language):
    global STEMMER
    if not language in SnowballStemmer.languages:
        raise ValueError("Valid languages are: " + ", ".join(sorted(SnowballStemmer.languages)))
    STEMMER = SnowballStemmer(language)


def set_stopwords_by_language(language, additional_stopwords):
    global STOPWORDS
    words = get_stopwords_by_language(language)
    if not additional_stopwords:
        additional_stopwords = {}
    STOPWORDS = frozenset({ w for w in words.split() if w } | { w for w in additional_stopwords if w })


def init_textcleanner(language, additional_stopwords):
    set_stemmer_language(language)
    set_stopwords_by_language(language, additional_stopwords)


def split_sentences(text):
    processed = replace_abbreviations(text)
    return [undo_replacement(sentence) for sentence in get_sentences(processed)]

def split_sentences_j(sents):
    return [[entry.word for entry in sent ]for sent in sents]






def replace_abbreviations(text):
    return replace_with_separator(text, SEPARATOR, [AB_SENIOR, AB_ACRONYM])


def undo_replacement(sentence):
    return replace_with_separator(sentence, r" ", [UNDO_AB_SENIOR, UNDO_AB_ACRONYM])


def replace_with_separator(text, separator, regexs):
    replacement = r"\1" + separator + r"\2"
    result = text
    for regex in regexs:
        result = regex.sub(replacement, result)
    return result


def get_sentences(text):
    for match in RE_SENTENCE.finditer(text):
        yield match.group()


# Taken from Gensim
RE_PUNCT = re.compile('([%s])+' % re.escape(string.punctuation), re.UNICODE)
def strip_punctuation(s):
    return RE_PUNCT.sub(" ", s)


# Taken from Gensim
RE_NUMERIC = re.compile(r"[0-9]+", re.UNICODE)
def strip_numeric(s):
    return RE_NUMERIC.sub("", s)


def remove_stopwords(sentence):
    return " ".join(w for w in sentence.split() if w not in STOPWORDS)


def stem_sentence(sentence):
    word_stems = [STEMMER.stem(word) for word in sentence.split()]
    return " ".join(word_stems)


def apply_filters(sentence, filters):
    for f in filters:
        sentence = f(sentence)
    return sentence


def filter_words(sentences):
    filters = [lambda x: x.lower(), strip_numeric, strip_punctuation, remove_stopwords,
               stem_sentence]
    apply_filters_to_token = lambda token: apply_filters(token, filters)
    return list(map(apply_filters_to_token, sentences))

def katakoto(doc):
    katakotoSents = [[entry.lemma_ if "ADP" not in entry.pos_ and "AUX" not in entry.pos_ and "SCONJ" not in entry.pos_ and "PUNCT" not in entry.pos_ else "" for entry in sent ]for sent in doc.stents]
    return katakotoSents

def sentFormatter(doc):
    filtered_sents=[]
    original_sents=[]
    tags=[]
    for sent in doc.sents:
        for token in sent:
            original_sents.append(token.orth_)
            tags.append(token.pos_)
            if "ADP" not in token.upos and "AUX" not in token.upos and "SCONJ" not in token.upos and "PUNCT" not in token.upos:
                filtered_sents.append(token.lemma_)
            else:
                filtered_sents.append("")
    return tags,original_sents, filtered_sents

# Taken from Gensim
def deaccent(text):
    """
    Remove accentuation from the given string.
    """
    norm = unicodedata.normalize("NFD", text)
    result = "".join(ch for ch in norm if unicodedata.category(ch) != 'Mn')
    return unicodedata.normalize("NFC", result)


# Taken from Gensim
PAT_ALPHABETIC = re.compile('(((?![\d])\w)+)', re.UNICODE)
def tokenize(text, lowercase=False, deacc=False):
    """
    Iteratively yield tokens as unicode strings, optionally also lowercasing them
    and removing accent marks.
    """
    if lowercase:
        text = text.lower()
    if deacc:
        text = deaccent(text)
    for match in PAT_ALPHABETIC.finditer(text):
        yield match.group()


def merge_syntactic_units(original_units, filtered_units, tags=None):
    units = []
    for i in range(len(original_units)):
        if filtered_units[i] == '':
            continue

        text = original_units[i]
        token = filtered_units[i]
        tag = tags[i][1] if tags else None
        sentence = SyntacticUnit(text, token, tag)
        sentence.index = i

        units.append(sentence)

    return units

def merge_syntactic_units_j(original_units, filtered_units, tags=None):
    units = []
    for i in range(len(original_units)):
        if filtered_units[i] == '':
            continue

        text = str(original_units[i])
        token = str(filtered_units[i])
        tag = tags[i] if tags else None
        sentence = SyntacticUnit(text, token, tag=tag)
        sentence.index = i

        units.append(sentence)

    return units


def clean_text_by_sentences(text, language="english", additional_stopwords=None):
    """ Tokenizes a given text into sentences, applying filters and lemmatizing them.
    Returns a SyntacticUnit list. """
    init_textcleanner(language, additional_stopwords)
    if language == "japanese":
        sents = nlp(text)
        # original_sentences = split_sentences_j(sents)
        # filtered_sentences = katakoto(sents)
        tags, original_sentences, filtered_sentences = sentFormatter(sents)
        return merge_syntactic_units_j(original_sentences, filtered_sentences,tags)
    else:
        original_sentences = split_sentences(text)
        filtered_sentences = filter_words(original_sentences)
        return merge_syntactic_units(original_sentences, filtered_sentences)


def clean_text_by_word(text, language="english", deacc=False, additional_stopwords=None):
    """ Tokenizes a given text into words, applying filters and lemmatizing them.
    Returns a dict of word -> syntacticUnit. """
    if language == "japanese":
        units = clean_text_by_sentences(text,language="japanese")
    else:
        init_textcleanner(language, additional_stopwords)
        text_without_acronyms = replace_with_separator(text, "", [AB_ACRONYM_LETTERS])
        original_words = list(tokenize(text_without_acronyms, lowercase=True, deacc=deacc))
        filtered_words = filter_words(original_words)
        if HAS_PATTERN:
            tags = tag(" ".join(original_words))  # tag needs the context of the words in the text
        else:
            tags = None
        units = merge_syntactic_units(original_words, filtered_words, tags)
    return { unit.text : unit for unit in units }


def tokenize_by_word(text, deacc=False):
    text_without_acronyms = replace_with_separator(text, "", [AB_ACRONYM_LETTERS])
    return tokenize(text_without_acronyms, lowercase=True, deacc=deacc)
