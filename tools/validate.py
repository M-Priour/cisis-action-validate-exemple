import requests
import xml.etree.ElementTree as ET
import lxml
import base64
import os,re,shutil
import fileinput
import sys
import glob 
import time


github_action_path = sys.argv[1] 
dir_path_exemple =  sys.argv[2] 
file_output = sys.argv[3] 


url = 'https://interop.esante.gouv.fr/evs/rest/validations'

def validate(fileName,validationServiceName,validationserviceValidator):

    #Validation
    validation = ET.Element('validation')
    validation.set("xmlns", "http://evsobjects.gazelle.ihe.net/")
    validationService = ET.SubElement(validation, 'validationService')
    validationService.set("xmlns", "http://evsobjects.gazelle.ihe.net/")
    validationService.set("name", validationServiceName )
    validationService.set("validator", validationserviceValidator)

    validationObject = ET.SubElement(validation, 'object')
    validationObject.set("xmlns", "http://evsobjects.gazelle.ihe.net/")
    validationObject.set("originalFileName", "nomdufichier.txt")

    validationContent = ET.SubElement(validationObject, 'content')

    with open(fileName, mode="rb") as validate_file:
        contents = validate_file.read()

    docbase64  = base64.b64encode(bytes(contents)).decode('ascii')
    validationContent.text = str(docbase64)
    tree = ET.ElementTree(validation)
    validate_data = ET.tostring(validation)

    headers = {'Content-Type': 'application/xml'}
    res =  requests.post(url, data=validate_data, headers=headers)
    locationRapport = (res.headers["X-Validation-Report-Redirect"])
    return locationRapport


def getRepport(locationRepport):
    #Recuperation du rapport de validation
    headers = {'accept': 'application/xml'}
    rapport = requests.get(locationRepport +"?severityThreshold=WARNING" +"", headers=headers)
    return rapport

def transformReport(rapport,github_action_path,file_output,nameFile,time):
    #Parsing svrl to html
    from lxml import etree
    parser = etree.ETCompatXMLParser()
    xsl = etree.parse(github_action_path +'/tools/svrl-to-html.xsl')
    dom = etree.fromstring(rapport.content,parser)

    transform = etree.XSLT(xsl)
    resultHtml= etree.tostring(transform(dom,nameFile=etree.XSLT.strparam(nameFile),elapsedTime=etree.XSLT.strparam(time)), pretty_print=True)
    with open(file_output, "a") as f:
        f.write(str(resultHtml))

print("source : " +dir_path_exemple)
print("output : " +     file_output)    

#Validation DICOM
for p in glob.iglob(dir_path_exemple+'/**/*.dcm', recursive=True):
    print("---file :" +  p)
    start_time = time.time()
    locationRepport = validate(p,"Dicom3tools","DICOM Standard Conformance")
    rapport = getRepport(locationRepport)
    end_time = time.time()
    print("-------Rapport  :" +  locationRepport)
    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))
