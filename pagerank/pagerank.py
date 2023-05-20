import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}

    potential_pages = corpus[page]

    if len(potential_pages) == 0:
        probability = 1 / len(corpus)
        for corpus_page in corpus:
            probability_distribution[corpus_page] = probability

        return probability_distribution

    damping_prob = damping_factor / len(potential_pages)

    damping_probability_random = (1 - damping_factor) / len(corpus)

    for potential_page in potential_pages:
        probability_distribution[potential_page] = damping_prob

    for page in corpus:
        if page in potential_pages:
            probability_distribution[page] += damping_probability_random
        else:
            probability_distribution[page] = damping_probability_random

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}

    next_page = random.choice(list(corpus))

    for i in range(n - 1):
        model = transition_model(corpus, next_page, damping_factor)

        next_page = random.choices(
            list(model), weights=model.values(), k=1).pop()

        if next_page in pagerank:
            pagerank[next_page] += 1
        else:
            pagerank[next_page] = 1

    for page in pagerank:
        pagerank[page] = pagerank[page] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}

    for page in corpus:
        pagerank[page] = 1 / len(corpus)

    changed = False
    while not changed:

        pagerank_copy = {k: v for k, v in pagerank.items()}
        pagerank_difference = {}
        for page in corpus.keys():
            probability = 0

            for page_i, pages in corpus.items():
                if page in pages:
                    probability += pagerank_copy[page_i] / len(pages)
                elif len(pages) == 0:
                    probability += 1 / len(corpus)

            pagerank[page] = (1 - damping_factor) / \
                len(corpus) + (damping_factor * probability)

            pagerank_difference[page] = abs(
                pagerank_copy[page] - pagerank[page])

        changed = True
        for page in pagerank_difference:
            if pagerank_difference[page] > 0.001:
                changed = False

    summary_pagerank = 0
    for k in pagerank:
        summary_pagerank += pagerank[k]

    for k in pagerank:
        pagerank[k] = pagerank[k] / summary_pagerank

    return pagerank


if __name__ == "__main__":
    main()
