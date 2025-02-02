#!/usr/bin/env python
# coding: utf-8

# # Chapter 2 - Core machine learning concepts; building text vocabularies

# 2022 January 26

# ![ml](img/ml.png)
# 
# [towardsdatascience.com - figure above and quotes below](https://towardsdatascience.com/artificial-intelligence-vs-machine-learning-vs-deep-learning-2210ba8cc4ac) 

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
import scipy.sparse


# ## What is machine learning?
# 
# Machine learning is a toolbox for modeling, investigating, and understanding data. To understand machine learning, a handful of key terms need to be defined. 

# [scikit-learn](https://scikit-learn.org/stable/) provides the foundation for this introductory machine learning session. 
# 
# Be sure to bookmark the below resources. Try them out with data from the `data/` folder as well as your own data! 
# 
# * scikit-learn tutorials: https://scikit-learn.org/stable/tutorial/index.html
# * scikit-learn user guide: https://scikit-learn.org/stable/user_guide.html 

# ## Key terms
# 
# * **Artificial intelligence:** "A program that can sense, reason, act, and adapt."
# 
# * **Machine learning:** "Algorithims whose performance improve as they are exposed to more data over time."
# 
# * **Deep learning:** "Subset of machine learning in which multilayered neural networks learn from vast amounts of data."

# ### _x_ and _y_ variables
# 
# * **_x_** variables are the independent variables. You will also see these referred to in a variety of contexts as features, covariates, predictors, input, or explanatory variables. 
# 
# * The **_y_** variable is the dependent variable. This is also referred to as the response, outcome, and target variable. 

# ### Types of machine learning:
# 
# * **Supervised machine learning:** algorithms train models that (best) learn the relationships between the **_x_** and **_y_** variables on a labeled dataset (called the **training set**, where the ground truth **_y_** variable is known). The performance of the trained model is then evaluated after it predicts the outcome on new data that the model has never seen before (called the **test set**) where where ground truth **_y_** label is unknown. 
# 
# The equation looks like:  $y=f(x)+ϵ$
# * $f$ is the unknown function that relates **_x_** to **_y_** and is estimated
# * $ϵ$ is random error independent of x and averages to zero

# ### Data splitting: Training and test performance
# 
# Preparation for supervised methods requires a split of the dataset into training and test sets. 
# 
# * **Training set:** is comprised of the data that will be used by the model to learn the relationships between the **_x_** and **_y_** variables. This "usually" consists of a majority portion of the rows in the dataset, such as 70%. 
# 
# * **Test set:** consists of the holdout data that the trained model has not yet seen and where the trained model will try predict the unknown labels. This "usually" consists of the remaining 30% of rows. 
# 
# > NOTE: These values are somewhat arbitrary. It could be argued that the more training data that are available, the "better" your model might be. Conversely, more test data could lead to higher performance on the test data. 
# 
# > Furthermore, if you have millions of rows of data, a splits of 50:50 or 99:1 might also work fine depending on the context. 

# * **Performance** is generally assessed through cost or loss functions such as misclassification error, sensitivity/specificity, precision/recall, (root) mean squared error, R-squared, AIC, BIC, and other [confusion matrix derivations](https://en.wikipedia.org/wiki/Confusion_matrix). 
# 
# * **Cross-validation** is the best way to split your data, because it repeats the train/test data splitting process $k$ number of times and rotates the test set each time so that every observation is included in a test set at least once. Performance results are then averaged to compute predictive performance. 

# ![cv_wiki](img/cv_wiki.png)

# ### Model evaluation
# 
# ![bv](img/bv.png)
# 
# * **Underfit:** A model is underfit if it performs poorly on the training data because it could not discern the relationship(s) between the **_x_** and **_y_variables.
# 
# * **Overfit:** A model is overfit if it performs well on the training dataset but poorly on the test set. 
# 
# * **Bias/variance tradeoff:** 
# 
# * **Bias** refers to the systematic error due to incorrect assumptions about the machine learning process or the framing of the problem itself. High bias models generally underfit and/or contain large amounts of error. 
# * **Variance** refers to changes in the model predictive accuracy due to fluctuations in the training set or when using different training datasets, and how much the model can adjust to each. High variance could be due to model complexity, noise in the dataset, and overfitting. 
# * The **tradeoff** means that models with high bias will have low variance, and vice-versa. The goal is to find the optimal combination of these two factors for your problem. 

# ### Classification versus regression
# 
# * **Supervised classification:** models probability that **_y_** is 1 given the covariates **_x_** and is performed when **_y_** is categorical (either binary yes/no or multinomial): $Pr(y=1|x)$ 
# * Medical diagnosis
# * Image classification
# * Fraud detection
# * Sentiment analysis

