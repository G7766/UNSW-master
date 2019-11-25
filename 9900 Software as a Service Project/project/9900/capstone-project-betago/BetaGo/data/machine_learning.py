import os
import json


db = {'unsupervised learning': {
	'description': 'Unsupervised learning is where you only have input data (X) and no corresponding output variables. \
	The goal for unsupervised learning is to model the underlying structure or distribution in the data in order to learn more about the data. \
	These are called unsupervised learning because unlike supervised learning above there is no correct answers and there is no teacher. \
	Algorithms are left to their own devises to discover and present the interesting structure in the data. \
	Unsupervised learning problems can be further grouped into clustering and association problems.',
	'example': '1.k-means for clustering problems, 2.Apriori algorithm for association rule learning problems'
	},

	'supervised learning':{
	'description': 'Supervised learning is where you have input variables (x) and an output variable (Y) and you use an algorithm to learn the mapping function from the input to the output. \
	The goal is to approximate the mapping function so well that when you have new input data (x) that you can predict the output variables (Y) for that data. \
	It is called supervised learning because the process of an algorithm learning from the training dataset can be thought of as a teacher supervising the learning process. \
	We know the correct answers, the algorithm iteratively makes predictions on the training data and is corrected by the teacher. Learning stops when the algorithm achieves an acceptable level of performance. \
	Supervised learning problems can be further grouped into regression and classification problems.',
	'example':  '1.Linear regression for regression problems, 2.Random forest for classification and regression problems, 3. Support vector machines for classification problems'
	},

	'k-means':{
	'how to code': 'Step 1: Start with some initial cluster centers (k random points) \n\
	Step 2: Iterate: \n\t\
	Assign/cluster each example to closest center\n\t\
	Recalculate and change centers as the mean of the points in the cluster.\n\
	Step 3: Stop when no pointsʼ assignments change',
	'properties': '– Guaranteed to converge in a finite number of iterations. \n\
	– Running time per iteration:\n\t\
	1. Assign data points to closest cluster center O(KN) time.\n\t\
	2. Change the cluster center to the average of its assigned points O(N).'
	},

	'logistic regression':{
	'description': 'Logistic regression is the appropriate regression analysis to conduct when the dependent variable is dichotomous (binary). \
	Like all regression analyses, the logistic regression is a predictive analysis. \
	Logistic regression is used to describe data and to explain the relationship between one dependent binary variable and one or more nominal, ordinal, interval or ratio-level independent variables.',
	'properties': 'Actually a technique for classification, not regression.\n\
	A multidimensional feature space (features can be categorical or continuous).\n\
	Outcome is discrete, not continuous.',
	'advantages': '– Makes no assumptions about distributions of classes in feature space.\n\
	– Easily extended to multiple classes (multinomial regression).\n\
	– Natural probabilistic view of class predictions.\n\
	– Quick to train.\n\
	– Very fast at classifying unknown records.\n\
	– Good accuracy for many simple data sets.\n\
	– Resistant to overfitting.\n\
	– Can interpret model coefficients as indicators of feature importance.',
	'disadvantages': 'Linear decision boundary'
	},

	'k-nearest neighbours':{
	'description': 'Essentially, given a query item: Find k closest matches in a labeled dataset. \
	Basic idea: If it walks like a duck, quacks like a duck, then it’s probably a duck.',
	'properties': '– Part of instance based learning (lazy learning).\n\
	– Non-parametric: makes no assumptions about the probability distribution the examples come from.\n\
	– Does not assume data is linearly separable.\n\
	– Derives decision rule directly from training data.\n\
	– No information discarded: exceptional and low frequency training instances are available for prediction.',
	'how to code': 'Requires three inputs:\n\t\
	1. The set of stored samples.\n\t\
	2. Distance metric to compute distance between samples.\n\t\
	3. The value of k, the number of nearest neighbors (NN) to retrieve.\n\n\
	To classify unknown record:\n\t\
	1. Compute distance to Unknown record other training records.\n\t\
	2. Identify k NN\n\t\
	3. Use class labels of NN to determine the class label of unknown record (e.g., by taking majority vote) Or to put simply, to classify a new input vector x, examine the k-closest training data points to x and assign the object to the most frequently occurring class.',
	'advantages': '– Training is very fast.\n\
	– Learn complex target functions.\n\
	– Do not lose information.',
	'disadvantages': '– Slow at query. Complexity: O(kdN).\n\
	– Required amount of training data increases exponentially with dimension.\n\
	– Must store all training data.\n\
	– Easily fooled by irrelevant attributes (add noise to distance measure).\n\
	– Sensitive to mis-labeled data and scales of attributes.'
	},

	'decision trees':{
	'description': 'Decision Trees are a type of Supervised Machine Learning (that is you explain what the input is and what the corresponding output is in the training data) where the data is continuously split according to a certain parameter. \
	The tree can be explained by two entities, namely decision nodes and leaves. The leaves are the decisions or the final outcomes. And the decision nodes are where the data is split.',
	'example': '1.Classification trees, 2.Regression trees.',
	'how to code': 'Base Case (do not split a node):\n\t\
	1. if all matching records have the same output value.\n\t\
	2. if none of the attributes can create multiple nonempty children (run out of questions!)\n\n\
	Recursive:\n\t\
	1. Select the “best” variable (based on Information Gain, Gini Index), and generate child nodes: One for each possible value.\n\t\
	2. Partition samples using the possible values, and assign these subsets of samples to the child nodes.\n\t\
	3. Repeat for each child node until all samples associated with a node that are either all positive or all negative.',
	'when to consider': '– Instances describable by attribute-value pairs.\n\
	– Target function is discrete valued.\n\
	– Disjunctive hypothesis may be required.\n\
	– Possibly noisy training data.\n\
	– Missing attribute values.',
	'properties': 'Problem: exponentially large trees (overfitting).\n\
	Simpler is better and avoids overfitting.\n\
	Otherways of avoiding overfitting are: Stop growing when split not statistically significant, grow full tree, then post-prune and cross validation.'
	}

}

#helper function to add created data to db file
def append_subject_content_to_db(db):
	if os.path.isfile('machine_learning.json') and os.access('machine_learning.json', os.R_OK):
		print("machine_learning.json exists and readable.")
		with open('machine_learning.json', 'r') as file:
			data = json.load(file)
			print("File loaded.")
		data.update(db)
		with open('machine_learning.json', 'w') as file:
			file.write(json.dumps(data, indent=4))
			print("Data writtten to file")
	else:
		print("Either json file is missing or not readable. Creating machine_learning.json")
		with open('machine_learning.json', 'w') as file:
			file.write(json.dumps(db, indent=4))
			print("Data writtten to file")
	return