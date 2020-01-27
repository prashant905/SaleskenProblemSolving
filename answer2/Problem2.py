from SemanticSimilarity import SentencesSemanticSimilarity
import numpy as np



def similarpair(lines):
    '''
    Function to find similar pairs of senetence
    :return: list with similar pairs of each sentence
    '''
    pair = []
    for sentence in range(len(lines)):
        seq = str(lines[sentence])
        comp = lines[sentence + 1:len(lines)]
        if not comp:
            break
        test = SentencesSemanticSimilarity(seq, comp)
        score = test.getSimilarity()
        if not np.any(score):
            pair.append([seq, "no_match"])
            continue
        matching = np.argmax(score)
        predicted_text = comp[matching]
        pair.append([seq, predicted_text])
        lines.remove(predicted_text)
    return pair

if __name__ == '__main__':
    with open("list_of_sentences", "r") as fd:
        lines = fd.read().splitlines()
        print(similarpair(lines))