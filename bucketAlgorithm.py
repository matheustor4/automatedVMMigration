import os
import subprocess
import xml.etree.ElementTree as ET
#from customtkinter import filedialog
import sys
import datetime

def saveXML(bRT, sdRT, bD, noB, bP, bL, sRT):
        xmlFields = {
            'baselineResponseTime': bRT,
            'baselineStandardDeviation': sdRT,
            'bucketDepth': bD,
            'numberOfBuckets': noB,
            'bucketPointer': bP,
            'bucketLoad': bL,
            'sampleResponseTime': sRT
            }
        
        root = ET.Element("variables")
        for key, value in xmlFields.items():
            child = ET.SubElement(root, key)
            child.text = str(value)

        file_path = "/home/matheus/go/bin/avm/test.xml"
        #file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding='utf-8', xml_declaration=True, method='xml')

def xmlToDict():
    tree = ET.parse("/home/matheus/go/bin/avm/test.xml")
    root = tree.getroot()
    data = {}

    for child in root:
        data[child.tag] = child.text

    return data


#def createDataFile():
#    f = open(("/home/matheus/AutomatedVMMig/BucketData.tsv"), "w")
#    f.close()
#    f = open(("/home/matheus/AutomatedVMMig/BucketData.tsv"), "a")
#    f.write("baselineResponseTime baselineStandardDeviation bucketDepth numberOfBuckets bucketPointer bucketLoad sampleResponseTime \n")
#    f.close()

def appendDataFile(dataString):
    f = open(("/home/matheus/go/bin/avm/BucketData.tsv"), "a")
    f.write(dataString)
    f.close()

def saveAlarm(alarm):
    f = open(("/home/matheus/go/bin/avm/ALARM"), "w")
    f.close()
    f = open(("/home/matheus/go/bin/avm/ALARM"), "a")
    f.write(alarm)
    f.close()


            
if __name__ == '__main__':
    
    sampleResponseTime = 1500
    xmlData = ''
    alarm = 0

    xmlData = xmlToDict()

    print(xmlData)

    baselineResponseTime = float(xmlData['baselineResponseTime'])
    baselineStandardDeviation = float(xmlData['baselineStandardDeviation'])
    bucketDepth = int(xmlData['bucketDepth'])
    numberOfBuckets = int(xmlData['numberOfBuckets'])
    bucketPointer = int(xmlData['bucketPointer'])
    bucketLoad = int(xmlData['bucketLoad'])


    sampleResponseTime = float(sys.argv[1])



    #bucket filling or taking
    if (sampleResponseTime > (baselineResponseTime + ((bucketPointer - 1) * baselineStandardDeviation))):
        bucketLoad = bucketLoad + 1
    else :
        bucketLoad = bucketLoad - 1
    
    #bucket full
    if bucketLoad > bucketDepth:
        bucketLoad = 0
        bucketPointer = bucketPointer + 1

    #bucket empty
    if bucketLoad < 0 and bucketPointer > 1:
        bucketLoad = bucketDepth
        bucketPointer = bucketPointer - 1
    
    #all buckets empty
    if bucketLoad < 0 and bucketPointer == 1:
        bucketLoad = 0;

    #all buckets full
    if bucketPointer > numberOfBuckets:
        ct = datetime.datetime.now()
        saveAlarm("1" + str(ct))
        alarm = 1
        subprocess.run(["/home/matheus/go/bin/avm/triggerMig.sh"])
    else:
        saveAlarm("0")
        alarm = 0
        #subprocess.run(["/home/matheus/go/bin/avm/triggerMig.sh"])


    ct = datetime.datetime.now()
    saveXML(baselineResponseTime, baselineStandardDeviation, bucketDepth, numberOfBuckets, bucketPointer, bucketLoad, sampleResponseTime)
    dataString = str(baselineResponseTime) + " " + str(baselineStandardDeviation) + " " +  str(bucketDepth) + " " +  str(numberOfBuckets) + " " +  str(bucketPointer) + " " +  str(bucketLoad) + " " +  str(sampleResponseTime) + " " + str(alarm) + " " + str(ct) + "\n"
    appendDataFile(dataString)  

