#!/usr/bin/env python
# coding: utf-8

# # Chapter 8 - Document encoding, sentiment analysis, and text classification

# 2022 August 24

# <a target="_blank" href="https://colab.research.google.com/github/EastBayEv/SSDS-TAML/blob/main/fall2022/8_Docencoding_sentanalysis_textclassif.ipynb">
#   <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
# </a>

# In[1]:


import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
import spacy
import nltk
from nltk.corpus import movie_reviews
import numpy as np
from sklearn.utils import shuffle
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, classification_report, accuracy_score, confusion_matrix 

import warnings
warnings.filterwarnings("ignore", category = DeprecationWarning)


# ## Document encoding for machine learning
# 
# In the last chapter you saw that we do not change text to numbers, but instead changed the _representation_ of the text to the numbers in sparse matrix format. 
# 
# In this format, each row represents a document and each column represents a token from the shared text vocabulary called a **feature**. 
# 
# ### Key terms
# 
# * **Document term matrix:** contains the frequencies (or TF-IDF scores) of vocabulary terms in a collection of documents in sparse format. 
#     * Each row is a document in the corpus.
#     * Each column represents a term (uni-gram, bi-gram, etc.) called a feature.
# 
# * **Bag of words:** The simplest text analysis model that standardizes text in a document by removing punctuation, converting the words to lowercase, and counting the token frequencies.
#     * Numeric values indicate that a particular feature is found in a document that number of times.
#     * A 0 indicates that the feature is _not_ found in that document. 
# 
# ![dtm](img/dtm.png)
# 
# [modified from "The Effects of Feature Scaling: From Bag-of-Words to Tf-Idf"](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/ch04.html)

# * **TF-IDF:** Term frequency–inverse document frequency; a weighted numerical statistic that indicates the uniqueness of a word is in a given document or corpus.
# 
# For TF-IDF sparse matrices:
# * A value closer to 1 indicate that a feature is more relevant to a particular document.
# * A value closer to 0 indicates that that feature is less/not relevant to that document.
# 
# ![tf1](img/tf1.png)
# 
# [Wikipedia](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
# 
# ![tf2](img/tf2.png)
# 
# [towardsdatascience](https://towardsdatascience.com/tf-term-frequency-idf-inverse-document-frequency-from-scratch-in-python-6c2b61b78558)

# ## Corpus definition: United Nations Human Rights Council Documentation
# 
# ![unhrc](img/unhrc.jpg)
# 
# We will select eleven .txt files from the UN HRC as our corpus, stored within the subfolder "human_rights" folder inside the main "data" directory. 
# 
# These documents contain information about human rights recommendations made by member nations towards countries deemed to be in violation of the HRC. 
# 
# [Learn more about the UN HRC by clicking here.](https://www.ohchr.org/en/hrbodies/hrc/pages/home.aspx)

# ### Define the corpus directory
# 
# Set the directory's file path and print the files it contains.

# In[4]:


import os
corpus = os.listdir('data/human_rights/')

# View the contents of this directory
corpus


# ### Store these documents in a data frame

# In[6]:


# Store in an empty dictionary for conversion to data frame
empty_dictionary = {}

# Loop through the folder of documents to open and read each one
for document in corpus:
    with open('data/human_rights/' + document, 'r', encoding = 'utf-8') as to_open:
         empty_dictionary[document] = to_open.read()

# Populate the data frame with two columns: file name and document text
human_rights = (pd.DataFrame.from_dict(empty_dictionary, 
                                       orient = 'index')
                .reset_index().rename(index = str, 
                                      columns = {'index': 'file_name', 0: 'document_text'}))


# ### View the data frame

# In[7]:


human_rights


# ### View the text of the first document

# In[8]:


# first thousand characters
print(human_rights['document_text'][0][:1000])


# ## English text preprocessing
# 
# Create a new column named "clean_text" to store the text as it is preprocessed. 
# 
# ### What are some of the things we can do? 
# 
# How else could you improve this process? 
# 
# * Remove non-alphanumeric characters/punctuation
# * Remove digits
# * Remove [unicode characters](https://en.wikipedia.org/wiki/List_of_Unicode_characters)
# * Remove extra spaces
# * Convert to lowercase
# * Lemmatize (optional for now)
# 
# Take a look at the first document after each step to see if you can notice what changed. 
# 
# > Remember: the process will likely be different for many other natural languages, which frequently require special considerations. 

