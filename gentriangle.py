#!/usr/bin/env python3.9

# create an html document for Pascal's triangle

import sys
import argparse

import lxml.html as html
from lxml.html import builder as E

from readpascal import read_row

from pasc_latex import pascal
from rowpascal import rowpascal


# the minimum row that should be fully contained on the screen, i.e without
# having to scroll
MINROW = 25

base = \
    E.HTML(
        E.HEAD(
            E.TITLE("Pascal's Triangle"),
            E.STYLE("""
                div.triangle {{
                    overflow-x: hidden;
                    overflow-y: auto;
                    width: 95%;
                    height: 95%;
                    margin: 0 auto;
                    scrollbar-width: thin;
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                }}

                div.row {{
                    height: {0}%;
                    overflow-y: hidden;
                    overflow-x: auto;
                    text-align: center;
                    white-space: nowrap;
                    scrollbar-width: thin;
                }}

                div.number {{
                    border: 1px solid #e1c2c2;
                    width: {0}%;
                    height: 80%;
                    display: inline-block;
                    position: relative;
                }}

                div.number pre {{
                    overflow: hidden;
                    text-overflow: ellipsis;
                    width: 80%;
                    margin: 0;
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                }}

                div.number pre:hover {{
                    overflow: visible;
                    background-color: rgb(241, 157, 67);
                    width: auto;
                    height: auto;
                    z-index: 100;
                    font-size: 150%;

                ::-webkit-scrollbar-thumb {{
                    border-radius: 3px;
                }}
                }}
            """.format(100/(MINROW+1), 100/(MINROW+1)+2))
        ),

        E.BODY(
            E.DIV(
                E.CLASS("triangle"), id="container"
            ),

            onload = """
                c = document.getElementById("container")
                for (d of c.children) {
                    d.scrollLeft = d.scrollLeftMax / 2
                }
            """
        )
    )


def create_row(row):
    id = str(row[1]) if len(row) > 1 else '0'
    row_elt = E.DIV(E.CLASS("row"), id=id)
    for i in row:
        row_elt.append(
            E.DIV(E.CLASS("number"),
                  E.PRE(str(i)))
        )

    return row_elt


def create_document(files):
    container = base.find_class("triangle")[0]

    for f in files:
        container.append(create_row(read_row(f)))


def create_document2(n):
    container = base.find_class("triangle")[0]

    for r in pascal(n):
        container.append(create_row(r))


def create_document3(n):
    container = base.find_class("triangle")[0]

    for r in range(n):
        container.append(create_row(rowpascal(r)))


def create_parser():
    p = argparse.ArgumentParser()

    p.add_argument("files", type=str, nargs="*", help="list of files")

    p.add_argument("-r", "--maxrow", type=int, nargs="?", const=100, help="Specify a range for files to read")
    p.add_argument("-p", "--prefix", type=str, default="./", help="path prefix in which to look for files if --maxrow was specified")
    p.add_argument("-s", "--suffix", type=str, default=".rpas", help="specify the suffix for row files, including the dot")

    p.add_argument("-t", "--type", type=int, default=1, help="type 1: read rows from .rpas files, type 2: use recursive generator approach, type 3: use iterative approach but generate rows on the fly, in memory")

    p.add_argument("-o", "--out", type=str, default="stdout", help="where to write output")
    return p


def main():
    args = create_parser().parse_args()

    if (args.type == 2):
        create_document2(args.maxrow)

    elif (args.type == 3):
        create_document3(args.maxrow)

    else:
        if (not (args.files or args.maxrow)):
            print("You have to supply either a list of files or a maxrow as a range")
            quit()

        if (args.files):
            create_document(args.files)

        else:
            create_document([ args.prefix + str(i) + args.suffix for i in range(args.maxrow+1)])

    with (open(args.out, "wb") if args.out != "stdout" else sys.stdout.buffer as out):
        out.write(html.tostring(base))

if __name__ == "__main__":
    main()
