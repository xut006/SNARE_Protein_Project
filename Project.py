import numpy as np
import requests
from bs4 import BeautifulSoup as BS


# downloadProteinID function 
# input: 
#   None
# output:
#   the name of the file contains a list of proteins IDs downloaded from InterPro
def downloadProteinID ():
  url = "http://www.ebi.ac.uk/interpro/entry/IPR010989/proteins-matched?taxonomy=2&export=ids"
  r = requests.get(url, allow_redirects=True)
  open("SNARE_proteins_bacteria.txt", 'wb').write(r.content)
  return "SNARE_proteins_bacteria.txt"


# getProteinID function 
# input: 
#   filename: string 
#             the filename of a fasta file
# output:
#   a list of all the protein ids in the fasta file
def getProteinID (filename):
  f = open(filename, "r")
  IDs = []
  for line in f:
    if line[0] == ">":
      ID = line[1:]
      IDs = np.append(IDs, ID)
  return IDs


# searchUniport_stable function
# input:
#   filename: string
#             the filename of a list of Protein ids 
# output:
#   a file with all the organism names matched to the protein ids and the
#   corresponding freqency of apperance
# SideNote: This function accomplish the smae goal as searchUniport_fast, but
#           this function accomplish the goal with uniprot api, where the 
#           result is stable but rather slow, which could take up to 10 mins.
def searchUniport_stable (filename):
  outFile = open("organism.txt", "w")
  proteinIDs = open(filename, "r")
  orgDic = {}
  for protein in proteinIDs:
    url = "https://www.uniprot.org/uniprot/?query=id:" + protein + "&columns=organism&format=tab"
    print("before")
    result = requests.get(url).content
    print ("after")
    organism = str(result).split("\\n")[1]
    if organism in orgDic:
      orgDic[organism] = orgDic[organism] + 1
    else:
      orgDic[organism] = 1
  for org_freqs in sorted(orgDic, key=orgDic.get, reverse=True):
    outFile.write(str(orgDic[org_freqs]) + " " + org_freqs + "\n")


# searchUniport_fast function
# input:
#   filename: string
#             the filename of a list of Protein ids 
# output:
#   a file with all the organism names matched to the protein ids and the
#   corresponding freqency of apperance
# SideNote: This function accomplish the smae goal as searchUniport_stable, but
#           accomplish the goal with python's BeautifulSoup package, where the 
#           result could be unstable but faster than using Uniport API. 
def searchUniport_fast (filename):
  outFile = open("organism.txt", "w")
  proteinIDs = open(filename, "r")
  orgDic = {}
  for protein in proteinIDs:
    text = requests.get('http://www.uniprot.org/uniprot/' + protein).text
    soup = BS(text)
    title = soup.head.title.text
    organism = title.split(" - ")[2]
    if organism in orgDic:
      orgDic[organism] = orgDic[organism] + 1
    else:
      orgDic[organism] = 1
  for org_freqs in sorted(orgDic, key=orgDic.get, reverse=True):
    outFile.write(str(orgDic[org_freqs]) + " " + org_freqs + "\n")


# queryOrg function
# input: 
#   queryName: string
#              the name of organism we want check if it's in the organism list
#   orgFile: string
#            the name of the file output by searchUniport function, which contains
#            all the organism names that have a specific protein fanmily
# output:
#   a boolean that tells if the query organism is in the organisms list
def queryOrg (queryName, orgFile):
  f = open(orgFile, "r")
  for org in f:
    lowerOrg = org.lower()
    qLower = queryName.lower()
    if qLower in lowerOrg:
      return True
  return False
  


   
# protein ids download from InterPor
proteinIDs = downloadProteinID ()
# get organism names from Uniport
searchUniport(proteinIDs)
searchUniport("SNARE_proteins_bacteria.txt")
# Determine if TB is in the orgnanism list
query = "Mycobacterium tuberculosis"
organism = "organism.txt"
result = queryOrg(query, organism)
print (result)


