from crawler import *
import config

if __name__ == "__main__":
    for (conf_name, info) in config.urls.items():
        dblp_prefix = info["dblp_prefix"]
        ieee_doi_url_pattern = info["pattern"]
        
        confs = []
        for year in range(config.year_start, config.year_end + 1):
            confs.append(Conference(conf_name, year, ieee_doi_url_pattern, "%s%d.html" % (dblp_prefix, year)))

        result = crawl_confs_through_dblp(confs, CrawlerConfig(config.crawled_page_output_dir, config.url_pause_lb, config.url_pause_ub), config.is_multithread, config.save_crawled, config.crawled_papers_output_dir)