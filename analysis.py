from typing import List
import re

def get_paper_keywords(paper):
    keywords = set()
    for keywords_set in paper["keywords"]:
        for x in keywords_set["kwd"]:
            keywords.add(x.lower())
    return keywords

def is_topic_related(paper : dict, topic_pattern : str) -> bool:
    re_pattern = re.compile(topic_pattern)
    found = lambda content : re_pattern.match(content) != None
    if found(paper["title"]) or found(paper["abstract"]):
        return True
    if any(map(found, get_paper_keywords(paper))):
        return True
    return False

def collect_topic_related(papers : List[dict], topic_pattern : str) -> List[dict]:
    return [x for x in papers if is_topic_related(x, topic_pattern)]

def remove_topic_related(papers : List[dict], topic_pattern : str) -> List[dict]:
    return [x for x in papers if not is_topic_related(x, topic_pattern)]

def is_hls_related(paper):
    topic_pattern = re.compile()
    found = lambda content : topic_pattern.match(content) != None

    if found(paper["title"]) or found(paper["abstract"]):
        return True

    if any(map(found, get_paper_keywords(paper))):
        return True
    return False

def collect_hls_related(papers : List[dict]) -> List[dict]:
    return collect_topic_related(papers, "(HLS)|((H|h)igh(-| )(L|l)evel(-| )(S|s)ynthesis)")

def remove_ml_related(papers : List[dict]) -> List[dict]:
    return remove_topic_related(papers, "([aA]rtificial [iI]ntelligence)|(([Mm]achine|[Dd]eep) [lL]earning)|([Nn]eural [nN]etwork)|[cC]onvolution|CNN|DNN")


def register_keyword(kw : str, result : dict):
    if kw not in result:
        result[kw] = {"counter" : 0, "papers" : []}

def sort_keywords_counter(grouped : dict):
    result = [(kw, v) for (kw, v) in grouped.items() if v["counter"] > 3]
    result.sort(key=lambda pr : pr[1]["counter"], reverse=True)
    return result

def group_by_keywords(papers : List[dict]):
    result = dict()
    for paper in papers:
        for kw in get_paper_keywords(paper):
            register_keyword(kw, result)
            result[kw]["counter"] += 1
            result[kw]["papers"].append(paper)
    return result


