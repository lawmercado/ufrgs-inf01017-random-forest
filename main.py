#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
import csv
import logging
import sys
import argparse

from data.handler import DataHandler
from ml.supervised.algorithms import decision_tree_classification
from ml.supervised.algorithms import random_trees_classification


def setup_logger():

    class MyFilter(object):
        def __init__(self, level):
            self.__level = level

        def filter(self, log_record):
            return log_record.levelno <= self.__level

    logger = logging.getLogger("main")

    formater = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
    handler1 = logging.FileHandler('usr.log', mode="w")
    handler1.setLevel(logging.INFO)
    handler1.filter(MyFilter(logging.INFO))
    handler1.setFormatter(formater)
    logger.addHandler(handler1)

    handler2 = logging.FileHandler('dev.log', mode="w")
    handler2.setLevel(logging.DEBUG)
    handler2.filter(MyFilter(logging.DEBUG))
    handler2.setFormatter(formater)
    logger.addHandler(handler2)

    logger.setLevel(logging.INFO)

    return logger


if __name__ == '__main__':
    logger = setup_logger()

    filename = "sets/benchmark.csv"
    delimiter = ";"
    class_attr = "Joga"

    dsets = ["benchmark", "diabetes"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="enables debugging", action="store_true")
    parser.add_argument("-ds", "--data_set", type=str, help="the data set to test. Options are " + str(dsets))

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.data_set is not None:
        if args.data_set in dsets:
            filename = ""
            delimiter = ""
            class_attr = ""

            if args.data_set.strip() == "benchmark":
                filename = "sets/benchmark.csv"
                delimiter = ";"
                class_attr = "Joga"

            elif args.data_set.strip() == "diabetes":
                filename = "sets/diabetes.csv"
                delimiter = ","
                class_attr = "Outcome"

            rows = list(csv.reader(open(filename, "r"), delimiter=delimiter))
            data_handler = DataHandler(rows, class_attr)

            test_instances = [instance[0] for instance in data_handler.as_instances()][0:6]

            print("Processing...")

            logger.info(random_trees_classification(data_handler, test_instances, 10))

            print("See the log output is in dev.log")

        else:
            raise AttributeError("Data set is not supported!")

    else:
        print("Nothing to do here...")
