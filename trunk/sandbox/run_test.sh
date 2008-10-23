rm test_filter*
nik2img.py -m bench.xml -o test_filter_works.png -s 400,300 -v
nik2img.py -m bench_filter_failure.xml -o test_filter_fails.png -s 400,300 -v