# * **Supervised regression:** models the conditional mean probability $E(y|x)$ and is performed when **_y_** is continuous (i.e., integer or float).
# * Life expectancy
# * Population growth
# * Weather forecasting
# * Stock market prediction

# * **Supervised algorithms** include: 
# * Regressions: ordinary least squares, generalized linear model, lasso
# 
# * Tree-based methods: decision tree, random forest, boosted trees
# 
# * Kernel-based methods: various; transform non-linear to linear space

# View scikit-learn's interactive documentation for estimator (algorithm) selection: https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html
# 
# ![skest](img/skest.png)

# * **Unsupervised machine learning:** algorithms are used to sort unlabeled datasets, without attempting to predict anything. 
# 
# The equation could simply look like: 
# 
# $\sim\ x$
# 
# Algorithms include: 
# * Clustering: hierarchical agglomerative, k-means, centroid, density-based, DBSCAN, GLRM
# 
# * Dimension reduction: PCA, t-SNE, UMAP

# * **Reinforcement:** algorithims are used to make real-time decisions and skill acquisition in fields such as game-theory and robotics. 

# * **Other:** semi-supervised, etc.

# * **Bias in research**
# 
# ![bias_res](img/bias_res.png)

# * **Ethical considerations:** 
# 
# Begin to familiarize yourself with the many ethnical points to consider along with their real-world implications.
# 
# * [Howard et al, 2017. Addressing bias in machine learning algorithms: A pilot study on emotion recognition for intelligent systems](https://ieeexplore.ieee.org/abstract/document/8025197?casa_token=xyJcglvpeyUAAAAA:_tpPmFLycMFQuTd4UC52Y2C5yxXignXv7OE1rgv01YwzOs2o9j_bMvIQPwD8IW2NT5awRJcl4g)
# * [Noble, 2018. Algorithms of oppression: How search engines reinforce racism](https://nyupress.org/9781479837243/algorithms-of-oppression/)
# * [Yapo and Weiss, 2018. Ethical implications of bias in machine learning](https://aisel.aisnet.org/hicss-51/os/topics_in_os/6/)
# * [Mehrabi et al, 2021. A survey on bias and fairness in machine learning](https://dl.acm.org/doi/abs/10.1145/3457607?casa_token=HkkFHCUfRh0AAAAA%3Az5PprDD4p2VDEyZD7KeJzl67tlpTTA48RsIlqcqDYLROEfyJMTzHRjdYYN8SheqDRkvt_H1XXojANQ)

# ## OLS example - by "hand"
# 
# Ordinary least squares regression provides a great example of the machine learning process and some of the key terms defined above. 

# ### Generate toy data

# In[2]:


import pandas as pd
data = pd.DataFrame({"x": [1,2,3,4,5],
                     "y": [2,4,6,8,20]})
data


# ### Calculate means of x and y

# In[3]:


x_mean = round(sum(data.x) / len(data.x), 2)
y_mean = round(sum(data.y) / len(data.y), 2)
print("mean of x:", x_mean)
print("mean of y:", y_mean)


# ### Visualize the data (training data)
# 
# Plot the known relationships between x and y. 

# In[4]:


plt.scatter(data.x, data.y);


# ### Calculate error for each observation
# 
# Error (least squares method) is the difference between each observation and the mean. Below this will be represented visually by the distance between each point and the line of best fit. 

# In[5]:


x_error = data.x - x_mean
y_error = data.y - y_mean


# In[6]:


# x
print(data.x)
print(x_mean)
print(x_error)


# In[7]:


# y
print(data.y)
print(y_mean)
print(y_error)


# ### Compute beta coefficients

# In[8]:


## Estimate the B1 coefficient (slope)
B1 = sum((data.x - x_mean) * (data.y - y_mean)) / sum((data.x - x_mean) **2)
print("slope (B1) is: ", B1)

## Estimate B0 coefficient (intercept)
B0 = y_mean - (B1 * x_mean)
print("intercept (B0) is: ", B0)


# ### Plot best fit line

# In[9]:


import seaborn as sns
import numpy as np
sns.regplot(data = data, 
            x = "x", y = "y",
           ci = None)
plt.xticks(np.arange(min(data.x), max(data.x)+1, 1.0))
plt.yticks(np.arange(min(data.y), max(data.y)+1, 2.0));


# ### Generate the predictions (test set)

# In[10]:


y_hat = B0 + B1 * data.x
print("Ground truth y values:")
print(data.y)
print()
print("Predicted y values:")
print(y_hat)


# ### Visualize the error for each observation
# 
# ![ls_err](img/ls_err.png)

