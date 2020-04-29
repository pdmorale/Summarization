import re
from collections import Counter
import spacy
from MyGraphShow import GraphShow
from pathlib import Path
from summa import keywords
from summa.summarizer import summarize
from simpleTextrank import TextRank

nlp=spacy.load("en_core_web_sm")
class NewsMining():
    """News Mining"""
    def __init__(self,content, filePath,filename,TranslateE2J=False):
        self.fullPath = filePath + filename
        self.TranslateE2J = TranslateE2J
        self.textranker = TextRank()
        self.content = content
        self.ners_label = ['PERSON', 'ORG', 'GPE','DATE','TIME','NP']
        self.ner_dict = {}
        self.ner_dict_orig = {
            'PERSON': 'Person',  # People, including fictional
            'ORG': 'Organization',  # Companies, agencies, institutions, etc.
            'GPE': 'Location',  # Countries, cities, states.
            'DATE': 'When',  # Countries, cities, states.
            'TIME': 'When',
            'NP': 'Topic'
        }
        # dependency markers for subjects
        self.SUBJECTS = {"nsubj", "nsubjpass",
                        "csubj", "csubjpass", "agent", "expl"}
        # dependency markers for objects
        self.OBJECTS = {"dobj", "dative", "attr", "oprd"}
        self.words_postags = []  # token and its POS tag
        self.ner_sents = []      # store sentences which contain NER entity
        self.ners = []           # store all NER entity from whole article
        self.triples = []        # store subject verb object
        self.events = []         # store self.events
        self.word_dict = []
        self.impt_sents = []


        # self.impt_sents = summarize(self.content, ratio=0.5)
        # 01 remove linebreaks and brackets
        if "(" in self.content:
            self.content= self.content.replace("(","\n").replace(")","\n").replace(";","\n")

        self.impt_sents = summarize(self.content, words=50).split("\n")
        self.remove_noisy()
        self.clean_spaces()
        # self.keywords = (keywords.keywords(self.content)).split("\n")
        # 02 split to sentences
        self.doc = nlp(self.content)
        

        for i, sent in enumerate(self.doc.sents):
            for token in sent:
                self.words_postags.append([token.text, token.pos_])
            # words = [token.text for token in sent]
            # postags = [token.pos_ for token in sent]
            ents = nlp(sent.text).ents  # NER detection
            collected_ners = self.collect_ners(ents)

            if collected_ners:  # only extract self.triples when the sentence contains 'PERSON', 'ORG', 'GPE'
                triple = self.extract_triples(sent)
                if not triple:
                    continue
                self.triples += triple
                self.ners += collected_ners
                sent_doc = nlp(str(sent))
                self.ner_sents.append([token.text + '/' + token.label_ for token in sent_doc.ents])

        # 03 get keywords
        #keywords = [i[0] for i in self.extract_keywords(self.words_postags)]
        # self.word_dict = [i for i in Counter([i[0] for i in self.words_postags if i[1] in ['NOUN'] and len(i[0]) > 1])]
        self.keywords = [i[0] for i in self.extract_keywords(self.words_postags)]
       
        for keyword in self.keywords:
           # if keyword in filtered_words:
           if self.content.count(keyword) and len(keyword)>1:
                name = keyword
                cate = 'keywords'
                self.events.append([name, cate])

        # 04 add self.triples to event only the word in keyword
        for t in self.triples:
            if (t[0] in self.keywords or t[1] in self.keywords) and len(t[0]) > 1 and len(t[1]) > 1:
                self.events.append([t[0], t[1]])

        # 05 get word frequency and add to self.events
        # for wd in self.word_dict:
        #     name = wd[0]
        #     cate = 'frequency'
        #     self.events.append([name, cate])

        for ImpSent in self.impt_sents:
            if "To:" in ImpSent or "Cc:" in ImpSent or "-san" in ImpSent or "From:" in ImpSent:
                continue
            if len([[token.text for token in sent] for sent in nlp(ImpSent).sents][0])>3:
                    name = ImpSent
                    cate = 'Text'
                    self.events.append([name, cate])
        # 06 get NER from whole article
        self.ner_dict = {i[0]: i[1] for i in Counter(self.ners).most_common(20)}
        for ner in self.ner_dict:
            name = ner.split('/')[0]  # Jessica Miller
            cate = self.ner_dict_orig[ner.split('/')[1]]  # PERSON
            if len(name)>1:
                self.events.append([name, cate])

        # 07 get all NER entity co-occurrence information
        # here ner_dict is from above 06
        co_dict = self.collect_coexist()
        co_events = [[i.split('@')[0].split(
            '/')[0], i.split('@')[1].split('/')[0]] for i in co_dict]
        self.events += co_events

    def clean_spaces(self):
        self.content = self.content.replace('\r', '').replace('\t', ' ').replace('\n', ' ')


    def remove_noisy(self):
        """Remove brackets"""
        p1 = re.compile(r'（[^）]*）')
        p2 = re.compile(r'\([^\)]*\)')
        self.content = p2.sub('', p1.sub('', self.content))


    def collect_ners(self, ents):
        """Collect token only with PERSON, ORG, GPE"""
        collected_ners = []
        for token in ents:
            if token.label_ in self.ners_label:
                collected_ners.append(token.text + '/' + token.label_)
        return collected_ners
    
    def shortner(self,inputSent):
        short = inputSent.replace("I "," ").replace(" the "," ").replace(" at ","@").replace(" to ","2").replace(" you "," u ").replace(" and ","&").replace("be ","B").replace(" a "," ")
        return short

    def conll_syntax(self, sent):
        """Convert one sentence to conll format."""

        tuples = list()
        for word in sent:
            if word.head is word:
                head_idx = 0
            else:
                head_idx = word.head.i + 1
            tuples.append([word.i + 1,  # Current word index, begin with 1
                           word.text,  # Word
                           word.lemma_,  # Lemma
                           word.pos_,  # Coarse-grained tag
                           word.tag_,  # Fine-grained tag
                           '_',
                           head_idx,  # Head of current  Index
                           word.dep_,  # Relation
                           '_', '_'])
        return tuples

    def getKeywords(self):
        return self.keywords
    def getWord_postags(self):
        return self.words_postags
    def getEvents(self):
        return self.events
    def getWord_dict(self):
        return self.word_dict
    def getNer_dict(self):
        return self.ner_dict
    def getNers(self):
        return self.ners
    def getImp_sent(self):
        return self.impt_sents

    def syntax_parse(self, sent):
        """Convert one sentence to conll format."""
        tuples = list()
        for word in sent:
            if word.head is word:
                head_idx = 0
            else:
                head_idx = word.head.i + 1
            tuples.append([word.i + 1,  # Current word index, begin with 1
                           word.text,  # Word
                           word.pos_,  # Coarse-grained tag
                           word.head,
                           head_idx,  # Head of current  Index
                           word.dep_,  # Relation
                           ])
        return tuples

    def build_parse_chile_dict(self, sent, tuples):
        child_dict_list = list()
        for word in sent:
            child_dict = dict()
            for arc in tuples:
                if arc[3] == word:
                    if arc[-1] in child_dict:
                        child_dict[arc[-1]].append(arc)
                    else:
                        child_dict[arc[-1]] = []
                        child_dict[arc[-1]].append(arc)
            child_dict_list.append([word, word.pos_, word.i, child_dict])
        return child_dict_list

    def complete_VOB(self, verb, child_dict_list):
        '''Find VOB by SBV'''
        for child in child_dict_list:
            word = child[0]
            # child_dict: {'dobj': [[7, 'startup', 'NOUN', buying, 5, 'dobj']], 'prep': [[8, 'for', 'ADP', buying, 5, 'prep']]}
            child_dict = child[3]
            if word == verb:
                for object_type in self.OBJECTS:  # object_type: 'dobj'
                    if object_type not in child_dict:
                        continue
                    # [7, 'startup', 'NOUN', buying, 5, 'dobj']
                    vob = child_dict[object_type][0]
                    obj = vob[1]  # 'startup'
                    return obj
        return ''
    
    def extract_triples(self, sent):
        svo = []
        tuples = self.syntax_parse(sent)
        child_dict_list = self.build_parse_chile_dict(sent, tuples)
        for tuple in tuples:
            rel = tuple[-1]
            if rel in self.SUBJECTS:
                sub_wd = tuple[1]
                verb_wd = tuple[3]
                obj = self.complete_VOB(verb_wd, child_dict_list)
                subj = sub_wd
                verb = verb_wd.text
                if not obj:
                    svo.append([subj, verb])
                else:
                    svo.append([subj, verb+' '+obj])
        return svo

    def extract_keywords(self, words_postags):
        return self.textranker.extract_keywords(words_postags, 10)

    def collect_coexist(self):
        """Construct NER co-occurrence matrices"""
        co_list = []
        ner_dictKeyList = list(self.ner_dict.keys())
        for words in self.ner_sents:
            co_ners = set(ner_dictKeyList).intersection(set(words))
            co_info = self.combination(list(co_ners))
            co_list += co_info
        if not co_list:
            return []
        return {i[0]: i[1] for i in Counter(co_list).most_common()}
    
    
    

    def combination(self, a):
        '''list all combination'''
        combines = []
        if len(a) == 0:
            return []
        for i in a:
            for j in a:
                if i == j:
                    continue
                combines.append('@'.join([i, j]))
        return combines
    def saveHTML(self):
        # 08 show event graph
        self.graph_shower = GraphShow(self.fullPath,self.events,TranslateE2J=self.TranslateE2J)
        self.graph_shower.create_page()


def textToDgram(content,filePath,name):
    Miner = NewsMining(content,filePath,name)
    if Miner == None:
        return ""
    else:
        Miner.saveHTML()
    return Miner.fullPath