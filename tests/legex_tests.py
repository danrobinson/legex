from nose.tools import *
from legex import Parser
import requests
from lxml import html as ET

def setup():
    print "Setting up."

def test_parse():
    
    r = requests.get("https://bulk.resource.org/courts.gov/c/US/544/544.US.1.03-1395.html")
    
    t = r.text
    
    root = ET.fromstring(t.encode("utf-8"))

    parser = Parser()

    for div in root[1].findall("div"):
        for p in div.findall("p"):
            paragraph = p.text_content()
            parser.parse(paragraph)

def teardown():
    print "Tearing down."