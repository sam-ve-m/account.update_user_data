export PYTHONPATH=$PWD/func
#mutatest -s ./func -y 'if' 'nc' 'ix' 'su' 'bs' 'bc' 'bn' -x 60 -n 1000 -t 'python3 -m pytest --cov-config=.coveragerc'
mutatest -s ./func -y 'if' 'nc' 'ix' 'su' 'bs' 'bc' 'bn' -x 60 -n 1000 -t 'python3 -m pytest --cov-report term-missing --cov-config=.coveragerc --cov=func tests'
