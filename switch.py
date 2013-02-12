import re
from re import search, sub
from subprocess import call
from tempfile import mkstemp
from os import remove, close
from shutil import move
#!/usr/bin/env python


	
def matchImages(projectFilePath):
	file = open(projectFilePath)
	xproj = file.read()

	appIds = getResourceIds(xproj)
	xmlResources = getXMLResources()
	targetResources = getTargetResources(appIds, xproj)
	for id in appIds:
		if not checkResourcesMatch(appIds[0], xmlResources):
			return False
	return True

def getTargetResources(resourceIds, xproj):
	resources = []
	for rid in resourceIds:
		pattern = rid + "\/\* Resources \*\/.*?files \-= \(\n"
		split = re.split(pattern, xproj)
		trailing = split[1]
		pattern = "\/\* Resources \*\/"
		split = re.split(pattern, trailing)

		pattern = "(?:A-Z0-9)+ \/\* ([a-zA-Z0-9]+.[a-z]) + in Resources)"

def getResourceIds(xproj, apps):
	"""docstring for getResourceIds"""
	appIds = []
	
	pattern = "(?<=Begin PBXNativeTarget section)"
	for app in apps:
		pattern = pattern + "(?:.*? \/\* " + app +" \*\/.*?)([A-Z0-9]+)(?: \/\* Resources \*\/)"
		print pattern
		m = search(pattern, xproj, re.DOTALL)
		appIds.append(m.group(1))
	return appIds

def uniq(input):
 	output = []
  	for x in input:
    		if x not in output:
     			output.append(x)
  	return output

def checkResourcesMatch(appId, xmlResources):
	"""If image resources in storyboard don't have a 1:1 matching with
	target resources, return false"""
	targets = getTargets(appId)

	for target in targets:
		if xmlResources.count() == 0:
			return False
	return True

def getXMLResources():
	resources = []
	return resources

def getTargets(appId):
	targets = []
	return targets
	
def subInFile(pattern, repl, projectFilePath):
	print "subInFile"
	tempHandle, tempPath = mkstemp()
	tempFile = open(tempPath, 'w')
	oldFile = open(projectFilePath)

	for line in oldFile:
		tempFile.write(sub(pattern, repl, line))

	tempFile.close()
	close(tempHandle)
	oldFile.close()
	remove(projectFilePath)
	move (tempPath, projectFilePath)

#print getResourceIds()

def commitWithSwappedCert(commitMessage, projectFilePath):
	subInFile("iPhone Developer", "iPhone Distribution", projectFilePath)
	
	print "Diff after fix: "
	call["svn commit -m \"commitMessage\""]

	subInFile("iPhone Distribution", "iPhone Developer", projectFilePath)

