from playwright.sync_api import sync_playwright
import json
import re
import random

def extract_author_abstract_keywords(web_content):
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


def crawle_single_conf_through_dblp(page, dblp_conf_url : str):
    print("LOG : handel %s" % dblp_conf_url)
    year = dblp_conf_url[-9:-5]

    papers = []
    
    page.goto(dblp_conf_url)
    
    doi_list = re.findall("<a href=\"https://doi\.org/[\.\/0-9A-Za-z]+\">", page.content()) # find all doi url
    doi_list = [x[len('<a href="'):-2] for x in doi_list] # remove useless
    
    print("LOG: all DOIs are loaded, total %d" % len(doi_list))

    counter = 0 # current DOI's id
    for doi in doi_list:
        if doi[-5:] == ("." + year): # this one is the IEEE's mainpage for DAC'21
            continue
        
        page.wait_for_timeout(random.randint(500, 1800))
        page.goto(doi)

        counter += 1
        print("LOG: handle %d-th DOI, title: %s" % (counter, page.title()))

        extracted = extract_author_abstract_keywords(page.content())
        if extracted == None:
            print("LOG: Failed to extract, doi : %s, title : \"%s\", url : %s" % (doi, page.title(), page.url))
            continue
        
        extracted["ieee_url"] = page.url
        extracted["title"] = [x.strip() for x in page.title().split("|")][0]
        papers.append(extracted)
    
    print("LOG : done with %s" % dblp_conf_url)
    
    return {"year" : year, "papers" : papers}


def crawle_ieee_confs_through_dblp(dblp_conf_urls):
    result = []

    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()
        
        for url in dblp_conf_urls:
            result.append(crawle_single_conf_through_dblp(page, url))
            page.wait_for_timeout(random.randint(10000, 15000))
        
        browser.close()

    return result


