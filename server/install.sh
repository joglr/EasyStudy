python3 -m venv .venv
curl -fsSL https://bootstrap.pypa.io/get-pip.py > get-pip.py
./.venv/bin/python get-pip.py
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r ./local_requirements_py3_10.txt
./.venv/bin/python -m flask --debug run

