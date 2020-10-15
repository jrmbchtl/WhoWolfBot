PY=python -m py_compile
.PHONY:
    all
    test
    install
    compile
    analyze
all:
    pymake analyze
    pymake test
    pymake install
test:
    python src/main/SystemTestRegistration.py
install:
    python src/main/Main.py
compile:
    $(PY) src/main/Main.py
analyze:
    pymake flake
    pymake pylama
flake:
    pymake flake_main
    pymake flake_systemtest
flake_main:
    flake8 --format=html --htmldir=flake-report src/main
flake_systemtest:
    flake8 --format=html --htmldir=flake-report src/systemtest
pylama:
    pymake pylama_main
    pymake pylama_systemtest
pylama_main:
    pylama -i W191,E501 src/main
pylama_systemtest:
    pylama -i W191,E501 src/systemtest
