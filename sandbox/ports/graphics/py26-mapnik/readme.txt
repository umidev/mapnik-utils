# pull macports sync post http://trac.macports.org/changeset/50085

# then...

sudo port install python26 python_select
sudo python_select python26
sudo port install jam 
sudo port install boost +icu +python26
sudo port install py26-mapnik
export PYTHONPATH=/opt/local/lib/python2.6/site-packages/:$PYTHONPATH
python
>>> import mapnik
>>> m = mapnik.Map(45,45)