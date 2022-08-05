#!/usr/bin/env python3

import sys, os
import argparse
import pandas as pd
import numpy as np
from skbio.tree import nj as nj
from skbio import DistanceMatrix as dm

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.stderr.write('\nerror: %s\n' % message)
        sys.exit(1)
    def print_help(self, file=None):
        if file is None:
            pass
        self._print_message(self.format_help(), file)

parser = MyParser(description=f"QuickSNP builds a NJ tree from a SNP distance matrix.",usage="QuickSNP <dm> <outtree>",add_help=True)
parser.add_argument("dm", help="SNP distance matrix CSV/TSV file with column headers and row names in square format.")
parser.add_argument("outtree", help="File name for Newick format tree.")
parser_args = parser.parse_known_args()
args = parser_args[0]

df = pd.read_csv(args.dm,sep=None,engine="python",index_col=0,header=0)
ids = list(df)
snp_array = df.to_numpy()
dm = dm(snp_array,ids)
newick_str = nj(dm, result_constructor=str)

with open(args.outtree, 'w') as outtree:
    outtree.write(newick_str)