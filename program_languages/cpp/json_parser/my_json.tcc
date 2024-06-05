#ifndef MY_JSON_TPP
#define MY_JSON_TPP

namespace my_json
{
    //
    // Helper Functions
    //

    // helper functions for parsing
    void skip_whitespaces(const std::string &txt, sci_t &it, int skip)
    {
        std::advance(it, std::min(skip, static_cast<int>(std::distance(it, txt.end()))));
        // alternatively, use the following
        // for (int i = 0; i < skip; i++)
        // {
        //     if (it == txt.end())
        //         break;
        //     it++;
        // }

        while (it != txt.end() && std::isspace(*it))
        {
            it++;
        }
    }

    // helper functions for parsing
    std::string parse_str_val(const std::string &txt, sci_t &it)
    {
        std::string str;

        sci_t str_start, str_end;

        if (*it != '"')
        {
            throw std::invalid_argument("The iterator for a string must point to a double quote");
        }

        while (it != str.end())
        {
            it++;
            if (*it != '"')
                str += *it;
            else
                break;
        }
        // if successful, it should be pointing to a double quote
        if (it == str.end())
        {
            throw std::invalid_argument("Invalid JSON. A string must end with a double quote.");
        }
        // move to the character after closing '"'
        skip_whitespaces(txt, it, 1);
        return str;
    }

    // helper functions for parsing
    void move_to_end_of_value(const std::string &txt, sci_t &it)
    {
        // must check } first to handle ']', '},'.
        while (it != txt.end() && *it != ']' && *it != '}' && *it != ',')
        {
            it++;
        }
    }

    // helper functions for << operator
    template <typename T>
    void print_value(std::ostream &os, const T &value)
    {
        if constexpr (std::is_same_v<T, int> || std::is_same_v<T, double>)
        {
            os << value;
        }
        else if constexpr (std::is_same_v<T, std::string>)
        {
            os << "\"" << value << "\"";
        }
        else if constexpr (std::is_same_v<T, MyJson>)
        {
            os << value;
        }
        else if constexpr (std::is_same_v<T, std::vector<typename T::value_type>>)
        {
            os << "[";
            for (auto it = value.begin(); it != value.end(); ++it)
            {
                print_value(os, *it);
                if (std::next(it) != value.end())
                {
                    os << ", ";
                }
            }
            os << "]";
        }
    }

    //
    // End: Helper Functions
    //

    MyJson::MyJson()
    {
        json = {};
    }
    MyJson::MyJson(std::map<std::string, MyJsonValue> input)
    {
        this->json = input;
    }

    template <typename T>
    void MyJson::add(std::string key, T value)
    {
        json[key] = value;
    }

    template <typename T>
    T &MyJson::get(const std::string &key)
    {
        return std::get<T>(json[key]);
    }

    bool MyJson::has_key(const std::string &key)
    {
        return json.find(key) != json.end();
    }

    bool MyJson::is_empty_vector(const std::string &key)
    {
        if (!has_key(key))
        {
            throw std::invalid_argument("The key does not exist.");
        }

        int code = std::visit([](auto &&arg)
                              {
            using T = std::decay_t<decltype(arg)>;
            if constexpr (std::is_same_v<T, std::vector<int>> || 
                        std::is_same_v<T, std::vector<double>> || 
                        std::is_same_v<T, std::vector<std::string>>)
            {
                if (arg.empty())
                {
                    return 0;
                }
                else
                {
                    return 1;
                }
            }
            else
            {
                return -1;
            } },
                              json[key]);

        if (code == -1)
        {
            throw std::invalid_argument("The value is not a vector.");
        }
        else
        {
            return code == 0;
        }
    }

