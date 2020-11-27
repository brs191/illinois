#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 15:18:41 2020

@author: bollamr2
"""
import hashlib

def checksums():
    
    with open('./xml/Consumer_Complaints_FileA.xml', 'r', encoding='utf-8') as file:
        fileA = file.read()  # .encode(encoding='utf-8')

    with open('./xml/Consumer_Complaints_FileB.xml', 'r', encoding='utf-8') as file:
        fileB = file.read()  # .encode(encoding='utf-8')
        
    md5_fileA = hashlib.md5(fileA.encode(encoding='utf-8')).hexdigest()
    md5_fileB = hashlib.md5(fileB.encode(encoding='utf-8')).hexdigest()
    
    with open('./canonicalized_xml/Canonicalized_Consumer_Complaints_FileA.xml', 'r', encoding='utf-8') as file:
        canon_fileA = file.read()  # .encode(encoding='utf-8')

    with open('./canonicalized_xml/Canonicalized_Consumer_Complaints_FileB.xml', 'r', encoding='utf-8') as file:
        canon_fileB = file.read()  # .encode(encoding='utf-8')
        
    canon_md5_fileA = hashlib.md5(canon_fileA.encode(encoding='utf-8')).hexdigest()
    canon_md5_fileB = hashlib.md5(canon_fileB.encode(encoding='utf-8')).hexdigest()
    print("MD5-Checksums")
    print("md5-checksum for FileA: ", md5_fileA)
    print("md5-checksum for FileB: ", md5_fileB)
    print("md5-checksum for Canonicalized_FileB: ", canon_md5_fileA)
    print("md5-checksum for Canonicalized_FileB: ", canon_md5_fileB)

if __name__ == '__main__':
        checksums()