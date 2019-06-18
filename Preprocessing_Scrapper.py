from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
from os import path 
import os 
import xlrd
import re
import pandas as pd

'''
Edited by -- Kelechi Ogudu 
Time of Edit -- 6/15/2019
Title        -- Preprocessing_Scrapper.py 
'''


def load_data(file_path, sheet_name):
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    return data


def create_url(data):
    """

    :param data: panda data frame
    :return: url column created by concatenating 'Project_Name' and 'Commit_ID'
    """
    url_list = []
    for ii in range(len(data)):
        split_proj_name = data["Project_Name"].loc[ii].split("-", 1)
        organization = split_proj_name[0]
        project = split_proj_name[1]
        url_list.append("https://github.com/" + organization + "/" + project + "/commit/" +
                        str(data["Commit_ID"].loc[ii]))
    data["Commit_URL"] = url_list
    return data


file_path = ''
if not path.exists("Neutral_Breaker.xlsx"):
    print("upload 'Neutral_Breaker.xlsx' to current working directory!")
else:
    pwd = os.getcwd()
    file_path += pwd + '\\Neutral_Breaker.xlsx'
neutral = load_data(file_path, "Neutral_url")
breaker = load_data(file_path, "Breaker_url")
neutral = create_url(neutral)
breaker = create_url(breaker)

def parse_urls(data):
    """
    parses the url within data["Commit_URL"] and classifies the commit
    as either 'Build', 'Testing', 'Maintenance' based on changes to files in diffs.

    :param data: pandas data frame
    :return: pandas data frame with three new binary columns 'Testing', 'Maintenance', 'Build'
    """
    testing = [0] * len(data["Commit_URL"])
    build = [0] * len(data["Commit_URL"])
    maintenance = [0] * len(data["Commit_URL"])
    for ii in range(len(data["Commit_URL"])):
        try:
            html = urlopen(data["Commit_URL"].iloc[ii])
            bsObj = BeautifulSoup(html, "html.parser")
            paths = bsObj.findAll("a", {"href": re.compile(r"#diff-[a-z0-9]+")})
            for path in paths:
                if len(path.attrs) == 1:
                    if re.match(r".*(build|pom).*", str(path)):
                        build[ii] = 1
                    if re.match(r".*(test|tests|tester).*", str(path)):
                        testing[ii] = 1
                    if re.match(r".*(u|U)til.*", str(path)) or re.match(r".*(h|H)elper.*", str(path)):
                        maintenance[ii] = 1
        except HTTPError as e:
            print(data["Commit_ID"].iloc[ii])
        except URLError as e:
            print("The server could not be found!")
    data["Testing"] = testing
    data["Build"] = build
    data["Maintenance"] = maintenance
    return data


neutral = parse_urls(neutral)
breaker = parse_urls(breaker)