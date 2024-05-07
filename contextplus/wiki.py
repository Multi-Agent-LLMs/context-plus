import concurrent.futures
import warnings
import wikipedia


def get_pages(search_prompt, n_results=5):
    """
    gets the wikipedia pages for the search prompt using the wikipedia api
    :param search_prompt: search prompt for the wikipedia search
    :param n_results: number of page titles that should be returned
    :return: page titles
    """
    return wikipedia.search(search_prompt, results=n_results)


def get_text_chunks(page_titles, chunk_length=512, verbose=False):
    """
    gets the content of the wikipedia pages using multiple threads (API calls take time) and splits it into chunks
    :param page_titles: list of page titles for which the content should be extracted
    :param chunk_length: length of characters that a chunk should have
    :param verbose: whether to print the progress
    :return: list of wiki text chunks
    """
    wiki_chunks = []
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_page = {executor.submit(get_page_content, page_title): page_title for page_title in page_titles}
            for future in concurrent.futures.as_completed(future_to_page):
                page_title = future_to_page[future]
                try:
                    wiki_content = future.result()
                    wiki_content = preprocess_and_chunk_wiki_content(wiki_content, chunk_length=chunk_length)
                    if verbose:
                        print(f"getting content of page {page_title}")
                    wiki_chunks.extend(wiki_content)
                except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
                    if verbose:
                        print(f"page {page_title} not found")
                    continue  # skip the page if it is not available
    return wiki_chunks


def get_page_content(page_title):
    """
    gets the content of the wikipedia page using the wikipedia api
    :param page_title: page_title of the wikipedia page from which the content should be extracted
    :return: content of the wikipedia page
    """
    return wikipedia.page(page_title, auto_suggest=False).content


def preprocess_and_chunk_wiki_content(wiki_content, chunk_length=512):
    """
    preprocesses the wiki content:
    - splits the content into paragraphs
    - removes headings and empty lines
    - splits too long paragraphs into smaller chunks without cutting sentences
    :param wiki_content: content of the wikipedia page
    :param chunk_length: length of characters that a chunk should have
    :return: list of wiki text chunks
    """
    # remove everything from the references section onwards
    wiki_content = wiki_content.split("== References ==")[0]
    # split into paragraphs
    chunks = wiki_content.split("\n")
    # remove headings, empty chunks and too short chunks
    chunks = [chunk for chunk in chunks if not ((chunk.startswith("=") and chunk.endswith("=")) or len(chunk) < 100)]
    # split too long chunks
    additional_chunks = []
    for i, chunk in enumerate(chunks):
        if len(chunk) > chunk_length:
            # split into sentences
            sentences = chunk.split(". ")
            # split into sub-chunks without cutting sentences
            sub_chunks = [""]
            sub_chunk_index = 0
            for sentence in sentences:
                if len(sentence) > chunk_length:
                    # cut the sentence if it's longer than the chunk_length (this should happen rarely)
                    sentence = sentence[:chunk_length]
                # if the sentence fits into the current sub-chunk
                if len(sub_chunks[sub_chunk_index]) + len(sentence) < chunk_length:
                    sub_chunks[sub_chunk_index] += sentence + ". "
                else:
                    sub_chunk_index += 1
                    sub_chunks.append(sentence + ". ")
            # replace original chunk with first sub-chunk
            chunks[i] = sub_chunks[0]
            # add the other sub-chunks to the list
            for j in range(1, len(sub_chunks)):
                additional_chunks.append(sub_chunks[j])
    chunks.extend(additional_chunks)
    return chunks
