mkdir wikidata
cd wikidata
python generate_text_files.py
wget -i text_file.txt
aws s3 sync . s3://wikibuckets/wikidata
