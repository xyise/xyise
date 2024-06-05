/*
This is a json parser that can parse json strings and store them in a map.
    * stores integers, doubles, strings, vectors of integers, doubles, strings and other MyJson objects.
    * parses json strings and store them in a MyJson object.
    * converts a MyJson object to a json string.

Notes:
    * C++ 17 is required. Only the standard library (std) is used. No external libraries are used.
    * No dynamic memory allocation is used. The standard library containers used in the implementation should have move semantics, so that the memory should not be copied when the objects are moved.
    * While exceptions are thrown when the json string is invalid, the parser may not be able to detect all invalid json strings.
*/

#ifndef MY_JSON_H
#define MY_JSON_H

#include <map>
#include <iostream>
#include <string>
#include <variant>
#include <vector>

namespace my_json
{
    class MyJson;
    typedef std::variant<int, double, std::string, std::vector<int>, std::vector<double>, std::vector<std::string>,MyJson> MyJsonValue;

    typedef std::string::const_iterator sci_t;

    class MyJson
    {
    private:
        std::map<std::string, MyJsonValue> json;

        static MyJson _parse(const std::string& txt, sci_t& it);

    public:
        MyJson();
        MyJson(std::map<std::string, MyJsonValue>);
        template <typename T>
        void add(std::string key, T value);
        template <typename T>
        T& get(const std::string& key);
        bool has_key(const std::string& key);
        bool is_empty_vector(const std::string& key);
        static MyJson parse(const std::string& txt);

    friend std::ostream &operator<<(std::ostream &os, const MyJson &my_json);
    };
}

#include "my_json.tcc"

#endif