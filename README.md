# RentApp
App that allows users (preferable students) to rent flats and owners to create offers. 

To run:
- create venv and install requirements\
\
python3 -m venv venv\
.venv/bin/activate\
pip install -r /path/to/requirements.txt

- init db\
flask db init
flask db migrate
flask db upgrade

- run app\
python -m flask run
