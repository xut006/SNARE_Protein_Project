import numpy as np
import requests
from bs4 import BeautifulSoup as BS

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


# searchUniport function
# input:
#   filename: string
#             the filename of a list of Protein ids 
# output:
#   a file with all the organism names matched to the protein ids
def searchUniport (filename):
  outFile = open("organism.txt", "w")
  proteinIDs = open(filename, "r")
  for protein in proteinIDs:
    text = requests.get('http://www.uniprot.org/uniprot/' + protein).text
    soup = BS(text)
    title = soup.head.title.text
    organism = title.split(" - ")[2]
    outFile.write(organism + "\n")


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
proteinIDs = "SNARE_proteins_bacteria.txt"
# get organism names from Uniport
searchUniport(proteinIDs)
# Determine if TB is in the orgnanism list
query = "Mycobacterium tuberculosis"
organism = "organism.txt"
result = queryOrg(query, organism)
print (result)


