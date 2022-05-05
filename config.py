urls = {
    "DAC" : {
        "pattern" : "https://doi\.org/10\.1109/DAC[\.\/0-9A-Za-z]+",
        "dblp_prefix" : "https://dblp.org/db/conf/dac/dac"
        },
    "ICCAD" : {
        "pattern" : "https://doi\.org/10\.1109/ICCAD[\.\/0-9A-Za-z]+", 
        "dblp_prefix" : "https://dblp.org/db/conf/iccad/iccad"
        }, 
    "DATE" : {
        "pattern" : "https://doi\.org/10\.23919/DATE[\.\/0-9A-Za-z]+", 
        "dblp_prefix" : "https://dblp.org/db/conf/date/date"
        }
}

year_start = 2018
year_end = 2021

url_pause = 600
url_pause_variation = 125


crawled_output_dir = "data/crawled"

analysis_output_dir = "data/analysis"