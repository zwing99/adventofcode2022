g++ -O3  -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) help.cpp -L/Users/zacoler/.pyenv/versions/3.10.8/lib/ -lpython3.10 -L/usr/local/lib -lintl -o help$(python3-config --extension-suffix)

