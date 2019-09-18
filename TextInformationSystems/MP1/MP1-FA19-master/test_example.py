import metapy
import tok as tok
import trigrams as trigrams

def tokens_lowercase(doc):
    #Write a token stream that tokenizes with ICUTokenizer, 
    #lowercases, removes words with less than 2 and more than 5  characters
    #performs stemming and creates trigrams (name the final call to ana.analyze as "trigrams")
    '''Place your code here'''
    print("tokens_lowercase() enter")
    tok = metapy.analyzers.ICUTokenizer()
    # tok = metapy.analyzers.LengthFilter(tok, min=2, max=30)
    # tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    # tok = metapy.analyzers.LengthFilter(tok, min=2, max=30)
    # tok = metapy.analyzers.Porter2Filter(tok)
    # tok = metapy.analyzers.LowercaseFilter(tok)
    # tok.set_content(doc.content())
    # tokens = [token for token in tok]
    #
    # tok = metapy.analyzers.CharacterTokenizer()
    # ana = metapy.analyzers.NGramWordAnalyzer(4, tok)
    # unigrams = ana.analyze(doc)
    # print(unigrams)
    #
    # seq = metapy.sequence.Sequence()
    # for word in ["The", "dog", "ran", "across", "the", "park", "."]:
    #     seq.add_symbol(word)
    # print(seq)
    #
    tagger = metapy.sequence.PerceptronTagger("perceptron-tagger/")
    # tagger.tag(seq)
    # print(seq)

    doc = metapy.index.Document()
    doc.content("I Said that I can't believe that it only costs $19.95!")
    tok = metapy.analyzers.ICUTokenizer()
    tok = metapy.analyzers.PennTreebankNormalizer(tok)
    tok.set_content(doc.content())
    for seq in extract_sequences(tok):
        print(seq)
        tagger.tag(seq)
        print(seq)

    ana = metapy.analyzers.load('config.toml')
    print(ana.analyze(doc))

    #leave the rest of the code as is
    # tok.set_content(doc.content())
    tokens, counts = [], []
    # for token, count in trigrams.items():
    #     counts.append(count)
    #     tokens.append(token)
    print("tokens_lowercase() exit")
    return tokens

def extract_sequences(tok):
    sequences = []
    for token in tok:
        if token == '<s>':
            sequences.append(metapy.sequence.Sequence())
        elif token != '</s>':
            sequences[-1].add_symbol(token)
    return sequences

if __name__ == '__main__':
    metapy.log_to_stderr()
    doc = metapy.index.Document()
    doc.content("I said that I can't believe that it only costs $19.95! I could only find it for more than $30 before.")
    print(doc.content()) #you can access the document string with .content()

    tokens = tokens_lowercase(doc)
    print(tokens)

