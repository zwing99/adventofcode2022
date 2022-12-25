#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdlib.h>
#include <tuple>
#include <optional>
#include <set>

#define getx std::get<0>
#define gety std::get<1>

namespace py = pybind11;

typedef std::tuple<int, int> Pair;
struct Extents {int min_x; int max_x; int min_y; int max_y;};
typedef std::map<Pair, std::vector<Pair> > WindPositions;
typedef std::unordered_map<int, WindPositions > WindPositionsLookup;

std::optional<Pair> get_direction(char c) {
    //std::cout << c << std::endl;
    if (c == '<') return Pair(-1, 0);
    if (c == '>') return Pair(1, 0);
    if (c == '^') return Pair(0, -1);
    if (c == 'v') return Pair(0, 1);
    return std::nullopt;
}

int add(int i, int j) {
    std::cout<<"foo"<<std::endl;
    return i + j;
}



void parse_grid(const std::vector<std::string>& lines, Pair& start, Pair &end, Extents& extents, WindPositions& initial_wind) {
    extents.min_x = 1;
    extents.max_x = lines[0].size() - 2;
    extents.min_y = 1;
    extents.max_y = lines.size() - 2;
    for (int y = 0; y < lines.size(); y++) {
        for (int x = 0; x < lines[y].size(); x++) {
            if (y == 0) {
                if (lines[y][x] == '.') start = Pair(x, y);
            }
            else if ( y == lines.size() - 1) {
                if (lines[y][x] == '.') end = Pair(x, y);
            }
            else {
                auto d = get_direction(lines[y][x]);
                if (d.has_value()) {
                    //if (initial_wind.count(d.value()) == 0) {
                    //    std::vector<Pair> m;
                    //    initial_wind[Pair(x, y)] = m;
                    //}
                    initial_wind[Pair(x, y)].push_back(d.value());
                }
            }
        }
    }
}

void load_winds(WindPositionsLookup& winds, Extents& extents, int minute) {
    if (winds.count(minute) > 0)
        return;
    for(int i = 1; i <= minute; i++) {
        if(winds.count(i) == 0) {
            auto prior = i-1;
            auto current = i;
            for (auto& item : winds[prior]) {
                auto& p = item.first;
                for (auto& d : item.second) {
                    Pair new_p(getx(p) + getx(d), gety(p) + gety(d));
                    if (getx(new_p) > extents.max_x) {
                        getx(new_p) = extents.min_x;
                    }
                    else if (getx(new_p) < extents.min_x) {
                        getx(new_p) = extents.max_x;
                    }
                    else if (gety(new_p) > extents.max_y) {
                        gety(new_p) = extents.min_y;
                    }
                    else if (gety(new_p) < extents.min_y) {
                        gety(new_p) = extents.max_y;
                    }
                    winds[current][new_p].push_back(d);
                }
            }
        }
    }
}


void dfs(
    int m,
    Pair pos,
    WindPositionsLookup& winds,
    const int& max_winds,
    Extents& extents,
    Pair& start,
    Pair& end,
    int& shortest,
    std::map<std::tuple<Pair, int> , int>& seen,
    const std::vector<Pair>& choices)
{
    auto& winds_m = winds[m];
    auto key = std::make_tuple(pos, m % max_winds);
    if (seen.count(key) > 0) {
        if (m >= seen[key]) return;
    }
    seen[key] = m;
    auto shortest_to_end = (gety(end) - gety(pos)) + (getx(end) - getx(pos));
    if ((m + shortest_to_end) >= shortest) return;
    if (pos == end) {
        //std::cout<<"found: "<<m<<std::endl;
        shortest = m;
        return;
    }
    load_winds(winds, extents, m+1);
    //if (m > 1000) return;
    for (auto c : choices) {
        auto c_pos = Pair(getx(pos) + getx(c), gety(pos) + gety(c));
        if (winds[m+1].count(c_pos) == 0) {
            if (c_pos == start || c_pos == end) {
                //std::cout<<"launch: "<<m<<" ("<<getx(c_pos)<<","<<gety(c_pos)<<")"<<std::endl;
                dfs(m + 1, c_pos, winds, max_winds, extents, start, end, shortest, seen, choices);
            }
            else if (
                getx(c_pos) >= extents.min_x
                && getx(c_pos) <= extents.max_x
                && gety(c_pos) >= extents.min_y
                && gety(c_pos) <= extents.max_y
            ) {
                //std::cout<<"launch: "<<m<<" ("<<getx(c_pos)<<","<<gety(c_pos)<<")"<<std::endl;
                dfs(m + 1, c_pos, winds, max_winds, extents, start, end, shortest, seen, choices);
            }
        }
    }
}


void go(const std::vector<std::string>& lines) {
    Pair start, end; 
    Extents extents;
    WindPositionsLookup winds;
    parse_grid(lines, start, end, extents, winds[0]);
    auto max_wind = extents.max_y - extents.min_y + 1;
    max_wind += extents.max_x - extents.min_x + 1;
    // std::cout << std::get<0>(start) << std::endl;
    // std::cout << std::get<0>(end) << std::endl;
    int shortest = 99999999;
    std::map<std::tuple<Pair, int> , int> seen;
    //std::vector<Pair> choices = { Pair(1, 0), Pair(0, 1), Pair(0, 0), Pair(-1, 0), Pair(0, -1)};
    std::vector<Pair> choices = { Pair(1, 0), Pair(0, 1), Pair(0, 0), Pair(-1, 0), Pair(0, -1)};
    std::vector<Pair> choices2 = { Pair(-1, 0), Pair(0, -1), Pair(0, 0), Pair(1, 0), Pair(0, 1)};
    dfs(0, start, winds, max_wind, extents, start, end, shortest, seen, choices);
    std::cout << shortest << std::endl;
    int m = shortest;
    shortest = 99999999;
    seen.clear();
    dfs(m, end, winds, max_wind, extents, end, start, shortest, seen, choices2);
    std::cout << shortest << std::endl;
    m = shortest;
    shortest = 99999999;
    seen.clear();
    dfs(m, start, winds, max_wind, extents, start, end, shortest, seen, choices);
    std::cout << shortest << std::endl;
    //Pair p1(1,0);
    //Pair p2(1,1);
    //std::cout<<(p1==p2)<<std::endl;
}


PYBIND11_MODULE(help, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function that adds two numbers");
    m.def("go", &go, "main");
}