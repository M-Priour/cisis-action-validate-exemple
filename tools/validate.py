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
    time.sleep(3)
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
    resultHtml= transform(dom,nameFile=etree.XSLT.strparam(nameFile),elapsedTime=etree.XSLT.strparam(time))
    print(resultHtml,file=open(file_output, "a"))


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

#Validation METADATA
for p in glob.iglob(dir_path_exemple+'/**/METADATA.XML', recursive=True):
    print("---file :" +  p)
    start_time = time.time()
    locationRepport = validate(p,"Model-based XDS Validator","ASIP XDM ITI-32 FR Distribute Document Set on Media")
    rapport = getRepport(locationRepport)
    end_time = time.time()
    print("-------Rapport  :" +  locationRepport)
    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))

#Validation CDA
for p in glob.iglob(dir_path_exemple+'/**/*xml', recursive=True):
    if '<ClinicalDocument' in open(p).read():
        print("---file :" +  p)
        start_time = time.time()
        locationRepport = validate(p,"Schematron Based CDA Validator",".Structuration minimale des documents de santé v1.16")
        rapport = getRepport(locationRepport)
        end_time = time.time()
        print("-------Rapport  :" +  locationRepport)
        transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))

#Validation HL7
for p in glob.iglob(dir_path_exemple+'/**/*.*', recursive=True):
    if(os.path.isfile(p)):
        if 'MSH|' in open(p, errors='ignore').read():
            if 'ORU^R01^ORU_R01' in open(p, errors='ignore').read():        
                if '2.1^CISIS_CDA_HL7_V2' in open(p).read():                
                    print("---file :" +  p)
                    start_time = time.time()
                    locationRepport = validate(p,"Gazelle HL7v2.x validator","1.3.6.1.4.1.12559.11.36.8.3.19")
                    rapport = getRepport(locationRepport)
                    end_time = time.time()
                    print("-------Rapport  :" +  locationRepport)
                    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))
            if 'MDM^T02^MDM_T02' in open(p, errors='ignore').read():        
                if '2.1^CISIS_CDA_HL7_V2' in open(p, errors='ignore').read():                
                    print("---file :" +  p)
                    start_time = time.time()
                    locationRepport = validate(p,"Gazelle HL7v2.x validator","1.3.6.1.4.1.12559.11.36.8.3.24")
                    rapport = getRepport(locationRepport)
                    end_time = time.time()
                    print("-------Rapport  :" +  locationRepport)
                    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))      
            if 'MDM^T04^MDM_T02' in open(p, errors='ignore').read():        
                if '2.1^CISIS_CDA_HL7_V2' in open(p, errors='ignore').read():                
                    print("---file :" +  p)
                    start_time = time.time()
                    locationRepport = validate(p,"Gazelle HL7v2.x validator","1.3.6.1.4.1.12559.11.36.8.3.25")
                    rapport = getRepport(locationRepport)
                    end_time = time.time()
                    print("-------Rapport  :" +  locationRepport)
                    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))                      
            if 'MDM^T10^MDM_T02' in open(p, errors='ignore').read(): 
                if '2.1^CISIS_CDA_HL7_V2' in open(p, errors='ignore').read():                
                    print("---file :" +  p)
                    start_time = time.time()
                    locationRepport = validate(p,"Gazelle HL7v2.x validator",	"1.3.6.1.4.1.12559.11.36.8.3.21")
                    rapport = getRepport(locationRepport)
                    end_time = time.time()
                    print("-------Rapport  :" +  locationRepport)
                    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))          
            if 'MDM^T02^MDM_T02' in open(p, errors='ignore').read():        
                if '1.1^CISIS_CDA_HL7_LPS' in open(p, errors='ignore').read():                
                    print("---file :" +  p)
                    start_time = time.time()
                    locationRepport = validate(p,"Gazelle HL7v2.x validator",	"1.3.6.1.4.1.12559.11.36.8.3.20")
                    rapport = getRepport(locationRepport)
                    end_time = time.time()
                    print("-------Rapport  :" +  locationRepport)
                    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))     
            if 'MDM^T10^MDM_T02' in open(p, errors='ignore').read():        
                if '1.1^CISIS_CDA_HL7_LPS' in open(p, errors='ignore').read():                
                    print("---file :" +  p)
                    start_time = time.time()
                    locationRepport = validate(p,"Gazelle HL7v2.x validator","1.3.6.1.4.1.12559.11.36.8.3.23")
                    rapport = getRepport(locationRepport)
                    end_time = time.time()
                    print("-------Rapport  :" +  locationRepport)
                    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))     
            if 'MDM^T04^MDM_T02' in open(p, errors='ignore').read():        
                if '1.1^CISIS_CDA_HL7_LPS' in open(p, errors='ignore').read():                
                    print("---file :" +  p)
                    start_time = time.time()
                    locationRepport = validate(p,"Gazelle HL7v2.x validator",	"1.3.6.1.4.1.12559.11.36.8.3.25")
                    rapport = getRepport(locationRepport)
                    end_time = time.time()
                    print("-------Rapport  :" +  locationRepport)
                    transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))   
            if '2.11~IHE_FRANCE-2.11-PAM' in open(p, errors='ignore').read():  
                print("---file :" +  p)
                start_time = time.time()
                locationRepport = validate(p,"Gazelle HL7v2.x validator","2.16.840.1.113883.2.8.3.1.1")
                rapport = getRepport(locationRepport)
                end_time = time.time()
                print("-------Rapport  :" +  locationRepport)
                transformReport(rapport,github_action_path,file_output,p,str(end_time - start_time))                  
        
