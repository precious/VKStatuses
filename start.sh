cd robot
ln -s ../libstatuses.py
cd ../
python manage.py syncdb
