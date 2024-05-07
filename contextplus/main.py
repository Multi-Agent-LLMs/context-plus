import time

from contextplus import model, wiki


def context(query, min_summary_length=100, max_summary_length=200, n_wiki_pages=5, n_top_chunks=8, verbose=False):
    """
    provides context for the query by searching for relevant wikipedia pages, extracting the most relevant information
    and summarizing the facts
    :param query: query as a string for which the context should be provided
    :param min_summary_length: (optional) minimum length of the summary (in tokens)
    :param max_summary_length: (optional) maximum length of the summary (in tokens)
    :param n_wiki_pages: (optional, not recommended to change) number of wikipedia pages that should be searched
    :param n_top_chunks: (optional, not recommended to change) number of highest scoring chunks that should be summarized
    :param verbose: (optional) whether to print the progress
    :return: summarized facts from the wikipedia pages as a string, None if no wikipedia pages were found
    """

    time1, time2, time3, time4, time5, time6, time7, time8, time9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    if verbose:
        print("Query:", query)
        time1 = time.time()

    # create wikipedia search prompt
    wiki_search_prompt = model.create_wiki_search_prompt(query, verbose=verbose)
    if verbose:
        time2 = time.time()
        print("Time taken to get wiki search prompt:", time2 - time1, "seconds")

    # get relevant wikipedia pages
    page_titles = wiki.get_pages(wiki_search_prompt, n_results=n_wiki_pages)
    if verbose:
        print("Page titles:", page_titles)
        time3 = time.time()
        print("Time taken to get wiki pages:", time3 - time2, "seconds")

    # get the content of the wikipedia pages and split it into chunks
    wiki_chunks = wiki.get_text_chunks(page_titles, chunk_length=512, verbose=verbose)
    if verbose:
        time4 = time.time()
        print("Time taken to get wiki chunks:", time4 - time3, "seconds")
    if not wiki_chunks:
        return None

    # get the embeddings for the query and the wiki chunks
    query_embedding = model.get_embeddings([query])
    if verbose:
        time5 = time.time()
        print("Time taken to get query embedding:", time5 - time4, "seconds")
    wiki_embeddings = model.get_embeddings(wiki_chunks)
    if verbose:
        time6 = time.time()
        print("Time taken to get wiki embeddings:", time6 - time5, "seconds")

    # calculate the similarity between the query and the wiki chunks
    similarities = model.calculate_similarity(query_embedding, wiki_embeddings, top_k=n_top_chunks)
    if verbose:
        time7 = time.time()
        print("Time taken to calculate similarity:", time7 - time6, "seconds")

    top_chunks = ""
    for i, similarity in enumerate(similarities):
        top_chunks += "<" + str(i + 1) + "> " + wiki_chunks[similarity['corpus_id']] + " </" + str(i + 1) + ">\n\n"
        if verbose:
            print("Chunk" + str(i + 1) + ":", wiki_chunks[similarity['corpus_id']], "\t\t\tscore:", similarity['score'])
    if verbose:
        time8 = time.time()
        print("Time taken to get concatenated top chunk string:", time8 - time7, "seconds")

    # summarize facts from the top wiki chunks
    summarized_facts = model.summarize_facts(top_chunks, min_length=min_summary_length, max_length=max_summary_length)
    if verbose:
        time9 = time.time()
        print("Time taken to summarize facts:", time9 - time8, "seconds")
        print("Total time taken:", time9 - time1, "seconds")
    return summarized_facts


if __name__ == "__main__":
    user_query = "What are the names of Barack Obamas children?"
    context = context(user_query, verbose=True)
    print(context)
