class EMAlgorithm2:
	## THIS PSUEDO CODE FROM Kevin Knight: A Statistical MT Tutorial Workbook helped a LOT
	# ## initialize t(e|f) uniformly
 # do until convergence
 #   set count(e|f) to 0 for all e,f
 #   set total(f) to 0 for all f
 #   for all sentence pairs (e_s,f_s)
 #     set total_s(e) = 0 for all e
 #     for all words e in e_s
 #       for all words f in f_s
 #         total_s(e) += t(e|f)
 #     for all words e in e_s
 #       for all words f in f_s
 #         count(e|f) += t(e|f) / total_s(e)
 #         total(f)   += t(e|f) / total_s(e)
 #   for all f
 #     for all e
 #       t(e|f) = count(e|f) / total(f)

 # When I ran into problems I looked at the implementation in https://github.com/ruaridht/mt-em/blob/master/mtass2.py
 # I DID NOT copy this - my approach is different (and I think shorter) - which is why I implemented the horribly long
 # version first, which is included for reference. 
 #
 from sets import Set
 import string

	def __init__():
		self.englishSentences = []
		self.spanishSentences = []
		self.englishUniqWords = {}
		self.spanishUniqWords = {}
		self.sentencePairs = {}
		self.ttable = defaultdict(dict)
		self.countsEGivenS = {}
		self.totalSpanish = 0
		self.wordPossibilitiesMapping = {}
		self.minIterations = 50
		self.denominatorForSpanish = {}

	def createDictionariesAndSentencePairs(self):
		with open("englishAligned.txt") as englishFile, open("spanishAligned.txt") as spanishFile:
			for englishSentence, spanishSentence in zip(englishFile, spanishFile):
				englishSentence = englishSentence.translate(string.maketrans("",""), string.punctuation)
				spanishSentence = spanishSentence.translate(string.maketrans("",""), string.punctuation) # remove punctuation
				self.englishUniqWords += englishSentence.split()
				self.spanishUniqWords += spanishSentence.split()
				self.englishSentences.append(englishSentence)
				self.spanishSentences.append(spanishSentence)
				self.sentencePairs.append((englishSentence, spanishSentence))
		self.englishUniqWords = list(Set(self.englishUniqWords))
		self.spanishUniqWords = list(Set(self.spanishUniqWords))

	def initTTable(self):
		#The algorithm initializes by associating every spanish word with an english aligned word.
		#As every spanish word can align to a word in its sentence, I go through all the spanish words
		#take the english sentences that are paired with a spanish sentence that contains those words.
		#Add up all of the lengths of those sentences and take that as what I need to divide by. 

		for word in self.spanishUniqWords:
			possibleWordAlignments = []

			for sentencePair in self.sentencePairs:
				englishSentence = sentencePair[0]
				spanishSentence = sentencePair[1]

				if word in spanishSentence:
					possibleWordAlignments = possibleWordAlignments.append(englishSentence.split())

				possibleWordAlignments = list(Set(possibleWordAlignments))
				self.wordPossibilitiesMapping[word] = possibleWordAlignments

		for word in self.spanishUniqWords:
			if len(self.wordPossibilitiesMapping[word]) != 0:
				probability = 1.0/float(len(self.wordPossibilitiesMapping[word]))
				for englishWord in self.englishUniqWords:
					self.ttable[word][englishWord] = probability


	def train(self):
		iteration = 0
		while(iteration < self.minIterations):
			for sentencePair in self.sentencePairs:
				englishSentence = sentencePair[0].split()
				spanishSentence = sentencePair[1].split()

				for englishWord in englishSentence:
					self.denominatorForSpanish[englishWord] = 0
					for spanishWord in spanishSentence:
						proabability = self.ttable[spanishWord]
						self.denominatorForSpanish += probability

				for 