    MyJson MyJson::_parse(const std::string &txt, sci_t &it)
    {
        std::map<std::string, MyJsonValue> json;

        skip_whitespaces(txt, it, 0);
        if (*it != '{') // outer opening {
        {
            throw std::invalid_argument("Invalid JSON: It must start with '{'");
        }
        skip_whitespaces(txt, it, 1);

        while (it != txt.end())
        {
            // find key
            std::string key = parse_str_val(txt, it);

            if (*it != ':')
            {
                throw std::invalid_argument("Invalid JSON. A key must be followed by ':'.");
            }
            skip_whitespaces(txt, it, 1);

            if (it == txt.end())
            {
                throw std::invalid_argument("Invalid JSON. A key must be followed by a value.");
            }

            // find value
            if (*it == '{') // inner opening {
            {
                json[key] = MyJson::_parse(txt, it);
                if (*it != '}') // inner closing }
                {
                    throw std::invalid_argument("Invalid JSON. A JSON object must end with a closing brace.");
                }
                skip_whitespaces(txt, it, 1);
            }
            else if (*it == '"')
            {
                json[key] = parse_str_val(txt, it);
                move_to_end_of_value(txt, it);
            }
            else if (*it == '[') // array opening
            {
                skip_whitespaces(txt, it, 1);
                bool is_str_array = false;
                if (*it == '"')
                {
                    is_str_array = true;
                }
                bool is_int_array = true;

                std::vector<std::string> str_array;

                while (*it != ']')
                {
                    if (*it == '"')
                    {
                        str_array.push_back(parse_str_val(txt, it));
                    }
                    else
                    {
                        sci_t pos_s = it;
                        move_to_end_of_value(txt, it);
                        std::string val_str = txt.substr(pos_s - txt.begin(), it - pos_s);
                        str_array.push_back(val_str);
                        if (val_str.find('.') != std::string::npos)
                        {
                            is_int_array = false;
                        }
                    }
                    skip_whitespaces(txt, it, 0);
                    if (*it == ',')
                    {
                        skip_whitespaces(txt, it, 1);
                    }
                }
                skip_whitespaces(txt, it, 1);

                // if all elements are strings
                if (is_str_array)
                {
                    json[key] = str_array;
                }
                else
                {
                    if (is_int_array)
                    {
                        std::vector<int> int_array;
                        for (auto &str : str_array)
                        {
                            int_array.push_back(std::stoi(str));
                        }
                        json[key] = int_array;
                    }
                    else
                    {
                        std::vector<double> double_array;
                        for (auto &str : str_array)
                        {
                            double_array.push_back(std::stod(str));
                        }

                        json[key] = double_array;
                    }
                }
            }
            else
            {
                // numbers
                sci_t pos_s = it;
                move_to_end_of_value(txt, it);
                std::string val_str = txt.substr(pos_s - txt.begin(), it - pos_s);

                if (val_str.find('.') != std::string::npos)
                {
                    json[key] = std::stod(val_str);
                }
                else
                {
                    json[key] = std::stoi(val_str);
                }
            }

            if (it == txt.end())
            {
                throw std::invalid_argument("Invalid JSON. A JSON object must end with a closing brace.");
            }

            if (*it == '}') // outer ending }
            {
                break;
            }
            else // i.e. ',' go to the next pair
            {
                skip_whitespaces(txt, it, 1);
            }
        }

        return json;
    }

    MyJson MyJson::parse(const std::string &txt)
    {
        sci_t it = txt.cbegin();
        return MyJson::_parse(txt, it);
    }

    //
    // Friend functions
    //

    std::ostream &operator<<(std::ostream &os, const MyJson &my_json)
    {
        os << "{";
        for (auto it = my_json.json.begin(); it != my_json.json.end(); ++it)
        {
            os << "\"" << it->first << "\": ";
            std::visit([&os](auto &&arg)
                       { print_value(os, arg); },
                       it->second);
            if (std::next(it) != my_json.json.end())
            {
                os << ", ";
            }
        }
        os << "}";
        return os;
    }

} // namespace my_json

#endif // MY_JSON_TPP