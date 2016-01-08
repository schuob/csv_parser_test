import csv
import re

## enter the csv that you plan to work with e.g something.csv
csvFile = '<REPLACE_WITH_CSV_FILE_WITH_EXT>'
## this opens the file and place it into a workable variable
csvData = csv.reader(open(csvFile,'rU'))
## Name of the xml/mrss file you want to create e.g something.mrss
## If you need to create one MRSS file per item move all the code between ## START and ## END and add above the
## xmlData.write( "\t\t" + '<item>' + "\n") line.

## MRSS Opening START

xmlFile = '<REPLACE_WITH_NAME_OF_MRSS_WITH_EXT>' ## Filename need to be unique if creating 1 MRSS per file // Use the guid or something unique for this.
##xmlFile = guid + '.mrss'
## Creates that file
xmlData = open(xmlFile, 'w')
## writing start of mrss file
xmlData.write('<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:lvpcm="http://www.limelightnetworks.com/" xmlns:dcterms="http://purl.org/dc/terms/">' + "\n")
xmlData.write("\t" + '<channel>' + "\n")
xmlData.write("\t\t" + '<title></title>' + "\n") 
##xmlData.write("\t\t" + '<title><![CDATA[' + channel + ']]></title>' + "\n") 
xmlData.write("\t\t" + '<link></link>' + "\n")
xmlData.write("\t\t" + '<description></description>' + "\n")
## MRSS Opening END

rowNum = 0
for row in csvData:
	if rowNum == 0:
		## takes the 1st row as it is assumed that this is the header row
		header = row
	else:
		if rowNum  == 1:	
			data = row
			## variables to be used; update the fields as needed
			## this requires that you know which column maps over to which field e.g title, keywords or custom properties.
			## data[index] - e.g [12345,'Some title some where','some-file-name.avi'] - [index 0, index 1, index 2]
			
			mediaurl = data[index]		# The column that holding the URL for the media item
			mediatitle = data[index]	# The column that holding the URL for the media item
			mediadesc = data[index]		# The column that holds the description  
			tempguid = data[index]		# ONLY uses this if you have a FILENAME and NO URL uncomment the extension stripper
			keywords = data[index]		# This is assuming that the keyword is in one box separated by commas
			category = data[index]		# Category
			
			## Custom Properties add as many as you need
			
			customprop1 = data[index]	# Custom properties
			customprop2 = data[index]	# Custom properies
			
			## Use below to build the GUID from a URL, uncomment any function to strip different parts of the URL
			## The first line will strip off the ?queryString from the URL
			## The second line will strip off the URL and leaving only the filename with extension
			## The third line will strip off the extension and leave only the filename
			## So if you need to strip out only the URL uncomment second & third line
			
			#tempguid = re.sub('(?:\?)[^&]*', '', mediaurl)		# Strip querystring
			#tempguid = re.sub('^((http[s]?|ftp):\/)?\/?([^:\/\s]+)(:([^\/]*))?((\/\w+)*\/)', '', tempguid)		# Strip url leaving filename
			#tempguid = re.sub('(\.[^.]*)$', '', tempguid)		# Strip file extension
			
			## sets the GUID after all the stripping - may need to update this part to convert spaces into "_"

			guid = tempguid.replace(" ","_")	# Replaces any spaces with "_"

			## Sample ITEM Node from 
			##<item>
			##	<title></title>
			##	<link></link>
			##	<description></description>
			##	<guid>filename</guid>
			##	<media:content url="">
			##		<media:title></media:title>
			##	    <media:description></media:description>
			##	    <media:thumbnail url="" />
			##	    <media:keywords></media:keywords>
			##	    <media:category></media:category>
			##	</media:content>
			##	<lvpcm:customProperties>
			##		<lvpcm:customProperty type="Property 1 Name" value="Property 1 Value"/>
			##		<lvpcm:customProperty type="Property 2 Name" value="Property 2 Value"/>
			##	</lvpcm:customProperties>
			##</item>
		
		
			## INSERT MRSS Opening here for 1 mrss per item
		
		
			## Writing each row into an item node
			## If you need to put description, keyword or keyword update the fields below to use <![CDATA[ + variable + ]]>
			## basically ensure that it looks the same as the mediatitle field
			## To add more custom properties copy the customprop1 line and update the variable
			xmlData.write( "\t\t" + '<item>' + "\n")
			xmlData.write( "\t\t\t" + '<title></title>' + "\n")
			xmlData.write( "\t\t\t" + '<link></link>' + "\n")
			xmlData.write( "\t\t\t" + '<description></description>' + "\n")
			xmlData.write( "\t\t\t" + '<guid>' + guid + '</guid>' + "\n")
			
			## URL
			## ---------
			## If using MRSS to update metadata use current line, if using the MRSS to also import media with a URL comment out the
			## bottom line and uncomment out the line with mediaurl.replace()
            xmlData.write( "\t\t\t" + '<media:content url="">' + "\n")
			##xmlData.write( "\t\t\t" + '<media:content url="' + mediaurl.replace(" ","%20") + '">' + "\n")
			xmlData.write( "\t\t\t\t" + '<media:title><![CDATA[' + mediatitle + ']]></media:title>' + "\n")
			xmlData.write( "\t\t\t\t" + '<media:description></media:description>' + "\n")
			xmlData.write( "\t\t\t\t" + '<media:thumbnail url="" />' + "\n")
			xmlData.write( "\t\t\t\t" + '<media:keywords></media:keywords>' + "\n")
			xmlData.write( "\t\t\t\t" + '<media:category></media:category>' + "\n")
			xmlData.write( "\t\t\t" + '</media:content>' + "\n")
			xmlData.write( "\t\t" + '<lvpcm:customProperties>' + "\n")
			xmlData.write( "\t\t\t" + '<lvpcm:customProperty type="customPropertyName" value="' + customprop1 + '"/>' + "\n")
			xmlData.write( "\t\t" + '</lvpcm:customProperties>' + "\n")
			xmlData.write( "\t\t" + '</item>' + "\n")
			
			## INSERT MRSS Closing here for 1 mrss per item
			
	rowNum +=1
		
## If you need to create one MRSS file per item move all the code between ## START and ## END and add above the
## xmlData.write( "\t\t" + '</item>' + "\n") line.

## MRSS Closing START
xmlData.write("\t" + '</channel>' + "\n")
xmlData.write('</rss>')
xmlData.close()
## MRSS Closing END