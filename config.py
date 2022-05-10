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
        },
    "HPCA" : {
        "pattern" : "https://doi\.org/10\.1109/HPCA[\.\/0-9A-Za-z]+", 
        "dblp_prefix" : "https://dblp.uni-trier.de/db/conf/hpca/hpca"
    },
    "FCCM" : {
        "pattern" : "https://doi\.org/10\.1109/FCCM[\.\/0-9A-Za-z]+",
        "dblp_prefix" : "https://dblp.org/db/conf/fccm/fccm"
    },
    "IPDPS" : {
        "pattern" : "https://doi\.org/10\.1109/IPDPS[\.\/0-9A-Za-z]+",
        "dblp_prefix" : "https://dblp.org/db/conf/ipps/ipdps"
    },
    "ISCA" : {
        "pattern" : "https://doi\.org/10\.1109/ISCA[\.\/0-9A-Za-z]+",
        "dblp_prefix" : "https://dblp.uni-trier.de/db/conf/isca/isca"
    },
    "CGO" : {
        "pattern" : "https://doi\.org/10\.1109/CGO[\.\/0-9A-Za-z]+",
        "dblp_prefix" : "https://dblp.uni-trier.de/db/conf/cgo/cgo"
    },
    "PACT" : {
        "pattern" : "https://doi\.org/[\.\/0-9A-Za-z]+",
        "dblp_prefix" : "https://dblp.uni-trier.de/db/conf/IEEEpact/pact"
    },
    "CODES+ISSS" : {
        "pattern" : "https://doi\.org/10\.1109/CODESISSS[\.\/0-9A-Za-z]+",
        "dblp_prefix" : "https://dblp.uni-trier.de/db/conf/codes/codes"
    },
    "MIRCO" : {
        "pattern" : "https://doi\.org/10\.1109/MICRO[\.\/0-9A-Za-z]+",
        "dblp_prefix" : "https://dblp.org/db/conf/micro/micro"
    }
}

is_multithread = True
save_crawled = True

year_start = 2020
year_end = 2022

url_pause_lb = 375
url_pause_ub = 625

crawled_page_output_dir = "data/crawled/pages"
crawled_papers_output_dir = "data/crawled"