# Copyright 2016, The James Hutton Insitute
# Author: Leighton Pritchard
#
# This code is part of the pyani package, and is governed by its licence.
# Please see the LICENSE file that should have been included as part of
# this package.

"""Code to support pyani."""

import pandas as pd


# Class to hold ANI dataframe results
class ANIResults(object):
    """Holds ANI dataframe results."""
    def __init__(self, labels):
        """Initialise with four empty, labelled dataframes."""
        self.alignment_lengths = pd.DataFrame(index=labels, columns=labels,
                                              dtype=float)
        self.similarity_errors = pd.DataFrame(index=labels, columns=labels,
                                              dtype=float).fillna(0)
        self.percentage_identity = pd.DataFrame(index=labels, columns=labels,
                                                dtype=float).fillna(1.0)
        self.alignment_coverage = pd.DataFrame(index=labels, columns=labels,
                                               dtype=float).fillna(1.0)
        self.zero_error = False

    def add_tot_length(self, qname, sname, value, sym=True):
        """Add a total length value to self.alignment_lengths."""
        self.alignment_lengths.loc[qname, sname] = value
        if sym:
            self.alignment_lengths.loc[sname, qname] = value

    def add_sim_errors(self, qname, sname, value, sym=True):
        """Add a similarity error value to self.similarity_errors."""
        self.similarity_errors.loc[qname, sname] = value
        if sym:
            self.similarity_errors.loc[sname, qname] = value

    def add_pid(self, qname, sname, value, sym=True):
        """Add a percentage identity value to self.percentage_identity."""
        self.percentage_identity.loc[qname, sname] = value
        if sym:
            self.percentage_identity.loc[sname, qname] = value

    def add_coverage(self, qname, sname, qcover, scover=None):
        """Add percentage coverage values to self.alignment_coverage."""
        self.alignment_coverage.loc[qname, sname] = qcover
        if scover:
            self.alignment_coverage.loc[sname, qname] = scover

    @property
    def hadamard(self):
        """Return Hadamard matrix (identity * coverage)."""
        return self.percentage_identity * self.alignment_coverage

    @property
    def data(self):
        """Return list of (dataframe, filestem) tuples."""
        return [(self.alignment_lengths, "ANIm_alignment_lengths"),
                (self.percentage_identity, "ANIm_percentage_identity"),
                (self.alignment_coverage, "ANIm_alignment_coverage"),
                (self.similarity_errors, "ANIm_similarity_errors"),
                (self.hadamard, "ANIm_hadamard")]


# Read sequence annotations in from file
def get_labels(filename, logger=None):
    """Returns a dictionary of alternative sequence labels, or None

    - filename - path to file containing tab-separated table of labels

    Input files should be formatted as <key>\t<label>, one pair per line.
    """
    labeldict = {}
    if filename is not None:
        if logger:
            logger.info("Reading labels from %s", filename)
        with open(filename, 'rU') as fh:
            count = 0
            for line in fh.readlines():
                count += 1
                try:
                    key, label = line.strip().split('\t')
                except ValueError:
                    if logger:
                        logger.warning("Problem with class file: %s",
                                       filename)
                        logger.warning("%d: %s", (count, line.strip()))
                        logger.warning("(skipping line)")
                    continue
                else:
                    labeldict[key] = label
    return labeldict