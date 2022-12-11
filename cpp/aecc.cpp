/*
 * MIT License
 * Copyright (c) 2021 Lin Cheng Chieh <https://github.com/blueskyson>
 */

#include "argparse.hpp"
#include <unordered_map>
#include <iomanip>

using std::string;
using std::cout;
using std::cin;
using std::endl;
using std::unordered_map;

unordered_map<string, string> get_fonts() {
    string esc = "\u001b[38;5;";
    unordered_map<string, string> map;
    for (int i = 0; i < 256; i++) {
        string code = std::to_string(i);
        map[code] = esc + code + 'm';
    }
    map["256"] = "\u001b[0m";
    return map;
}

unordered_map<string, string> get_bold_fonts() {
    string esc = "\u001b[38;5;";
    unordered_map<string, string> map;
    for (int i = 0; i < 256; i++) {
        string code = std::to_string(i);
        map[code] = esc + code + ";1m";
    }
    map["256"] = "\u001b[1m";
    return map;
}

unordered_map<string, string> get_backgrounds() {
    string esc = "\u001b[48;5;";
    unordered_map<string, string> map;
    for (int i = 0; i < 256; i++) {
        string code = std::to_string(i);
        map[code] = esc + code + 'm';
    }
    map["256"] = "\u001b[0m";
    return map;
}

void display(unordered_map<string, string> map, string font_color = "\u001b[0m") {
    string s[257];
    string reset = "\u001b[0m";

    for (int i = 0; i < 8; i++) {
        string key = std::to_string(i);
        cout << map[key] << ' ' << std::left
             << std::setw(3) << key << ' ';
    }
    cout << reset << "  " << font_color;
    for (int i = 8; i < 16; i++) {
        string key = std::to_string(i);
        cout << map[key] << ' ' << std::left
             << std::setw(3) << key << ' ';
    }
    cout << reset << "\n\n";

    int index = 16;
    for (int j = 0; j < 6; j++) {
        for (int k = 0; k < 3; k++) {
            cout << font_color;
            for (int l = 0; l < 6; l++) {
                string key = std::to_string(index);
                cout << map[key] << ' ' << std::left
                     << std::setw(3) << key << ' ';
                index++;
            }
            cout << reset << "  ";
        }
        cout << '\n';
        index += 18;
    }
    cout << '\n';

    index = 34;
    for (int j = 0; j < 6; j++) {
        for (int k = 0; k < 3; k++) {
            cout << font_color;
            for (int l = 0; l < 6; l++) {
                string key = std::to_string(index);
                cout << map[key] << ' ' << std::left
                     << std::setw(3) << key << ' ';
                index++;
            }
            cout << reset << "  ";
        }
        cout << '\n';
        index += 18;
    }
    cout << '\n';

    for (int i = 232; i < 244; i++) {
        string key = std::to_string(i);
        cout << map[key] << ' ' << std::left
             << std::setw(3) << key << ' ';
    }
    cout << reset << '\n' << font_color;
    for (int i = 244; i < 256; i++) {
        string key = std::to_string(i);
        cout << map[key] << ' ' << std::left
             << std::setw(3) << key << ' ';
    }

    cout << "\u001b[0m" << endl;;
}

bool is_label(const char* c) {
    char *ptr;
    long num;

    num = strtol(c, &ptr, 10);
    if (ptr == c) {
        return false;
    }
    if (num < 0 || num > 256) {
        return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    argparse::ArgumentParser args("ANSI escape code color lookup (256 colors)");
    args.add_argument("font")
    .help("Specicfy font color by a number (e.g. 3). B[number] represents bold font (e.g. B122). 256 is the default color.")
    .default_value(std::string(""));

    args.add_argument("background")
    .help("Specicfy background color by a number (e.g. 5). 256 is the default background color.")
    .default_value(std::string(""));

    args.add_argument("-f", "--font")
    .help("Display font numbers.")
    .default_value(false)
    .implicit_value(true);

    args.add_argument("-b", "--background")
    .help("Display background numbers.")
    .default_value(false)
    .implicit_value(true);

    try {
        args.parse_args(argc, argv);
    } catch (const std::runtime_error& err) {
        std::cout << err.what() << std::endl;
        exit(0);
    }

    if (argc == 1) {
        cout << "Default : \\u001b[0m" << endl;
        return 0;
    }


    string font = args.get<string>("font");
    string background = args.get<string>("background");
    bool show_font = args.get<bool>("-f");
    bool show_background = args.get<bool>("-b");

    unordered_map<string, string> fonts = get_fonts();
    unordered_map<string, string> bfonts = get_bold_fonts();
    unordered_map<string, string> backgrounds = get_backgrounds();

    if (show_font) {
        display(fonts);
    }
    if (show_background) {
        display(backgrounds, "\u001b[38;5;0m");
    }

    string demo, result;
    if (font != "") {
        if (font[0] == 'B') {
            const char *c = font.c_str();
            if (!is_label(c + 1)) {
                cout << "Invalid font label." << endl;
                exit(0);
            }
            if (font == "B256") {
                result= "\\u001b[1m";
            } else {
                result = "\\u001b[38;5;" + string(c + 1) + ";1m";
            }
            demo = bfonts[font.substr(1)];
        } else {
            if (!is_label(font.c_str())) {
                cout << "Invalid font label." << endl;
                exit(0);
            }
            if (font == "256") {
                result= "\\u001b[0m";
            } else {
                result = "\\u001b[38;5;" + font + "m";
            }
            demo = fonts[font];
        }
    } else
        return 0;

    if (background != "") {
        if (!is_label(background.c_str())) {
            cout << "Invalid background label." << endl;
            exit(0);
        }
        demo += backgrounds[background];
        if (background != "256") {
            result += "\\u001b[48;5;" + background + 'm';
        }
    }

    demo += ' ' + font;
    if (background != "")
        demo += ';' + background;
    demo += " \u001b[0m: ";

    cout << demo << result << endl;
    return 0;
}