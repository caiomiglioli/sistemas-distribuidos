import csv
import spacy

def tw2dict(header, tw):
    res = dict()
    for i, head in enumerate(header):
        res[head] = tw[i]
    return res

cloud = list()

with open('tweet_data.csv', newline='') as tws:
    _reader = csv.reader(tws)
    header = None
    nlp = spacy.load("en_core_web_sm")

    for i, tw in enumerate(_reader):            
        if i == 0:
            header = tw
            continue

        t = tw2dict(header, tw)

        doc = nlp(t['text'].lower())

        for token in doc:
            if not token.is_stop:
                cloud.append(token.text)
    #end for

    with open('cloud.txt', 'w') as f:
        f.write(' '.join(cloud))