# Analyzes a word or string of words and returns a negtive value, 0, or positive value
# if that word or string of words is identified as having a negative, neutral,
# or positive connotation, resplectively.


import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # open texts and skip to first words in each
        pfile = open(positives)
        nfile = open(negatives)
        skip(pfile)
        skip(nfile)

        # stores words from both files to instance variables
        self.pwords = []
        self.nwords = []
        for line in pfile:
            self.pwords.append(line.rstrip('\n'))
        for line in nfile:
            self.nwords.append(line.rstrip('\n'))

        # close files
        pfile.close()
        nfile.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokens = nltk.word_tokenize(text)
        score = 0
        for i in tokens:
            if text in self.pwords:
                score += 1
            elif text in self.nwords:
                score -= 1
        return score

# specific for the dictionaries provided in pset6/sentiments
def skip(file):
    for i in range(0, 35):
        file.readline()