# ### Remove non-alphanumeric characters/punctuation

# In[11]:


human_rights['clean_text'] = human_rights['document_text'].str.replace(r'[^\w\s]', ' ', regex = True)


# In[12]:


print(human_rights['clean_text'][0][:1000])


# In[13]:


# view third column
human_rights


# ### Remove digits

# In[14]:


human_rights['clean_text'] = human_rights['clean_text'].str.replace(r'\d', ' ', regex = True)


# In[15]:


print(human_rights['clean_text'][0][:1000])


# ### Remove unicode characters such as Ð and ð

# In[16]:


# for more on text encodings: https://www.w3.org/International/questions/qa-what-is-encoding
human_rights['clean_text'] = human_rights['clean_text'].str.encode('ascii', 'ignore').str.decode('ascii')


# In[17]:


print(human_rights['clean_text'][0][:1000])


# ### Remove extra spaces

# In[18]:


import regex as re
human_rights['clean_text'] = human_rights['clean_text'].str.replace(r'\s+', ' ', regex = True)


# In[19]:


print(human_rights['clean_text'][0][:1000])


# ### Convert to lowercase

# In[20]:


human_rights['clean_text'] = human_rights['clean_text'].str.lower()


# In[21]:


print(human_rights['clean_text'][0][:1000])


# ### Lemmatize

# In[25]:


get_ipython().system('python -m spacy download en_core_web_sm')
# !python -m spacy download en_core_web_lg


# In[26]:


nlp = spacy.load('en_core_web_sm')
human_rights['clean_text'] = human_rights['clean_text'].apply(lambda row: ' '.join([w.lemma_ for w in nlp(row)]))


# In[27]:


print(human_rights['clean_text'][0])


# ### View the updated data frame

# In[28]:


human_rights


# ## Unsupervised learning with `TfidfVectorizer()`
# 
# Remember `CountVectorizer()` for creating Bag of Word models? We can extend this idea of counting words, to _counting unique words_ within a document relative to the rest of the corpus with `TfidfVectorizer()`. Each row will still be a document in the document term matrix and each column will still be a linguistic feature, but the cells will now be populated by the word uniqueness weights instead of frequencies. 

# In[29]:


from sklearn.feature_extraction.text import TfidfVectorizer

tf_vectorizer = TfidfVectorizer(ngram_range = (1, 3), 
                                stop_words = 'english', 
                                max_df = 0.50
                                )
tf_sparse = tf_vectorizer.fit_transform(human_rights['clean_text'])


# In[30]:


tf_sparse.shape


# In[31]:


print(tf_sparse)


# ### Convert the tfidf sparse matrix to data frame

# In[48]:


tfidf_df = pd.DataFrame(tf_sparse.todense(), columns = tf_vectorizer.get_feature_names())
tfidf_df


# ### View 20 highest weighted words

# In[49]:


tfidf_df.max().sort_values(ascending = False).head(n = 20)


# ### Add country name to `tfidf_df`

# In[50]:


# wrangle the country names from the human_rights data frame
countries = human_rights['file_name'].str.slice(stop = -8)
countries = list(countries)
countries


# In[51]:


tfidf_df['COUNTRY'] = countries


# In[52]:


tfidf_df


# ### Examine unique words by each document/country
# 
# Change the country names to view their highest rated terms.

# In[53]:


country = tfidf_df[tfidf_df['COUNTRY'] == 'jordan']
country.max(numeric_only = True).sort_values(ascending = False).head(20)


# ## Sentiment analysis
# 
# Sentiment analysis is the contextual mining of text data that elicits abstract information in source materials to determine if data are positive, negative, or neutral. 

# ![sa](img/sa.jpg)
# 
# [Repustate](https://www.repustate.com/blog/sentiment-analysis-challenges-with-solutions/)

# ### Download the nltk built movie reviews dataset

# In[54]:


