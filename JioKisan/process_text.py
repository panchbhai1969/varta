import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from word2number import w2n

#POS Tags
# CC coordinating conjunction
# CD cardinal digit
# DT determiner
# EX existential there (like: “there is” … think of it like “there exists”)
# FW foreign word
# IN preposition/subordinating conjunction
# JJ adjective ‘big’
# JJR adjective, comparative ‘bigger’
# JJS adjective, superlative ‘biggest’
# LS list marker 1)
# MD modal could, will
# NN noun, singular ‘desk’
# NNS noun plural ‘desks’
# NNP proper noun, singular ‘Harrison’
# NNPS proper noun, plural ‘Americans’
# PDT predeterminer ‘all the kids’
# POS possessive ending parent’s
# PRP personal pronoun I, he, she
# PRP$ possessive pronoun my, his, hers
# RB adverb very, silently,
# RBR adverb, comparative better
# RBS adverb, superlative best
# RP particle give up
# TO, to go ‘to’ the store.
# UH interjection, errrrrrrrm
# VB verb, base form take
# VBD verb, past tense took
# VBG verb, gerund/present participle taking
# VBN verb, past participle taken
# VBP verb, sing. present, non-3d take
# VBZ verb, 3rd person sing. present takes
# WDT wh-determiner which
# WP wh-pronoun who, what
# WP$ possessive wh-pronoun whose
# WRB wh-abverb where, when

#Change this using the database
list_commodity = ['carrots', 'tomatoes', 'potatoes']

commodity_quantity = []
commodity_type = []

#Tree navigation function
def get_nodes(parent):
    for node in parent:
        if (type(node) is nltk.Tree):
            # if node.label() == ROOT:
            #     print("**SENTENCE**")
            #     print("Sentence:", " ".join(node.leaves()))
            # else:
            #     print("Label:", node.label())
            #     print("Leaves:", node.leaves())
            if(node.label() == "Commodity"):
                for word in node.leaves():
                    if(word[0] in list_commodity):
                        commodity_type.append(word)
                    else:
                        commodity_quantity.append(word)
            else:
                get_nodes(node)
            # print("Word:", node)
    # print(commodity_type)
    print(commodity_quantity)
    quantity_string = ""
    for w in commodity_quantity:
        if (w[1] == 'CD'):
            quantity_string += str(w[0])
            quantity_string += " "
        else:
            unit = str(w[0])
    print(quantity_string)
    quantity = w2n.word_to_num(quantity_string)
    # print("Quantity :", quantity)
    #Convert unit to standard format
    kg_synset = wordnet.synset('kilogram.n.01')
    tonne_synset = wordnet.synset('metric_ton.n.01')
    liter_synset = wordnet.synset('liter.n.01')
    dozen_synset = wordnet.synset('twelve.n.01')

    unit_synset = wordnet.synsets(unit)[0]
    if(kg_synset.wup_similarity(unit_synset) >= 0.9):
        unit = 'KG'
    elif(tonne_synset.wup_similarity(unit_synset) >= 0.9):
        unit = 'METRIC TON'
    elif(liter_synset.wup_similarity(unit_synset) >= 0.9):
        unit = 'LITRES'
    elif(dozen_synset.wup_similarity(unit_synset) >= 0.9 or unit == 'dozens'):
        unit = 'DOZENS'
    # print("Unit :", unit)
    # print("Commodity :", commodity_type[0][0])
    return {
        "Quantity": quantity,
        "Unit": unit,
        "Commodity": commodity_type[0][0]
        #Call the list_request here.
    }


def process_content(example_sentence):
    words = word_tokenize(example_sentence)
    try:
        tagged = nltk.pos_tag(words)
        # print(tagged)
        commodity_grammar = r""" Commodity: {<CD>*<NN.*>*} """
        parser = nltk.RegexpParser(commodity_grammar)
        chunked_tree = parser.parse(tagged)
        # chunked_tree.draw()
        #Navigate the Chunked Tree
        data = get_nodes(chunked_tree)
        print(data)
    except Exception as e:
        print(str(e))

process_content("I want to sell two hundred kilo carrots.")