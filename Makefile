PY=python -m py_compile
.PHONY:
    test
    server
    client
    compile
    analyze
test:
    pymake analyze
    python src/systemtest/SystemTestMain.py
server:
    python3 src/main/server/Main.py
client:
    python3 src/main/client/Main.py
compile:
    $(PY) src/main/Main.py
analyze:
    pymake flake
    pymake pylama
flake:
    pymake flake_main
    pymake flake_client
    pymake flake_systemtest
flake_main:
    flake8 --format=html --htmldir=flake-report src/main/server
flake_client:
    flake8 --format=html --htmldir=flake-report src/main/client
flake_systemtest:
    flake8 --format=html --htmldir=flake-report src/systemtest
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
