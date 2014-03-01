from sets import Set
import itertools
from itertools import izip
from collections import defaultdict
from nltk import word_tokenize, wordpunct_tokenize
import string
from nltk.corpus import stopwords
import nltk_contrib.align.align_util as align_util
import nltk_contrib.align.align as align
import nltk_contrib.align.distance_measures as distance_measures
import sys



class EMAlgorithm:

	def __init__(self,corpus, dictionary):
		self.ttable = defaultdict(dict)
		self.dictionary = dictionary
		self.corpus = corpus
		self.sentencePairs = []
		self.alignmentProbabilities = {}
		self.uniqWords = []
		self.translatedUniqWords = {}
		self.minIterations = 20
		self.translatedWords = []
		self.spanishStopWords = stopwords.words('spanish')
		self.englishStopWords = stopwords.words('english')


	def hasConverged(self, oldTable, newTable):
		for word in self.uniqWords:
			for translatedWord in self.translatedWords:

				if oldTable[word][translatedWord] != newTable[word][translatedWord]:
					return False
		return True


	def train(self):
		newTTable = defaultdict(dict)
		nIterations = 0
		self.ttable = self.initializeProbabilities()
		while(nIterations < self.minIterations):
			newTTable = defaultdict(dict)
			for sentencePair in self.sentencePairs:
				spanishSentence = sentencePair[0]
				englishSentence = sentencePair[1]
				alignmentProbPairings = sentencePair[2]["alignments"]
				normalizationDenominator = sentencePair[3]
				for alignmentProbPairing in alignmentProbPairings:
					alignment = alignmentProbPairing["alignment"]
					alignmentProbability = 1
					alignmentProbabilities = []
					for englishWordPos, spanishAlignedWord in enumerate(alignment):
						# print englishSentence
						# print spanishSentence
						# print len(englishSentence)
						# print len(spanishSentence)
						if (len(englishSentence) == len(spanishSentence) + 1):
							englishWord = englishSentence[englishWordPos]
							probability = self.ttable[spanishAlignedWord][englishWord]
							alignmentProbability *= probability
					alignmentProbPairing["probability"] = alignmentProbability
					normalizationDenominator += alignmentProbability

				sentencePair[3] = normalizationDenominator



			for sentencePair in self.sentencePairs:
				alignmentProbPairings = sentencePair[2]["alignments"]
				for alignmentProbPairing in alignmentProbPairings:
					alignmentProbPairing["probability"] = alignmentProbPairing["probability"]/float(sentencePair[3])


			for word in self.uniqWords:
				for translatedWord in self.translatedWords:
					for sentencePair in self.sentencePairs:
						alignmentProbPairings = sentencePair[2]["alignments"]
						for alignmentProbPairing in alignmentProbPairings:
							alignment = alignmentProbPairing["alignment"]
							indices = [i for i, x in enumerate(alignment) if x == word]
							for i in indices:
								print(sentencePair[1])
								print(sentencePair[0])
								print(i)
								print("=====")
								alignedWord = sentencePair[1][i]

								if alignedWord == translatedWord:
									if word in newTTable and translatedWord in newTTable[word]:
										newTTable[word][translatedWord] += alignmentProbPairing["probability"]
									else: 
										newTTable[word][translatedWord] = alignmentProbPairing["probability"]
								else:
									if word in newTTable and translatedWord in newTTable[word]:
										newTTable[word][translatedWord] += 0
									else: 
										newTTable[word][translatedWord] = 0

			for word in self.uniqWords:
				rowSum = 0
				for translatedWord in self.translatedWords:
					rowSum += newTTable[word][translatedWord]
				for translatedWord in self.translatedWords:
					newTTable[word][translatedWord] = newTTable[word][translatedWord]/rowSum


			# for k,v in self.ttable.iteritems():
			# 	print k, dict(v)

			# print("==========")
			for k,v in newTTable.iteritems():
				print k, dict(v)


			if(self.hasConverged(self.ttable,newTTable)):
				print("SELF HAS CONVERGED")
				print self.ttable
				return self.ttable

			self.ttable = newTTable
			print self.ttable

			# print("^^^^^^^^^^^^^^^^^^^^^")


			nIterations = nIterations + 1




	def score(self, sentence):
		return 0

	def generateSentencePairings(self,corpus):
		for spanishSentence in self.corpus:
			englishSentence = []
			for word in spanishSentence:
				englishSentence.append(self.dictionary[word])

			englishSentence = englishSentence.translate(string.maketrans("",""), string.punctuation)
			spanishSentence = spanishSentence.translate(string.maketrans("",""), string.punctuation)
			englishSentence  = [i for i in englishSentence if i not in self.englishStopWords]
			spanishSentence = [ i for i in spanishSentence if i not in self.spanishStopWords]

			alignmentList = itertools.permutations(spanishSentence)
			alignmentProbList = []
			for alignment in alignmentList:
				alignmentProbPairing = {"alignment" : alignment, "probability": 0}
				alignmentProbList.append(alignmentProbPairing)
			alignmentObject = {"alignments" : alignmentProbList}
			englishSentence.append("NULL")
			if(len(spanishSentence) == 1 + len(englishSentence)):
				sentencePair = [spanishSentence, englishSentence, alignmentObject, 0]
				self.sentencePairs.append(sentencePair)


	def initializeProbabilities(self):
		nSentences = 500
		i = 0
		with open("englishTestSentence.txt") as englishFile, open("spanishTestSentence.txt") as spanishFile:
			for englishSentence, spanishSentence in zip(englishFile, spanishFile):
				if i == nSentences:
					break
				i = i + 1
				englishSentence = englishSentence.translate(string.maketrans("",""), string.punctuation)
				spanishSentence = spanishSentence.translate(string.maketrans("",""), string.punctuation)
				englishSentence = word_tokenize(englishSentence)
				spanishSentence = wordpunct_tokenize(spanishSentence)
				alignmentList = [itertools.permutations(spanishSentence)]
				alignmentProbList = []
				for alignment in alignmentList:
					alignmentProbPairing = {"alignment" : alignment, "probability": 0}
					alignmentProbList.append(alignmentProbPairing)
				alignmentObject = {"alignments" : alignmentProbList}
				print("LENGTHS")
				print(len(spanishSentence))
				print(len(englishSentence))
				if(len(spanishSentence) == len(englishSentence)):
					sentencePair = [spanishSentence, englishSentence, alignmentObject, 0]
					self.sentencePairs.append(sentencePair)
					self.uniqWords += spanishSentence
					self.translatedWords += englishSentence


		self.uniqWords = list(Set(self.uniqWords))
		self.translatedWords = list(Set(self.translatedWords))

		uniqWordsLen = float((len(self.uniqWords)))

		for word in self.uniqWords:
			for translatedWord in self.translatedWords:
				self.ttable[word][translatedWord] = 1/uniqWordsLen

		return self.ttable

def main():
	corpus = [["casa","verde"],["la", "casa"]]
	dictionary ={ "casa" : "house", "la" : "the", "verde" : "green"}
	# emAlgo =  EMAlgorithm(corpus, dictionary)
	# emAlgo.initializeProbabilities()
	# # emAlgo.generateSentencePairings(corpus)
	# emAlgo.train()
	hard_delimiter = '.EOP'
	soft_delimiter = '.EOS'
	input_file1 = "englishTestSentence.txt.tk"
	input_file2 = "spanishTestSentence.txt.tk"
	gc = align.GaleChurchAligner(distance_measures.two_side_distance, 'original', 'text_tuples', print_flag=True)
	(regions1, regions2) = gc.get_delimited_regions('token', input_file1, input_file2, hard_delimiter, soft_delimiter)
	print regions1
	print regions2
	gc_alignment = gc.batch_align(regions1, regions2)  
	print "Alignment0: %s" % gc_alignment



if __name__ == "__main__":
    main()