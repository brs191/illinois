import metapy
import tok as tok
import trigrams as trigrams

def tokens_lowercase(doc):
    # Write a token stream that tokenizes with ICUTokenizer,
    # lowercases, removes words with less than 2 and more than 5  characters
    # performs stemming and creates trigrams (name the final call to ana.analyze as "trigrams")
    '''Place your code here'''
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.LengthFilter(tok, min=2, max=5)
    tok = metapy.analyzers.Porter2Filter(tok)
    ana = metapy.analyzers.NGramWordAnalyzer(3, tok)
    trigrams = ana.analyze(doc)

    # leave the rest of the code as is
    tok.set_content(doc.content())
    tokens, counts = [], []
    for token, count in trigrams.items():
        counts.append(count)
        tokens.append(token)
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

