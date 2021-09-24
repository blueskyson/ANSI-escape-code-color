# MIT License
# Copyright (c) 2021 Lin Cheng Chieh <https://github.com/blueskyson>


import sys
import argparse


def get_fonts():
    esc = "\u001b[38;5;"
    fonts = {}
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            fonts[code] = esc + code + "m"
    fonts["256"] = "\u001b[0m"
    return fonts


def get_bold_fonts():
    esc = "\u001b[38;5;"
    fonts = {}
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            fonts["B" + code] = esc + code + ";1m"
    fonts["B256"] = "\u001b[1m"
    return fonts


def get_backgrounds():
    esc = "\u001b[48;5;"
    bgs = {}
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            bgs[code] = esc + code + "m"
    bgs["256"] = "\u001b[0m"
    return bgs


def display(_dict):
    keys = list(_dict.keys())
    for i in range(0, 16):
        line = ""
        for j in range(0, 16):
            key = keys[i * 16 + j]
            line += _dict[key] + " " + key.ljust(4) + " "
        print(line + "\u001b[0m")
    print(_dict[keys[-1]] + " " + keys[-1].ljust(4) + "\u001b[0m")


def main():
    parser = argparse.ArgumentParser(
        description="A tool for looking up ANSI escape code colors (256 colors)"
    )
    parser.add_argument(
        "-f",
        "--show-font",
        action="store_true",
        default=False,
        help="Display font colors",
    )
    parser.add_argument(
        "-b",
        "--show-background",
        action="store_true",
        default=False,
        help="Display background colors",
    )
    parser.add_argument(
        "font",
        type=str,
        nargs="?",
        default="",
        help="Specicfy font color by a label, 256 represents default color, e.g. 3, B3",
    )
    parser.add_argument(
        "background",
        type=str,
        nargs="?",
        default="",
        help="Specicfy background color by a label, e.g. 5",
    )
    args = parser.parse_args()

    fonts = get_fonts()
    bfonts = get_bold_fonts()
    backs = get_backgrounds()

    if len(sys.argv) == 1:
        print("Default : \\u001b[0m")
        return

    if args.show_font:
        print("Fonts:")
        display(fonts)
        print("Bold Fonts:")
        display(bfonts)
    if args.show_background:
        print("Backgrounds:")
        display(backs)

    result = ""
    demo = ""
    if args.font != "":
        if args.font[0] == "B":
            if args.font not in bfonts:
                print("Invalid font label.")
                return
            if args.font == "B256":
                result= "\\u001b[1m"
            else:
                result = "\\u001b[38;5;" + str(int(args.font[1:])) + ";1m"
            demo = bfonts[args.font]
        else:
            if args.font not in fonts:
                print("Invalid font label.")
                return
            if args.font == "256":
                result= "\\u001b[0m"
            else:
                result = "\\u001b[38;5;" + args.font + "m"
            demo = fonts[args.font]
    else:
        return

    if args.background != "":
        if args.background not in backs:
            print("Invalid background label.")
            return
        demo += backs[args.background]
        if args.background != "256":
            result += "\\u001b[48;5;" + args.background + "m"

    demo += " " + args.font
    if args.background != "":
        demo += ";" + args.background
    demo += " \u001b[0m: "
    print(demo + result)


if __name__ == "__main__":
    main()
