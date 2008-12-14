
createdb -T template_postgis test
psql -U postgres -f mrdata.sql test

python run_test.py

nik2img.py -m mapfile.xml -o test.png --fonts fonts/gargi.ttf