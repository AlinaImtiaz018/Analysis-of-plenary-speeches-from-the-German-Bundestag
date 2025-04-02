rule all:
    input: "plots/topics_by_year.svg", directory("plots/wordclouds"), "plots/sentiment.svg",
            "plots/sentiment_by_gender.svg", "plots/sentiment_by_faction.svg"

rule download:
    output: "data/speeches.csv", "data/politicians.tab", "data/factions.tab"
    shell: "./src/download.sh -d data"

rule files_to_parquet:
    input: "data/speeches.csv", "data/politicians.tab", "data/factions.tab"
    output: "data/parquet/speeches.parquet", "data/parquet/politicians.parquet", "data/parquet/factions.parquet"
    shell: "python -m src.files_to_parquet {input} -o1 {output[0]} -o2 {output[1]} -o3 {output[2]}"

# Preprocessing

rule clean_text:
    input: "data/parquet/speeches.parquet"
    output: "data/parquet/speeches_cleaned.parquet"
    shell: "python -m src.clean_text {input} speechContent --output {output}"

rule remove_stopwords:
    input: "data/parquet/speeches_cleaned.parquet", "data/custom_stopwords.txt"
    output: "data/parquet/speeches_wo_sw.parquet"
    shell: "python -m src.remove_stopwords {input[1]} {input[0]} speechContent --output {output}"

rule remove_whitespaces:
    input: "data/parquet/speeches_wo_sw.parquet"
    output: "data/parquet/speeches_wo_sw_ws.parquet"
    shell: "python -m src.remove_whitespaces {input} speechContent --output {output}"

rule stemming:
    input: "data/parquet/speeches_wo_sw_ws.parquet"
    output: "data/parquet/speeches_stemmed.parquet"
    shell: "python -m src.stemming {input} speechContent --output {output}"

rule remove_punctuation:
    input: "data/parquet/speeches_stemmed.parquet"
    output: "data/parquet/speeches_stemmed_wo_punctuation.parquet"
    shell: "python -m src.remove_punctuation {input} speechContent --output {output}"

rule tokenize:
    input: "data/parquet/speeches_stemmed_wo_punctuation.parquet"
    output: "data/parquet/speeches_tokenized.parquet"
    shell: "python -m src.tokenize_column {input} removed_punctation -o {output} -f NOUN PROPN"

rule add_gender_column:
    input: "data/parquet/speeches_stemmed.parquet", "data/parquet/politicians.parquet"
    output: "data/parquet/speeches_stemmed_with_gender.parquet"
    shell: "python -m src.merge_tables {input} politicianId gender -o {output}"

# Analysis
rule lda:
    input: "data/parquet/speeches_stemmed_wo_punctuation.parquet", "data/parquet/factions.parquet"
    output: "data/topics_by_year.json"
    shell: "python -m src.LDA.lda_model -m LDA -minf 20 -fname {input[0]} -fname1 {input[1]} -output {output}"

rule analyse_sentiment:
    input: "data/parquet/speeches_stemmed_with_gender.parquet"
    output: "data/parquet/speeches_with_sentiment.parquet"
    shell: "python -m src.SA.sentiment_analysis {input} -a nltk -o {output}"

rule analyse_sentiment_before_election:
    input: "data/parquet/speeches_with_sentiment.parquet", "data/election_dates.csv"
    output: "data/sentiment_before_election.csv"
    shell: "python -m src.SA.sentiment_before_election {input} --output {output}"

rule analyse_sentiment_by_gender:
    input: "data/parquet/speeches_with_sentiment.parquet"
    output: "data/sentiment_by_gender.csv"
    shell: "python -m src.SA.sentiment_by_gender {input} --output {output}"

rule analyse_sentiment_by_party:
    input: "data/parquet/speeches_with_sentiment.parquet"
    output: "data/sentiment_by_party.csv"
    shell: "python -m src.SA.sentiment_by_party {input} --output {output}"

# Plotting

rule plot_sentiment:
    input: "data/parquet/speeches_with_sentiment.parquet"
    output: "plots/sentiment.svg", "plots/sentiment_by_gender.svg"
    shell: "python -m src.plot_sentiment {input} {output}"

rule plot_sentiment_by_gender:
    input: "data/sentiment_by_gender.csv"
    output: "plots/overall_sentiment_by_gender.svg"
    shell: "python -m src.plot_sentiment_by_gender {input} {output}"


rule plot_topics_year:
    input: "data/topics_by_year.json"
    output: "plots/topics_by_year.svg"
    shell: "python -m src.plot_topics_year {input} {output} --plot-type scatter"

rule plot_word_cloud:
    input: "data/topics_by_year.json"
    output: directory("plots/wordclouds")
    shell: "python -m src.plot_wordcloud_per_year {input} {output} --output-format svg"

rule plot_sentiment_by_faction:
    input: "data/sentiment_by_party.csv", "data/parquet/factions.parquet"
    output: "plots/sentiment_by_faction.svg"
    shell: "python -m src.plot_sentiment_by_party {input[0]} {input[1]} {output}"
