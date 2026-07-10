# Luna Bot
Python 3.14 Discord Bot

To Run:
'''
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
'''

To exit .venv
'''
deactivate
'''

For docker-compose run
'''
docker-compose up
'''

to rebuild:
'''
docker-compose up -d --no-deps --build
'''

Test are done via pytest. And pyproject.toml
'''
python -m venv .venv
pip install -r requirements-test.txt
pytest
'''
