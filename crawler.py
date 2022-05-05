from playwright.sync_api import sync_playwright
import json
import re
import random
from typing import List

def extract_author_abstract_keywords(web_content : str) -> dict:
    m = re.search('xplGlobal\.document\.metadata\=.*\};', web_content)
    if m == None:
        return None
    
    metadata = json.loads(m.group(0)[len("xplGlobal.document.metadata="):-1])

    if any([x not in metadata for x in ["abstract", "keywords", "authors"]]):
        return None
    
    result = dict()
    result["abstract"] = metadata['abstract']
    keywords = []
    for keywords_list in [x["kwd"] for x in metadata['keywords'] if x["type"] in ["IEEE Keywords", "Author Keywords", "INSPEC: Controlled Indexing", "INSPEC: Controlled Indexing"]]:
        keywords.extend(keywords_list)
    result["keywords"] = keywords
    result["authors"] = metadata["authors"]
    return result


def crawle_single_conf_through_dblp(page, dblp_conf_url : str, ieee_doi_pattern : str) -> List[dict]:
    print("LOG : handel %s" % dblp_conf_url)

    papers = []
    
    page.goto(dblp_conf_url) # goto conference's main page in DBLP
    
    content = page.content() # save webpage content

    ieee_links = set(re.findall("https://ieeexplore\.ieee\.org/document/[0-9]+", content))
    doi_links = set(re.findall(ieee_doi_pattern, content))
    
    links = None
    if len(doi_links) > 0:
        links = doi_links
    if len(ieee_links) > 0:
        links = ieee_links
    if links == None:
        print("LOG: conference have no valid IEEE paper url, %s" % page.url)
        return None
    
    print("LOG: all DOIs are loaded, total %d" % len(links))

    counter = 0 # current DOI's id
    for ieee_paper_link in links:
        page.wait_for_timeout(random.randint(500, 1800))
        page.goto(ieee_paper_link)

        if len(re.findall("dl\.acm\.org", page.url)) > 0:
            print("LOG: ACM url %s, skip it" % page.url)
            continue
    
        counter += 1
        print("LOG: handle %d-th DOI, title: %s" % (counter, page.title()))

        extracted = extract_author_abstract_keywords(page.content())
        if extracted == None:
            print("LOG: Failed to extract, url : %s, title : \"%s\", url : %s" % (ieee_paper_link, page.title(), page.url))
            continue
        
        extracted["ieee_url"] = page.url
        extracted["title"] = [x.strip() for x in page.title().split("|")][0]
        papers.append(extracted)
    
    print("LOG : done with %s" % dblp_conf_url)
    
    return papers


class Conference(object):
    def __init__(self, name : str, year : int, pattern : str, dblp_url : str) -> None:
        self.name = name
        self.year = year
        self.pattern = pattern
        self.dblp_url = dblp_url
    

def crawle_ieee_confs_through_dblp(confs : List[Conference], dir : str)  -> List[List[dict]]:
    result = []

    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()
        
        for conf in confs:
            papers = crawle_single_conf_through_dblp(page, conf.dblp_url, conf.pattern)
            if papers == None:
                continue

            result.append({"papers" : papers, "name" : conf.name, "year" : conf.year})
            page.wait_for_timeout(random.randint(10000, 15000))

            with open("%s/%s.%d.json" % (dir, conf.name, conf.year)) as f:
                json.dump(papers, f)
        
        browser.close()
    return result


