from crawler import *
import config

if __name__ == "__main__":
    for (conf_name, urls) in config.urls.items():
        result = crawle_ieee_confs_through_dblp(urls)
        with open("%s/%s.json" % (config.output_dir, conf_name), "w") as f:
            json.dump(result, f)