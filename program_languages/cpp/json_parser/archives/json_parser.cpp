#include <iostream>
#include <fstream>
#include <string>
#include "json_parser.h"

namespace JsonParser
{
    static void step_skip_whitespaces(int steps, text_it &it)
    {
        // step and skip whitespaces
        for (int i = 0; i < steps; i++)
            it++;
        while (std::isspace(*it))
            it++;
    }

    void ReadFile(const std::string &filepath, std::string &output)
    {
        std::cout << "hi from namespace" << std::endl;
        std::ifstream file(filepath);
        if (file.is_open())
        {
            std::string line;
            while (std::getline(file, line))
            {
                output += line;
            }
            file.close();
        }
        else
        {
            std::cout << "file not open" << std::endl;
        }
    }

    JsonValue ParsePrimitive(const std::string &text, text_it start, text_it end)
    {
        std::string val_str = text.substr(start - text.begin(), end - start);
        if (val_str.find('.') != std::string::npos)
        {
            // if '.' is found, it's a double
            return {.d = std::stod(val_str)};
        }
        else
        {
            // otherwise, it's an int
            return {.i = std::stoi(val_str)};
        }
    }

    std::pair<std::string, JsonValue> ParsePair(const std::string &text, text_it it)
    {
        auto text_end = text.end();
        step_skip_whitespaces(0, it);

        text_it curr_it;
        std::string key_str;

        return {"", {.i = 0}};

        // JsonValue val;
        // if (*it == '"')
        // {
        //     // find the key string
        //     it++; 
        //     curr_it = it;
        //     while (*it != '"')
        //     {
        //         key_str += *it;
        //         it++;
        //     }
        //     key_str = text.substr(curr_it - text.begin(), it - curr_it);

        //     step_skip_whitespaces(1, it);
        //     // the net character should be ':'
        //     if (*it != ':')
        //     {
        //         throw std::runtime_error("Bad jason. Expected ':'");
        //     }
        //     step_skip_whitespaces(1, it);

        //     if (*it == '{')
        //     {
        //         // if it's an object, parse it recursively
        //         val.json 
        //         it++;
        //         auto pair = ParsePair(text, it);
        //         val.json



        //         while (*it != '}')
        //         {
        //             auto
        //     }
            




        // }
        // else
        // {
        //     // if it's not a string, parse it as a primitive
        //     curr_it = it;
        //     while (!std::isspace(*curr_it) && *curr_it != ',' && *curr_it != '}')
        //     {
        //         key_str += *curr_it;
        //         curr_it++;
        //     }
        //     it = curr_it;
        // }

    }
}