#!/usr/bin/python3
"""
A script that converts Markdown to HTML.
"""

import sys
import os
import hashlib


def checkUsage(args):
    """
    Checks if the script is called properly.
    """
    err_msg = "Usage: ./markdown2html.py <input_file> <output_file>"
    if len(args) != 3:
        print(err_msg, file=sys.stderr)
        sys.exit(1)


def checkReadmeExists(readme):
    """
    Checks if the Markdown file exists.
    """
    if not (os.path.exists(readme) and os.path.isfile(readme)):
        print(f"Missing {readme}", file=sys.stderr)
        sys.exit(1)


def getReadmeLines(readme):
    """
    Reads in the readme file line by line.
    """
    with open(readme) as f:
        return [line.rstrip() for line in f]


def parseLowerMD5(lines):
    """
    Parses a line into MD5 (lowercase) the content.
    """
    html_lines = []
    for line in lines:
        line_list = line.replace('[[', ',||,').replace(']]', ',||,').split(',')

        i = 0
        j = i
        while i < len(line_list):
            line_part = line_list[i]
            if line_part == '||':

                j = i + 1
                while j < len(line_list):
                    if line_list[j] == '||':
                        line_list[i] = ''
                        line_list[j] = ''

                        if line_list[i+1] != '':
                            line_list[i+1] = create_md5_hash(line_list[i+1])

                        i = j
                        break
                    else:
                        j += 1
                i = j
            else:
                i += 1

        html_lines.append(''.join(line_list))

    return html_lines


def parse_case_insensitive_C(lines):
    """
    Parses a line into MD5 (lowercase) the content.
    """
    html_lines = []
    for line in lines:
        line_list = line.replace('((', ',||,').replace('))', ',||,').split(',')

        i = 0
        j = i
        while i < len(line_list):
            line_part = line_list[i]
            if line_part == '||':

                j = i + 1
                while j < len(line_list):
                    if line_list[j] == '||':
                        line_list[i] = ''
                        line_list[j] = ''

                        if line_list[i+1] != '':
                            line_list[i+1] = replace_all_C(line_list[i+1])

                        i = j
                        break
                    else:
                        j += 1
                i = j
            else:
                i += 1

        html_lines.append(''.join(line_list))

    return html_lines


def parseBold(lines):
    """
    Parses Bold.
    """
    html_lines = []
    for line in lines:
        line_list = line.replace('**', ',**,').split(',')

        i = 0
        j = i
        while i < len(line_list):
            line_part = line_list[i]
            if line_part == '**':
                j = i + 1
                while j < len(line_list):
                    if line_list[j] == '**':
                        line_list[i] = '<b>'
                        line_list[j] = '</b>'
                        i = j
                        break
                    else:
                        j += 1
                i = j
            else:
                i += 1

        html_lines.append(''.join(line_list))

    return html_lines


def parseEmphasis(lines):
    """
    Parses Emphasis.
    """
    html_lines = []
    for line in lines:
        line_list = line.replace('__', ',__,').split(',')

        i = 0
        j = i
        while i < len(line_list):
            line_part = line_list[i]
            if line_part == '__':
                j = i + 1
                while j < len(line_list):
                    if line_list[j] == '__':
                        line_list[i] = '<em>'
                        line_list[j] = '</em>'
                        i = j
                        break
                    else:
                        j += 1
                i = j
            else:
                i += 1

        html_lines.append(''.join(line_list))

    return html_lines


def parseHeadings(lines):
    """
    Parses the lines for headings.
    """
    html_lines = []
    for line in lines:
        level = 0

        while level < len(line) and line[level] == '#':
            level += 1

        if level > 0:
            heading_text = line[level+1:]
            html_lines.append(f"<h{level}>{heading_text}</h{level}>")
        else:
            html_lines.append(line)

    return html_lines


def parseUnorderedList(lines):
    """
    Parses the lines for Unordered Lists.
    """
    html_lines = []

    for line in lines:
        if line.startswith("- "):
            html_lines.append(f"<uli>{line.replace('- ', '', 1)}</uli>")
        else:
            html_lines.append(line)

    return wrapList(html_lines, 'ul')


def parseOrderedList(lines):
    """
    Parses the lines for Ordered Lists.
    """
    html_lines = []

    for line in lines:
        if line.startswith("* "):
            html_lines.append(f"<oli>{line.replace('* ', '', 1)}</oli>")
        else:
            html_lines.append(line)

    return wrapList(html_lines, 'ol')


def parseParagraph(lines):
    """
    Parses the lines for Paragraphs.
    """
    html_lines = []
    hasOpenParagraph = False
    i = 0
    while i < len(lines):
        line = lines[i]

        if not isEmptyLine(line) and isParagraph(line):
            if not hasOpenParagraph:
                html_lines.append('<p>')

            html_lines.append(line)
            # if next line is also a paragraph, insert a </br> tag
            next_line_index = i + 1
            if next_line_index < len(lines):
                next_line = lines[next_line_index]
                if not isEmptyLine(next_line) and isParagraph(next_line):
                    html_lines.append('</br>')

            hasOpenParagraph = True

        elif hasOpenParagraph:
            html_lines.append('</p>')
            hasOpenParagraph = False

        else:
            html_lines.append(line)

        i += 1

    if hasOpenParagraph:
        html_lines.append('</p>')

    return html_lines


def replace_all_C(line):
    """
    Replaces all c characters in a string.
    """
    return line.replace('c', '').replace('C', '')


def create_md5_hash(string):
    """
    Generates the md5 representation of a string
    """
    return hashlib.md5(string.encode()).hexdigest()


def isParagraph(line):
    """
    Checks if a line is a paragraph
    """
    return not line.startswith(('#', '- ', '* '))


def isEmptyLine(line):
    """
    Checks if a line is empty
    """
    return line == ''


def wrapList(lines=['a', 'b'], list_type='ul'):
    """
    Wraps a list in its proper parent element
    """
    i = 0
    while i < len(lines):
        line = lines[i]
        j = i

        if line.startswith(f'<{list_type}i>'):
            lines.insert(j, f'<{list_type}>')

            while ((j + 1) < len(lines)
                   and lines[j + 1].startswith(f'<{list_type}i>')):
                j += 1
                lines[j] = lines[j].replace(f'{list_type}i', 'li')

            lines.insert(j + 1, f'</{list_type}>')

        i = j + 1

    return lines


def writeLinesToFile(filename, lines):
    """
    Writes Lines to file
    """
    with open(filename, "w") as fp:
        fp.write("\n".join(lines))


def removeEmptyLines(lines):
    """
    Removes blank lines
    """
    i = 0
    html_lines = []

    while i < len(lines):
        line = lines[i]
        if line != '':
            html_lines.append(line)
        i += 1

    return html_lines


def convert_markdown_to_html(lines):
    """
    Converts a Markdown file to HTML.
    """
    functions = [
        parse_case_insensitive_C,
        parseLowerMD5,
        parseEmphasis,
        parseBold,
        parseParagraph,
        parseOrderedList,
        parseUnorderedList,
        parseHeadings,
        removeEmptyLines
    ]

    for fxn in functions:
        lines = fxn(lines)

    return lines


def main():
    """
    Converts a Markdown file to HTML and writes the output to a file.
    """
    argv = sys.argv
    checkUsage(argv)

    readme = argv[1]
    checkReadmeExists(readme)

    readme_html = argv[2]

    lines = getReadmeLines(readme)

    html_lines = convert_markdown_to_html(lines)

    writeLinesToFile(readme_html, html_lines)

    sys.exit(0)


if __name__ == "__main__":
    main()
