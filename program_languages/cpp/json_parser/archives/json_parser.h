#ifndef JSON_PARSER_H
#define JSON_PARSER_H

#include <map>
#include <memory>
#include <string>

namespace JsonParser {

    using text_it = std::string::const_iterator;
    union JsonValue {
        int i;
        double d;
        std::map<std::string, JsonValue>* json;
        std::unique_ptr<std::map<std::string, JsonValue>> json_ptr; // = nullptr;
    };

    void ReadFile(const std::string& filepath, std::string& output);

    JsonValue ParsePrimitive(const std::string& text, text_it start, text_it end);

    std::pair<std::string, JsonValue> ParsePair(const std::string& text, text_it it);

}


#endif