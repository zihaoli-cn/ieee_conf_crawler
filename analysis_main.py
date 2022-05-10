import json
from operator import length_hint
import config
import os
import analysis

if __name__ == "__main__":
    hls_related = []
    for fname in os.listdir(config.crawled_output_dir):
        file_path = os.path.join(config.crawled_output_dir, fname)
        if not(os.path.isfile(file_path) and fname[-5:] == ".json"):
            continue

        with open(file_path, "r") as f:
            papers = json.load(f)
            old_length = len(papers)
            hls = analysis.collect_hls_related(papers)
            print("LOG: %s has %d HLS papers" % (fname, len(hls)))
            papers = analysis.remove_ml_related(papers)
            new_length = len(papers)

            print("LOG: %s used to have %d papers. Now it have %d papers after remove ML-related" % (fname, old_length, new_length))

            hls = analysis.collect_hls_related(papers)
            print("LOG: %s has %d HLS papers" % (fname, len(hls)))

            hls_related.extend(hls)

            target_path = file_path = os.path.join(config.filter_output_dir, fname)
            with open(target_path, "w") as dst:
                json.dump(papers, dst)

            group = analysis.group_by_keywords(papers)
            group = analysis.sort_keywords_counter(group)
            target_path = file_path = os.path.join(config.kw_indexed_output_dir, fname)
            with open(target_path, "w") as dst:
                json.dump(group, dst)

    print(hls_related)
    print("LOG: HLS-related = %d" % len(hls_related))
