#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""WK13 warmup task 01 - Opening and reading a CSV file."""


import csv
import json


GRADES = {'A': 1.,
          'B': .9,
          'C': .8,
          'D': .7,
          'F': .6}


def get_score_summary(filename):
    """A function to loop through CSV data.

    Args:
        filename(file): A csv file.

    Returns:
        dict: A new dictionary.

    Examples:
    >>> get_score_summary('inspection_results.csv')
    {'BRONX': (156, 0.9762820512820514),
    'BROOKLYN': (417, 0.9745803357314141),
    'STATEN ISLAND': (46, 0.9804347826086955),
    'MANHATTAN': (748, 0.9771390374331531),
    'QUEENS': (414, 0.9719806763285017)}

    """

    fhandler = open(filename, 'r')
    csv_file = csv.reader(fhandler)
    mydata1 = {}

    for line in csv_file:
        if line[0] not in mydata1 and line[10] in GRADES:
            mydata1.update({line[0]: [line[10], line[1]]})

    fhandler.close()

    mydata2 = {}

    for item in mydata1.itervalues():
        if item[1] not in mydata2:
            mydata2[item[1]] = [1, GRADES[item[0]]]
        else:
            mydata2[item[1]][0] += 1
            mydata2[item[1]][1] += GRADES[item[0]]

    mydata3 = {}

    for boro, grade in mydata2.iteritems():
        mydata3[boro] = grade[0], grade[1]/grade[0]

    return mydata3


def get_market_density(filename):
    """A function using JSON.

    Args:
        filename(file): A json file.

    Returns:
        dict: A new dictionary.

    Example:
    >>> get_market_density('green_markets.json')
    {u'Staten Island': 2, u'Brooklyn': 48, u'Bronx': 32,
    u'Manhattan': 39, u'Queens': 16}

    """

    fhandler = open(filename, 'r')
    jsondata = json.load(fhandler)["data"]
    result = {}
    fhandler.close()

    for item in jsondata:
        item[8] = item[8].strip()
        if item[8] not in result.iterkeys():
            value = 1
        else:
            value = result[item[8]] + 1
        result[item[8]] = value
        result.update(result)
    return result


def correlate_data(firstarg='inspection_results.csv',
                   secondarg='green_markets.json',
                   thirdarg='finalresult.json'):
    """Combining the two pieces of data.

    Args:
        firstarg(file): A default csv file.
        secondarg(file): A default json file.
        thirdarg(file): The resulting json file.

    Returns:
        JSON writing function that fills in the thirdarg file.

    """

    score = get_score_summary(firstarg)
    market = get_market_density(secondarg)
    result = {}
    for item2 in market.iterkeys():
        for item1 in score.iterkeys():
            if item1 == str(item2).upper():
                value1 = score[item1][1]
                value2 = float(market[item2])/(score[item1][0])
                result[item2] = (value1, value2)
                result.update(result)
    jsondata = json.dumps(result)

    fhandler = open(thirdarg, 'w')
    fhandler.write(jsondata)
    fhandler.close()