# ### Evaluate the performance using RMSE
# 
# Root mean squared error is a handy performance metric because it has the same units of whatever is plotted on the y-axis. 
# 
# In our toy example here, we are off an average of 2.82843 units on the y-axis of a given data point from the line of best fit. 

# In[11]:


# 1. Square each error
y_error_sq = y_error ** 2
print(y_error_sq)


# In[12]:


# 2. Sum these values
sum_error_sq = sum(y_error_sq)
print(sum_error_sq)


# In[13]:


# 3. Calculate RMSE - the square root of summed squared error divided by the length of y
import math
RMSE = math.sqrt(sum_error_sq) / len(data.y)
print(round(RMSE, 5))


# ### Compare our by "hand" results to the scikit-learn version! 

# In[14]:


# use scikit-learn to compute R-squared value
from sklearn.linear_model import LinearRegression

lin_mod = LinearRegression().fit(data[['x']], data[['y']])
print("R-squared: " + str(lin_mod.score(data[['x']], data[['y']])))


# In[15]:


# use scikit-learn to compute slope and intercept
print("scikit-learn slope: " + str(lin_mod.coef_))
print("scikit-learn intercept: " + str(lin_mod.intercept_))


# In[16]:


# compare to our by "hand" versions. Both are the same!
print(int(lin_mod.coef_) == B1)
print(int(lin_mod.intercept_) == B0)


# In[17]:


# use scikit-learn to compute RMSE
from sklearn.metrics import mean_squared_error

RMSE_scikit = round(mean_squared_error(data.y, y_hat, squared = False), 5)
print(RMSE_scikit)


# In[18]:


# Does our hand-computed RMSE equal that of scikit-learn at 5 digits?? Yes!
print(round(RMSE, 5) == round(RMSE_scikit, 5))


# ## Supervised machine learning - logistic regression
# 
# Fortunately, you do not have to do any of this by hand thanks to scikit-learn! 
# 
# Here is a short workflow to fit a logistic regression model. Logistic regression is similar to linear regression $y \sim\ x$ but regresses for the probability of a categorical outcome. 
# 
# Let's calculate training and test set accuracy to predict whether a penguin is MALE or FEMALE based on thier biological and spatial characteristics. 

# In[19]:


# load data
penguins = pd.read_csv("data/penguins.csv")


# In[20]:


penguins.head()


# ### Preprocess the data - remove rows with NaN (missing) values

# In[21]:


# count number of rows with missing data in penguins. Eleven...
penguins.isnull().any(axis=1).sum()


# In[22]:


# make a copy with listwise deleted rows
p_complete = penguins.dropna()


# In[23]:


# count number of rows with missing data in p_complete. Zero! 
p_complete.isnull().any(axis=1).sum()


# ### Preprocess the data - convert categorical variables to indicators
# 
# Check out this great tutorial on [one-hot encoding](https://stackabuse.com/one-hot-encoding-in-python-with-pandas-and-scikit-learn/) to learn more.

# In[24]:


# convert island categorical variable into numeric indicators
p_dummy_island = pd.get_dummies(p_complete.island, prefix = "island")
p_dummy_island.head()


# In[25]:


# convert species categorical variable into numeric indicators
p_dummy_species = pd.get_dummies(p_complete.species, prefix = "species")
p_dummy_species.head()


# ### Preprocess the data - remove the island and species variables from p_complete

# In[26]:


# view column names
print(p_complete.columns)

# drop the first and second columns
p_complete = p_complete.drop(p_complete.columns[[0, 1]], axis=1)
p_complete.head()


# ### Recombine the numeric indicators with the other variables

# In[27]:


clean_penguins = pd.concat([p_dummy_island, p_dummy_species, p_complete], axis=1) 
clean_penguins.head()


# ### Recode MALE as 1 and FEMALE as 0 

# In[28]:


clean_penguins['sex'] = clean_penguins['sex'].map({'MALE': 1, 'FEMALE': 0})


# In[29]:


clean_penguins.head()


# ### Define your logistic regression object

# In[30]:


from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(solver = 'liblinear')

# Use something like the code below for multi-class classification
# lr = LogisticRegression(multi_class='multinomial', solver='lbfgs')


# ### Split the `clean_penguins` dataset into training and test sets

# In[31]:


# Define x and y for both training and test sets
from sklearn.model_selection import train_test_split

