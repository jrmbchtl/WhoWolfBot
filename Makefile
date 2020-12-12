PY=python -m py_compile
.PHONY:
    test
    server
    analyze
test:
    pymake analyze
    python3 src/main/server/main.py --systemtest
server:
    python3 src/main/server/main.py --telegram
analyze:
	python3 pylint_check.py
    pymake flake
    pymake pylama
    python3 check_localization.py
flake:
    pymake flake_main
    pymake flake_client
    pymake flake_systemtest
flake_main:
    flake8 --format=html --htmldir=flake-report src/main/server --ignore=E126,W503
flake_client:
    flake8 --format=html --htmldir=flake-report src/main/client --ignore=E126,W503
flake_systemtest:
    flake8 --format=html --htmldir=flake-report src/systemtest --ignore=E126,W503
pylama:
    pymake pylama_main
    pymake pylama_client
    pymake pylama_systemtest
pylama_main:
    pylama -i W191,E501,E128,W503 src/main/server
pylama_client:
    pylama -i W191,E501,E128,W503 src/main/client
pylama_systemtest:
    pylama -i W191,E501,E128,W503 src/systemtest
