mkdir wikidata
cd wikidata
python generate_text_files.py
wget -i enwiki-pages-mutlistream.txt
wget -i enwiki-meta-history.txt
aws s3 sync . s3://wikibuckets/wikidata