x = clean_penguins[['island_Biscoe', 'island_Dream', 'island_Torgersen', 'species_Adelie',
       'species_Chinstrap', 'species_Gentoo', 'bill_length_mm',
       'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
y = np.array(clean_penguins['sex']) 

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 123)


# In[32]:


x_train.shape


# In[33]:


x_test.shape


# In[34]:


len(y_train)


# In[35]:


len(y_test)


# ### Fit the model to the training data (0.84 accuracy)

# In[36]:


lr.fit(x_train, y_train)


# In[37]:


# View the accuracy
lr.score(x_train, y_train)


# ### Generate predicted values on the test data

# In[38]:


# Generate predicted y values based on the x test set data
predictions = lr.predict(x_test)
predictions


# ### Calculate test set accuracy (0.81 accuracy)

# In[39]:


test_score = lr.score(x_test, y_test)
print(test_score)


# In[40]:


from sklearn import metrics

cm = metrics.confusion_matrix(y_test, predictions)
print(cm)


# In[41]:


# Fancy it up! Use plt.savefig() to export
plt.figure(figsize=(8,8))
sns.heatmap(cm, annot = True, fmt = ".0f", 
            cbar = False, linewidths = 2, 
            square = True, cmap = 'YlGnBu', annot_kws={"size": 20})
plt.ylabel('Ground truth y label')
plt.xlabel('Predicted y label')
all_sample_title = 'Accuracy Score: {0}'.format(test_score)
plt.title(all_sample_title, size = 15);


# ## Building text vocabularies
# 
# What about how text is predicted? If we have text as data, we also need to convert the _representation_ of text into a format that machine learning algorithms can understand. 

# ### Define a corpus 

# In[56]:


corpus = [
    "First document text goes in this list of strings.",
    "Second document text goes here as well.",
    "Third document text text.",
    "Document four!"
    ]
corpus


# ### Bag of words model with `CountVectorizer`
# 
# A bag of words model removes punctuation and casefolds the text to lowercase before counting the words. 

# In[57]:


from sklearn.feature_extraction.text import CountVectorizer

# create the bag of words
vectorizer = CountVectorizer()

# the .fit method will learn the vocabulary 
vectorizer.fit(corpus)

# Print the vocabulary
vectorizer.vocabulary_


# ### Document term matrix
# 
# A [document term matrix](https://en.wikipedia.org/wiki/Document-term_matrix) displays term frequencies in sparse format across a collection of docuemnts. The `.transform` method will help us here!
# 
# * The first number is the document number
# * The second number is the word from the vocabulary
# * The third number is the number of times that word occurs

# In[58]:


vector = vectorizer.transform(corpus)
print(vector) 


# ### Present the sparse matrix

# In[59]:


# each row is a document, each column is a word from the vocabulary! 
# 1 means that word is present in that particular document
print(vector.toarray())


# In[60]:


# get the column names (alphabetical sort)
vectorizer.get_feature_names()


# In[61]:


# What does this tell us? 
vectorizer.transform(['document']).toarray()


# ### N-grams
# 
# While we have focused on single words above, we can apply this approach to multi-word phrases in order to try to predict linguistic instances and potentially better understand context of a corpus of documents. 
# 
# Use the below token patterns: 
# * bigrams    `ngram_range = (1, 2)`
# * trigrams   `ngram_range = (1, 3)`
# * etc.

# In[62]:


bigram_vectorizer = CountVectorizer(ngram_range = (1,2),
                                    token_pattern = r'\b\w+\b', 
                                    min_df = 1)
bigram_vectorizer


# Since we specify bigrams, both unigrams _and_ bigrams are returned!

# In[63]:


from sklearn.feature_extraction import DictVectorizer
bigram_analyzer = bigram_vectorizer.build_analyzer()
bigram_analyzer('Welcome to Stanford Libraries!')


# ### Apply n-grams to our above corpus

# In[64]:


corpus


# In[65]:


# perform the transformation
x = bigram_vectorizer.fit_transform(corpus).toarray()
print(x)


# In[66]:


# get the feature (column) names
# remember the rows are our four documents!
bigram_vectorizer.get_feature_names()


# In[67]:


# search for vocabulary words across the documents
feature_index = bigram_vectorizer.vocabulary_.get('first document')
x[:, feature_index]


# ### Data frame vocabulary across documents
# 
# Our vocabulary consists of 29 unigrams and bigrams across the four documents.

# In[68]:


# redefine x as sparse matrix (not array)
x = bigram_vectorizer.fit_transform(corpus)
print(x)


# In[69]:


import scipy.sparse
corpus_df = pd.DataFrame(x.todense(), columns = bigram_vectorizer.get_feature_names())
corpus_df


# In[70]:


# The features (columns) are the vocabulary from the bigram version of our corpus variable above! 
corpus_df.columns


# ## Quiz - Classic horror novel vocabulary
# 
# 1. Create a single sparse data frame that contains the vocabulary for _Frankenstein_ and _Dracula_. You should only have two rows (one for each of these novels), but potentially thousands of columns to represent the vocabulary across the two texts. 
