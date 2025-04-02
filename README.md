# Analysis and visualization of plenary speeches from the German Bundestag.

[//]: # (## Overview)

[//]: # (What is the distribution of topics discussed in the Bundestag sessions in the last 70 years?)

[//]: # (What are the most important topics discussed in the Bundestag in the last 70 years?)

[//]: # (How does the overall sentiment change over time?)

[//]: # (What is the sentiment by gender over time?)

[//]: # (What is the sentiment by political party over time?)



## Overview

This project aims to analyze and visualize various aspects of plenary speeches delivered
in the German Bundestag over the past 70 years. 
The analysis will focus on the distribution of topics discussed, 
the topic distribution by party, the sentiment of speeches in general as well as partitioned by gender and party.

### Methodology:

This project involves a multi-step approach to analyze the topics and sentiment of parliament speeches text using a combination of natural language processing (NLP) techniques.

**Data Pre-processing:**

The parliament speeches text data is initially preprocessed using the Natural Language Toolkit (NLTK), polars, regex, spaCy and string library to perform the following tasks:

1. **Clean Text:** Cleaning speech texts from certain patterns and newline characters.
2. **Whitespace Removal:** Removing whitespace characters like spaces, tabs and line breaks from the text.
3. **Stop word Removal:** Removing common words that do not add much value.
4. **Stemming:** Reducing words to their stem or root form.
5. **Punctuation Removal:** Removing punctuations from the text.

**Topic Modelling:**

We use the Latent Dirichlet allocation (LDA) approach to model the most prevalent topics in the dataset over time.
To achieve this, the pre-processed text data is converted into a Gensim corpus and dictionary.  
Using those, we build a model where each topic is a combination of keywords, and each keyword contributes a certain weightage to the topic. After looking at those keyword lists, we noticed that most keyword lists could be attributed to one of the following topics: Außenpolitik, Innenpolitik, Regierungspolitik, Gesetzesgebung, Bundeswehr, Klimapolitik, Immigrationspolitik, Wirtschaftspolitik and Oppositionspolitik.  
Using SpaCy word embeddings and a cosine similarity approach, the output of the LDA model will be classified into these topics. For each year, we were able to extract up to 5 prevalent topics.

**Sentiment Analysis:**

The pre-processed text data is fed into the NLTK analyzer (set to default), to compute the compound scores (aggregates the sentiment scores of individual words to get an overall sentiment score for the text) for each word in the text and normalizes them between -1(most extreme negative) and +1(most extreme positive). Using the Sentiment Model, computing sentiment metrics such as:

**Sentiment by Gender:** Analyzing the sentiment trends of male and female speakers over time.

**Sentiment by Party:** Analyzing the sentiment trends of different political parties over time.

**Sentiment before elections:** Analyzing the sentiment trends before election periods.

To answer the research questions, we performed a **Latent Dirichlet Allocation** as well as a **Sentiment Analysis**

### Key Research Questions

1. **What is the distribution of topics discussed in the Bundestag sessions in the last 70 years?**
   - This question seeks to uncover the main themes and topics that have been addressed 
   in the Bundestag over an extended period. 
   - Understanding the evolution of topics can provide insights into the changing priorities 
   and concerns of German legislators.

2. **What are the most important topics discussed in the Bundestag in the last 70 years?**
   - This question aims at revealing, more generally than in question 1, which topics are most important in our research  
   context

3. **How does the overall sentiment change over time?**
   - by looking at the sentiment of the speeches over time, one can get an overwiew of how the political tone might have
   changed in the last 70 years
   - possible patterns, notably around important historical events, or general patterns over time could possibly be
   uncovered

4. **What is the sentiment by gender over time?**
   - This analysis aims to explore whether there are any significant differences in the 
   tone, evaluated through a sentiment analysis, of speeches based on the gender of the speaker. 
   - Tracking this over time can reveal trends and shifts in the rhetorical styles 
   of male and female legislators.

5. **What is the sentiment by political party?**
   - By examining the sentiment of speeches by party, we can identify which parties 
   tend to adopt more positive/negative tones in their discourse. 
   - This could be indicative of their rhetorical strategies and political tactics.


    
### Conclusion

1. **What is the distribution of topics discussed in the Bundestag sessions in the last 70 years?**
   - for this question, the output of the LDA has been visualized in the form of wordclouds, 
   each representing the output of one year, starting 1949. 
   - over time, the words/topics that appear most frequently and prominently are 'Bundesregierung','Gesetzesentwurf'
   and 'Land'
   - in the years 1989 and 1990, the word 'DDR' appears, which aligns with the general historical context
   - in 2010, the topic 'Afghanistan' is present, aligning with the end of a German military operation in that country
   - in 2020, the topic 'AfD' seems quite relevant. Also, the word 'Pandemie' appears

2. **What are the most important topics discussed in the Bundestag in the last 70 years?**
   - this question seems more difficult to answer specifically
   - in general, it can be observed that the topic 'Regierungspolitik' is most relevant over the years,
   followed by other ones like 'Gesetzgebung' and 'Innenpolitik', whereas topics like 'Aussenpolitik seem 
   less relevant
   
3. **How does the overall sentiment change over time?**
   - we obeserve that the average sentiment generally remains withing values between 0 and -0.16, with one noteable 
   negative change between 1950 and 1960, where the sentiment drops to almost -0.2. However, it seems unclear without 
   additional analysis, what the cause for such a drastic change might be
   - from 1960 to about 2000, there is a general negative trend in sentiment. Starting from around 2000,
   the sentiment is getting more positive, with one noticeable negative trend around 2008. This might be due to the 
   global financial crisis around that time 

4. **What is the sentiment by gender over time?**
   - starting from around 1970, the sentiment of both male and female speakers follows the general pattern described in 
   answer #3
   - generally, the tone of female speakers has shown to be more positive than those of their male counterparts
   - starting from 1950 to about 1970, we observed an extreme negative amplitude of tone in the speeches of female 
   members of parliament

5. **What is the sentiment by political party?**
   - there are noticeable differences in sentiment with regards to the political party of the speakers
   - the lowest, i.e. most positive sentiment was ovserved from the SSW party, the most negative one being the GB/BHE
   party
   - the sentiment of parties which are currently represented in the Bundestag appear to be quite similar around -0.25
   with a slightly more negative tone by SPD and CDU/CSU
   - we did not ovbserve differences in sentiment according to political orientation (left-/right-wing parties)



## Usage
To run this workflow, only Snakemake needs to be installed; no additional software is required. 
For further information, visit [Development Setup](CONTRIBUTING.md#development-setup).

## Citation
The work must be cited as [Citation](CITATION.cff).

## License
This work is licensed unter a [![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)

## Contributation and Contact
To learn more about how you can contribute to this project and to get in touch with us, please visit our [Contributing Page](CONTRIBUTING.md).

## Code of Conduct
To review our software's code of conduct, please visit our [Code of Conduct Page](CONDUCT.md).
