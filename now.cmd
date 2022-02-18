set FLASK_APP=sensors:create_app('money', 7775)
START "" flask run --port 7775
set FLASK_APP=sensors:create_app('smog', 7776)
START "" flask run --port 7776
set FLASK_APP=sensors:create_app('temperature', 7777)
START "" flask run --port 7777
set FLASK_APP=sensors:create_app('cpu', 7778)
START "" flask run --port 7778
set FLASK_APP=sensors:create_app('people', 7779)
START "" flask run --port 7779

