#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:30:40 2020

@author: bollam
"""

"""Complaints XML canonicalizer

Usage:
  canonical.py <file> [-o <out_file>]
  canonical.py (-h | --help)
  canonical.py --version
"""
import logging
import re
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET
from collections import OrderedDict
from operator import attrgetter

from docopt import docopt

logger = logging.getLogger("complaint_errors")


def sorted_attributes(node: ET.Element) -> OrderedDict:
    return OrderedDict([(k, node.attrib[k].strip()) for k in sorted(node.attrib.keys())])


def get_response(node: ET.Element) -> ET.Element:
    response = node.find('response')
    assert response.tag == "response"

    response = clone_element(response)

    timely = response.attrib['timely']
    response.attrib['timely'] = yesno_to_yn(timely)
    response.attrib = sorted_attributes(response)

    return response


def yesno_to_yn(yesno: str) -> str:
    return {'yes': 'Y', 'no': 'N'}.get(yesno, yesno)


def clone_element(src: ET.Element) -> ET.Element:
    clone = ET.Element(src.tag)
    clone.attrib = sorted_attributes(src)

    for e in src:
        e.tail = ""
        e.text = re.sub(r'\s+', ' ', e.text.strip())

    children = sorted(src, key=attrgetter('tag'))
    clone.extend(children)
    return clone


def copy_child(name: str, src: ET.Element, dst: ET.Element):
    elem = src.find(name)
    assert elem.tag == name

    clone = clone_element(elem)
    dst.append(clone)


def complaint(node: ET.Element):
    assert node.tag == "complaint"
    complaint_id = node.attrib['id']

    out = ET.Element('complaint')
    try:
        submission_type = node.attrib.get('submissionType') or node.find('submitted').attrib['via']
        out.attrib = OrderedDict([('id', complaint_id), ('submissionType', submission_type)])

        copy_child('company', node, out)

        consumer_narrative = node.find('consumerNarrative')
        if consumer_narrative is not None:
            consumer_narrative.tail = ""
            out.append(consumer_narrative)

        events = get_events(node)
        out.extend(events)

        copy_child('issue', node, out)
        copy_child('product', node, out)

        resp = get_response(node)
        out.append(resp)
    except:
        logger.error("complaint_id: %d", complaint_id)
        raise

    return out


def get_events(node):
    return map(clone_element, sorted(node.findall('event'), key=lambda n: n.attrib['type']))


def consumerComplaints(path: str) -> ET.Element:
    parser = ET.XMLParser()
    parser.entity["redaction"] = "XXXX"
    tree = ET.parse(path, parser=parser)
    root: ET.Element = tree.getroot()
    assert root.tag == 'consumerComplaints'

    complaints = list(map(complaint, root))
    out = ET.Element('consumerComplaints')
    children = sorted(complaints, key=lambda c: int(c.attrib['id']))
    out.extend(children)
    return out


def pretty_print_xml(tree: ET.ElementTree) -> str:
    dump = ET.tostring(tree)
    dom = xml.dom.minidom.parseString(dump)
    return dom.toprettyxml()


if __name__ == "__main__":
    arguments = docopt(__doc__, version="CS598 XML canonicalizer 1.0")
    tree = consumerComplaints(arguments["<file>"])
    xml = pretty_print_xml(tree)

    out_file = arguments["<out_file>"]
    if out_file:
        with open(out_file, "w") as f:
            f.write(xml)
    else:
        sys.stdout.write(xml)