import os
import random
import re
import sys
import numpy as np
import copy

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
            # Regex pattern to find web links in HTML
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

    prob_d = {}
    d = damping_factor
    links = corpus[page]
    num_links = len(links)

    # If links between pages exist
    if links:
        # Assigns prob (1 - damping_factor) / pages in the corpus to each key of the corpus
        for key in corpus:
            prob_d[key] = (1 - d) / len(corpus)

        # Random surfer should randomly choose one of the links from page with equal probability
        for key in links:
            prob_d[key] += d / len(corpus)

    # O/W
    else:
        # Choose randomly within corpus since there are no outgoing links
        for key in corpus:
            prob_d[key] = 1.0 / len(corpus)

    return prob_d


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # NEW: create a new dict all values = 0
    prob_d = {}.fromkeys(corpus.keys(), 0)

    # Start with a random page
    page = random.choices(list(corpus.keys()))[0]

    for i in range(1, n - 1):
        prob_d[page] += 1
        current_dist = transition_model(corpus, page, damping_factor)
        page = random.choices(list(current_dist.keys()),
                              current_dist.values())[0]

    # Divide all page counts by n to get proportion of samples for that page
    prob_d = {page: num_samples / n for page, num_samples in prob_d.items()}

    return prob_d


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    for each page, determine which/how many other pages link to it
    then, apply the PageRank formula
    if change (new_rank, old_rank) < threshold update counter
    if by the end of the loop, counter == N,
    it means that the change in rank for each page in the corpus was within the threshold
    so end the loop
    return rank
    """

    d = damping_factor
    total_pages = len(corpus)
    prob_d = {}.fromkeys(corpus.keys(), 1.0 / total_pages)

    change = True

    while change:
        change = False
        old_d = copy.deepcopy(prob_d)
        for page in corpus:
            prob_d[page] = ((1 - d) / total_pages) + \
                (d * get_sum(corpus, prob_d, page))

            # return each page’s PageRank accurate to within 0.001.
            change = abs(old_d[page] - prob_d[page]) > 0.001

    return prob_d


def get_sum(corpus, distribution, page):
    """
    New helper function

    """
    result = 0
    for p in corpus:
        if page in corpus[p]:
            result += distribution[p] / len(corpus[p])
    return result


if __name__ == "__main__":
    main()
