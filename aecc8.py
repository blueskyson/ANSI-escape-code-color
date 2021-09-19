import sys
import argparse


def get_fonts():
    esc = "\u001b["
    fonts = {}
    for i in range(30, 38):
        fonts[str(i - 30)] = esc + str(i) + "m"
    fonts["8"] = "\u001b[0m"
    return fonts


def get_bold_fonts():
    esc = "\u001b["
    fonts = {}
    for i in range(30, 38):
        fonts["B" + str(i - 30)] = esc + str(i) + ";1m"
    fonts["B8"] = "\u001b[1m"
    return fonts


def get_backgrounds():
    esc = "\u001b["
    bgs = {}
    for i in range(40, 48):
        bgs[str(i - 40)] = esc + str(i) + "m"
    bgs["8"] = "\u001b[0m"
    return bgs


def display(_dict):
    line = ""
    for key in _dict:
        line += _dict[key] + " " + key.ljust(4) + " "
    line += "\u001b[0m"
    print(line)


def main():
    parser = argparse.ArgumentParser(
        description="A tool for looking up ANSI escape code colors (8 colors)"
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
        help="Specicfy font color by a label, D represents default color, e.g. 3, B3, D",
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
            demo = bfonts[args.font]
            num = 0 if args.font == "B8" else int(args.font[1:]) + 30
            result = "\\u001b[" + str(num) + ";1m"
        else:
            if args.font not in fonts:
                print("Invalid font label.")
                return
            num = 0 if args.font == "8" else int(args.font) + 30
            demo = fonts[args.font]
            result = "\\u001b[" + str(num) + "m"
    else:
        return

    if args.background != "":
        if args.background not in backs:
            print("Invalid background label.")
            return
        num = 0 if args.background == "8" else int(args.background) + 40
        demo += backs[args.background]
        result += "\\u001b[" + str(num) + "m"

    demo += " " + args.font
    if args.background != "":
        demo += ";" + args.background
    demo += " \u001b[0m: "
    print(demo + result)


if __name__ == "__main__":
    main()
