#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdlib.h>
#include <tuple>

namespace py = pybind11;

int add(int i, int j) {
    std::cout<<"foo"<<std::endl;
    return i + j;
}


int mdistance(long long ax, long long ay, long long bx, long long by) {
    return std::abs(bx - ax) + std::abs(by - ay);
}

const int MAX_BOUNDS = 4000000;

struct Sensor {
    long long x;
    long long y;
    long long d;
};

long long part2(std::vector<std::tuple<std::tuple<int, int>, int> >  sensors) {
    std::vector<Sensor> v_sensors;
    for (auto s : sensors) {
        auto coor = std::get<0>(s);
        auto d = std::get<1>(s);
        Sensor sensor;
        sensor.x = std::get<0>(coor);
        sensor.y = std::get<1>(coor);
        sensor.d = d;
        v_sensors.push_back(sensor);
    }
    long long x;
    long long y;
    for (y=0; y<=MAX_BOUNDS; y++) {
        std::cout<<y<<std::endl;
        for (x=0; x<=MAX_BOUNDS; x++) {
            bool found = false;
            for (auto s : v_sensors) {
                auto target_distance = mdistance(s.x,s.y,x,y);
                if (target_distance <= s.d) {
                    found = true;
                    auto x_shift = s.d - target_distance;
                    x += x_shift;
                    break;
                }
            }
            if (!found) {
                std::cout << x << " " << y << std::endl;
                return (MAX_BOUNDS * x) + y;
            }
        }
    }
    return 0;
}


PYBIND11_MODULE(help, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function that adds two numbers");
    m.def("part2", &part2, "pt2");
}