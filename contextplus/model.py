from sentence_transformers.util import semantic_search
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Loading models
device = "cpu"  # todo only for cpu testing, can be removed to automatically choose the device
gist_embedding = SentenceTransformer("avsolatorio/GIST-small-Embedding-v0", device=device)
bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
flan_t5 = pipeline("text2text-generation", model="google/flan-t5-base", device=device)


# ------------------------------------------------ Embedding Model ----------------------------------------------------


def get_embeddings(texts):
    """
    gets the embeddings for the texts using the sentence transformer embedding model
    :param texts: list of texts for which the embeddings should be calculated
    :return: embeddings
    """
    # todo: check out arguments of the encode method for example 'prompt' or 'precision'
    return gist_embedding.encode(texts)


def calculate_similarity(query_embedding, wiki_embeddings, top_k=10):
    """
    calculates the similarity between the query_embedding and the wiki_embeddings which can be used to filter the
    wiki content
    for the most relevant information
    :param query_embedding: embedding of the query
    :param wiki_embeddings: list of chunked embeddings of the wikipedia content
    :param top_k: number of most similar chunks that should be returned
    :return: list of dictionary's with similarity scores ['score'] between the query_embedding and each embedding chunk
             and the index of the chunk ['corpus_id']
    """
    return semantic_search(query_embedding, wiki_embeddings, top_k=top_k)[0]


# --------------------------------------------------- Flan T5 ---------------------------------------------------------

def create_wiki_search_prompt(query, verbose=False):
    """
    extracts the most relevant keywords from the query and returns it as a prompt for the wikipedia search
    :param query: query for which the keywords should be extracted
    :param verbose: whether to print the wiki search prompt
    :return: keywords for the wikipedia search
    """
    prompt = ("I will give you a query and you have to create a list of keywords separated by commas to search in the "
              "internet for additional information. "
              "Example Query 1: What is the capital of France? "
              "Keywords: capital, France"
              "Example Query 2: Person that won the Nobel Prize in Literature in 2020 "
              "Keywords: Nobel Prize, Literature, 2020"
              "Example Query 3: What variation of house music was produced by artists such as Madonna and Kylie Minogue? "
              "Keywords: house music, Madonna, Kylie Minogue"
              "Now it's your turn!"
              f"Query: {query} Keywords:")

    keywords = flan_t5(prompt, max_length=50, do_sample=False)[0]['generated_text']
    if verbose:
        print("wiki search prompt:", keywords)
    return keywords


# todo: try out to look at different titles and let the model decide which will be the most promising ones

# ------------------------------------------------ Bart Large CNN -----------------------------------------------------

def summarize_facts(top_chunks, min_length, max_length):
    """
    summarizes the facts from the wiki_content
    :param top_chunks: chunks of the wiki content with the highest similarity to the query
    :param min_length: minimum length of the summary (in tokens)
    :param max_length: maximum length of the summary (in tokens)
    :return: summarized facts from the wiki content as a string
    """
    summary = bart_summarizer(top_chunks, min_length=min_length, max_length=max_length, do_sample=False)
    summary = summary[0]['summary_text']
    if summary.startswith(" "):
        summary = summary[1:]
    return summary
