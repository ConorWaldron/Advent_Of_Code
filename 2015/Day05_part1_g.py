# g.py taken from optum aoc repo for day 5 2015
import datetime

start_time = datetime.datetime.now()

#import sys
import re


def load_input(fname):
    with open(fname, "r") as f:
        file = f.read().strip()
        word_list = file.split("\n")
        return word_list


def part_a(word_list):
    repeated_char = re.compile(r"\S*(.)\1\S*")
    three_vowels = re.compile(r"(.*[aeiou]){3,}")
    bad_combi = re.compile(r"^(?!.*(ab|cd|pq|xy)).*$")

    repeated_char_list = list(filter(repeated_char.match, word_list))
    vowels_list = list(filter(three_vowels.match, repeated_char_list))
    final = list(filter(bad_combi.match, vowels_list))
    return final


def main(fname):
    word_list = load_input(fname)
    print('Answer to part a is {}'.format(len(part_a(word_list))))
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
    print("Time taken to get answer: {:.3f} ms".format(processing_time))

"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: python [script.py] [input.txt]")
    else:
        main(sys.argv[1])
"""
if __name__ == "__main__":
    main('input.txt')