import random
import itertools
import statistics

def genPopulation(popSize, numBits):

	chromosomes = []

	for _ in range(popSize):

		chromosome = ""

		for _ in range(numBits):

			bit = random.randrange(2)
			chromosome += str(bit)

		chromosomes.append(chromosome)

	return chromosomes

def createNextGeneration(parentPop, fitnessScores):

	#Assign fitness scores
	fitnessRouletteCutoffs, bestIndividual, bestFitness, averageFitness = assignFitnessRatios(parentPop, fitnessScores)

	childPop = []

	bestParents  = extractBestParents(parentPop, fitnessScores)

	#Create a child population the same size as the parent population
	for _ in range(len(parentPop) - len(bestParents)):

		#Selection
		selectedPair = selection(parentPop, fitnessRouletteCutoffs)
		#Crossover
		child = crossOver(selectedPair)
		#Mutation
		child = mutation(child)

		childPop.append(child)

	#Combine the best parents from the old generation with the new generation
	childPop = childPop + bestParents

	return childPop, bestIndividual, bestFitness, averageFitness


def assignFitnessRatios(parentPop, fitnessScores):


	#Get data about the fitness scores
	bestFitness = max(fitnessScores)
	bestIndividual = parentPop[fitnessScores.index(bestFitness)]
	totalScore = sum(fitnessScores)
	averageFitness = totalScore/len(fitnessScores)
	
	fitnessRatios = []

	totalScore = sum(fitnessScores)
	#Calculate the fitness ratios
	for score in fitnessScores:
		ratio = score/totalScore
		fitnessRatios.append(ratio)

	fitnessRouletteCutoffs = list(itertools.accumulate(fitnessRatios))

	return fitnessRouletteCutoffs, bestIndividual, bestFitness, averageFitness


def extractBestParents(parentPop, fitnessScores):

	fitnessScoresCopy = fitnessScores.copy()
	fitnessScoresCopy.sort()

	maxIndex = len(fitnessScores) - 1

	bestScoresCutoffIndex = int(maxIndex*(1/2))

	#Get a cutoff value for the median fitness score
	bestScoresCutoff = fitnessScoresCopy[bestScoresCutoffIndex]

	bestParents = []

	#Find the chromsomes with fitness scores above the cutoff
	for i in range(len(parentPop)):

		if fitnessScores[i] > bestScoresCutoff:
			bestParents.append(parentPop[i])

	return bestParents


def selection(parentPop, fitnessRouletteCutoffs):

	pair = []
	
	#Select two individuals randomly from the parent population to mate
	for _ in range(2):

		#Get a random value between 0 and 1
		randVal = random.random()

		for i, cutoff in enumerate(fitnessRouletteCutoffs):
			if randVal < cutoff:
				pair.append(parentPop[i])
				break

	return pair

def crossOver(pair):
	randVal = random.randrange(2)
	startWithFirst = True
	if randVal == 0:
		startWithFirst = False

	numBits = len(pair[0])
	crossOverPoint = random.randrange(numBits)

	#Create child offpsring with crossover
	child = ""
	if startWithFirst:
		#If the crossoverpoint is past the final bit, no need for concatenation
		if crossOverPoint == numBits - 1:
			child = pair[1]
		else:
			child = pair[0][:crossOverPoint] + pair[1][crossOverPoint:]
	else:
		#If the crossoverpoint is past the final bit, no need for concatenation
		if crossOverPoint == numBits - 1:
			child = pair[0]
		else:
			child = pair[1][:crossOverPoint] + pair[0][crossOverPoint:]

	return child

def mutation(chrom):
	MUTATION_RATE = .008
	#Convert the chromsome bit string into a list
	bitList = list(chrom)
	for i,bit in enumerate(bitList):

		randVal = random.random()

		#If the random chance of mutation occured
		if randVal < MUTATION_RATE:
			#Flip the bit
			if bitList[i] == "0":
				bitList[i] = "1"
			else:
				bitList[i] = "0"

	newString = "".join(bitList)

	return newString