import nltk
from nltk.corpus import movie_reviews
nltk.download("movie_reviews")


# ### Define x (reviews) and y (judgements) variables

# In[55]:


# Extract our x (reviews) and y (judgements) variables
reviews = [movie_reviews.raw(fileid) for fileid in movie_reviews.fileids()]
judgements = [movie_reviews.categories(fileid)[0] for fileid in movie_reviews.fileids()]


# In[56]:


# Save in a dataframe
movies = pd.DataFrame({"Reviews" : reviews, 
                      "Judgements" : judgements})
movies.head()


# In[57]:


movies.shape


# ### Shuffle the reviews

# In[58]:


import numpy as np
from sklearn.utils import shuffle
x, y = shuffle(np.array(movies.Reviews), np.array(movies.Judgements), random_state = 1)


# In[59]:


# change x[0] and y[0] to see different reviews
x[0], print("Human review was:", y[0])


# ### Pipelines - one example
# 
# scikit-learn offers hand ways to build machine learning pipelines: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html

# In[61]:


# standard training/test split (no cross validation)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.30, random_state = 0)

# get tfidf values
tfidf = TfidfVectorizer()
tfidf.fit(x)
x_train = tfidf.transform(x_train)
x_test = tfidf.transform(x_test)

# instantiate, train, and test an logistic regression model
logit_class = LogisticRegression(solver = 'liblinear',
                                 penalty = 'l2', 
                                 C = 1000, 
                                 random_state = 1)
model = logit_class.fit(x_train, y_train)


# In[62]:


# test set accuracy
model.score(x_test, y_test)


# ### $k$-fold cross-validated model

# In[63]:


# Cross-validated model!
text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 3))),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LogisticRegression(solver = 'liblinear',
                                               penalty = 'l2', 
                                               C = 1000, 
                                               random_state = 1))
                     ])

# for your own research, thesis, or publication
# you would select cv equal to 10 or 20
scores = cross_val_score(text_clf, x, y, cv = 3)

print(scores, np.mean(scores))


# ### Top 25 features for positive and negative reviews

# In[64]:


feature_names = tfidf.get_feature_names()
top25pos = np.argsort(model.coef_[0])[-25:]
print("Top features for positive reviews:")
print(list(feature_names[j] for j in top25pos))
print()
print("Top features for negative reviews:")
top25neg = np.argsort(model.coef_[0])[:25]
print(list(feature_names[j] for j in top25neg))


# In[65]:


new_bad_review = "This was the most awful worst super bad movie ever!"

features = tfidf.transform([new_bad_review])

model.predict(features)


# In[66]:


new_good_review = 'WHAT A WONDERFUL, FANTASTIC MOVIE!!!'

features = tfidf.transform([new_good_review])

model.predict(features)


# In[68]:


# try a more complex statement
my_review = 'I hated this movie, even though my friend loved it'
my_features = tfidf.transform([my_review])
model.predict(my_features)


# ## UN HRC text analysis - what next?
# 
# What next? Keep in mind that we have not even begun to consider named entities and parts of speech. What problems immediately jump out from the above examples, such as with the number and uniqueness of country names?
# 
# The next two chapters introduce powerful text preprocessing and analysis techniques. Read ahead to see how we can handle roadblocks such as these. 
# 
# [Chapter 9](https://eastbayev.github.io/SSDS-TAML/fall2022/9_spaCy_textaCy_intros.html) provides introductions to the spaCy and textaCy Python libraries. 
# 
# [Chapter 10](https://eastbayev.github.io/SSDS-TAML/fall2022/10_BERTopic.html) provides an application of the BERTopic model. 

# ## Exercise - text classification
# 
# "The 20 newsgroups dataset comprises around 18000 newsgroups posts on 20 topics split in two subsets: one for training (or development) and the other one for testing (or for performance evaluation). The split between the train and test set is based upon a messages posted before and after a specific date."
# 
# 1. [Read through this 20 newsgroups dataset example](https://scikit-learn.org/0.19/datasets/twenty_newsgroups.html) to get familiar with newspaper data. 
# 2. Do you best to understand and explain what is happening at each step of the workflow. 
