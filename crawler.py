from playwright.sync_api import sync_playwright
import json
import re
import random
from typing import List
import threading
import os

class CrawlerConfig(object):
    def __init__(self, page_dir, page_pause_lb, page_pause_ub) -> None:
        self.page_dir = page_dir
        self.page_pause_lb = page_pause_lb
        self.page_pause_ub = page_pause_ub


class Conference(object):
    def __init__(self, name : str, year : int, pattern : str, dblp_url : str) -> None:
        self.name = name
        self.year = year
        self.ieee_doi_pattern = pattern
        self.dblp_conf_url = dblp_url
    
    def get_name(self):
        return "%s%d" % (self.name, self.year)


def save_page(title, content, conf: Conference, cfg  : CrawlerConfig):
    name = "%s.%d.%s.html" % (conf.name, conf.year, title)
    path = os.path.join(cfg.page_dir, name)
    with open(path, "w") as f:
        f.write(content)


def crawle_single_conf_through_dblp(page, conf: Conference, cfg : CrawlerConfig) -> List[dict]:
    conf_name = conf.get_name()
    print("LOG : handel %s: %s" % (conf_name, conf.dblp_conf_url))

    papers = []
    
    page.goto(conf.dblp_conf_url) # goto conference's main page in DBLP
    
    content = page.content() # save webpage content

    ieee_links = set(re.findall("https://ieeexplore\.ieee\.org/document/[0-9]+", content))
    ieee_doi_links = set(re.findall(conf.ieee_doi_pattern, content))
    doi_links =  set(re.findall("https://doi\.org/[0-9a-zA-Z\/\.]+", content))
    
    links = None
    if len(doi_links) > 0:
        links = doi_links
    if len(ieee_doi_links) > 0:
        links = ieee_doi_links
    if len(ieee_links) > 0:
        links = ieee_links
    if links == None:
        print("LOG: conference %s have no valid url for paper, %s" % (conf_name, page.url))
        return None
    
    print("LOG: % s has %d papers" % (conf_name, len(links)))

    counter = 0 # current DOI's id
    for ieee_paper_link in links:
        page.wait_for_timeout(random.randint(cfg.page_pause_lb, cfg.page_pause_ub))
        page.goto(ieee_paper_link)

        counter += 1
        print("LOG: handle %d-th DOI in %s, title: %s" % (counter, conf_name, page.title()))

        paper_title = [x.strip() for x in page.title().split("|")][0]
        paper_page_content = page.content()
        
        save_page(paper_page_content, paper_page_content, conf, cfg)

        if len(re.findall("dl\.acm\.org", page.url)) > 0:
            kind = "ACM"
        else:# IEEE url
            kind = "IEEE"

        papers.append({"title" : paper_title, "content" : paper_page_content, "url" : page.url, "kind" : kind})

    print("LOG : done with %s: %s" % (conf_name, conf.dblp_conf_url))
    return papers


def extract_ieee_info(web_content : str) -> dict:
    m = re.search('xplGlobal\.document\.metadata\=.*\};', web_content)
    if m == None:
        return None
    
    metadata = json.loads(m.group(0)[len("xplGlobal.document.metadata="):-1])

    if any([x not in metadata for x in ["abstract", "keywords", "authors"]]):
        return None
    
    result = dict()
    result["abstract"] = metadata['abstract']

    keywords = set()
    for x in metadata['keywords']:
        keywords.union(x["kwd"])

    result["keywords"] = keywords
    return result


def extract_acm_info(web_content : str) -> dict:
    m = re.search("<div class=\"abstractSection abstractInFull\">.*</div></div></div><!-- /abstract content -->", web_content)
    if m == None:
        return None
    
    abstract = m.group(0)[len("<div class=\"abstractSection abstractInFull\">"):-len("</div></div></div><!-- /abstract content -->")]
    abstract.replace("<p>", "")
    abstract.replace("</p>", "")

    result = dict()
    result["abstract"] = abstract
    result["keywords"] = [] # TODO: support keywords for ACM
    return result


def extract_papers_info(papers : List[dict]) -> List[dict]:
    result = []
    for paper in papers:
        if paper["kind"] == "IEEE":
            extracted = extract_ieee_info(paper["content"])
        else:
            assert(paper["kind"] == "ACM")
            extracted = extract_acm_info(paper["content"])

        x = paper.copy()
        x.pop("content", None)

        result.append({**x, **extracted})
    return result


class CrawlerThread (threading.Thread):
    def __init__(self, conf : Conference, cfg : CrawlerConfig):
        threading.Thread.__init__(self)
        self.conf = conf
        self.cfg = cfg
        self.extracted_papers = None

 
    def run(self):
        with sync_playwright() as p:
            browser = p.firefox.launch()

            page = browser.new_page()
            raw_papers = crawle_single_conf_through_dblp(page, self.conf, self.cfg)
            page.close()
            
            if raw_papers != None:
                self.extracted_papers = extract_papers_info(raw_papers)


def crawl_confs_through_dblp_multithread(confs : List[Conference], cfg : CrawlerConfig)  -> List[dict]:
    threads = []
    for conf in confs:
        threads.append(CrawlerThread(conf, cfg))
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    result = []
    for t in threads:
        result.append({"conf_name" : t.conf.name, "year" : t.conf.year, "papers" : t.extracted_papers})
    return result


def crawl_confs_through_dblp_single_thread(confs : List[Conference], cfg : CrawlerConfig)  -> List[dict]:
    result = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for conf in confs:
            page = browser.new_page()
            raw_papers = crawle_single_conf_through_dblp(page, conf, cfg)
            page.close()
            if raw_papers != None:
                extracted_papers = extract_papers_info(raw_papers)
                result.append({"conf_name" : conf.name, "year" : conf.year, "papers" : extracted_papers})
    return result

def crawl_confs_through_dblp(confs : List[Conference], cfg : CrawlerConfig, is_multithread : bool, save_crawled : bool = False, save_dir : str = None) -> List[dict]:
    if is_multithread:
        result = crawl_confs_through_dblp_multithread(confs, cfg)
    else:
        result = crawl_confs_through_dblp_single_thread(confs, cfg)

    if save_crawled:
        with open(os.path.join(save_dir, "papers.json"), "w") as f:
            f.write(json.dumps(result, indent=2))
    return result