#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 13:34:39 2020

@author: bollam
"""

from lxml import etree

def dtd_validate():
    
    with open('./xml/Consumer_Complaints_FileA.xml', 'r', encoding='utf-8') as file:
        fileA = file.read()  # .encode(encoding='utf-8')

    with open('./xml/Consumer_Complaints_FileB.xml', 'r', encoding='utf-8') as file:
        fileB = file.read()  # .encode(encoding='utf-8')
        
    with open('./canonicalized_xml/Canonicalized_Consumer_Complaints_FileA.xml', 'r', encoding='utf-8') as file:
        canon_fileA = file.read()  # .encode(encoding='utf-8')

    with open('./canonicalized_xml/Canonicalized_Consumer_Complaints_FileB.xml', 'r', encoding='utf-8') as file:
        canon_fileB = file.read()  # .encode(encoding='utf-8')
        
    # DTD Validations
    print("DTD Validations")
    dtd_fileA = etree.DTD('./dtd/FileA.dtd')
    xml_fileA = etree.XML(fileA.encode('utf-8'))
    validate_A = dtd_fileA.validate(xml_fileA)
    print("validate fileA with dtd_fileA ", validate_A)
    
    dtd_fileB = etree.DTD('./dtd/FileB.dtd')
    xml_fileB = etree.XML(fileB.encode('utf-8'))
    validate_B = dtd_fileB.validate(xml_fileB)
    print("validate fileB with dtd_fileB ", validate_B)

    dtd_final = etree.DTD('./dtd/Final.dtd')
    xml_canon_fileA = etree.XML(canon_fileA.encode('utf-8'))
    validate_canon_A = dtd_final.validate(xml_canon_fileA)
    print("validate canonicalized_fileA with dtd_final ", validate_canon_A)
    
    xml_canon_fileB = etree.XML(canon_fileB.encode('utf-8'))
    validate_canon_B = dtd_final.validate(xml_canon_fileB)
    print("validate canonicalized_fileB with dtd_final ", validate_canon_B)

if __name__ == '__main__':
        dtd_validate()