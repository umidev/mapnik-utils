#!/usr/bin/env python

"""
mapniktrac.py - http://inamidst.com/phenny/
"""

import re
import urllib

# need to build up at runtime...
keywords = ['BoostCompatibility','BuildingSymbolizer','CamelCase','CentOS/RHEL','Compositing','DebuggingMapnik','DemoGallery','DeveloperTodo','ElseFilter','ExampleCode','ExampleCodePythonPostGIS','Filter','GettingStarted','InstallationTroubleshooting','IntegrateWithWxPython','InterMapTxt','InterTrac','InterWiki','IntroductionToGIS','LabelingSupport','LinePatternSymbolizer','LineSymbolizer','LinuxInstallation','MacInstallation','MacInstallation/Optional','MacInstallationPorts','MacInstallationSource','MacPostGIS_Setup','MacPythonUpgradeIssues','ManagingLargeXmlFiles','MapDesign','MapnikDependencies','MapnikInstallation','MapnikInstallationSvn','MapnikOverview','MapnikRenderers','MapnikViewer','MarkersSymbolizer','MaxScaleDenominator','MinScaleDenominator','ModServer','Nik2Img','OgcServer','OgcServerSvn','OpenSuse','OutputFormats','PluginArchitecture','PointSymbolizer','PolygonPatternSymbolizer','PolygonSymbolizer','PostGIS','RasterSymbolizer','RecentChanges','SandBox','ScaleAndPpi','ShieldSymbolizer','ShieldSymbolizerTests','StableMergeQueue','SymbologySupport','TextSymbolizer','TitleIndex','TracAccessibility','TracAdmin','TracBackup','TracBrowser','TracCgi','TracChangeset','TracEnvironment','TracFastCgi','TracGuide','TracImport','TracIni','TracInstall','TracInterfaceCustomization','TracLinks','TracLogging','TracModPython','TracNotification','TracPermissions','TracPlugins','TracQuery','TracReports','TracRevisionLog','TracRoadmap','TracRss','TracSearch','TracStandalone','TracSupport','TracSyntaxColoring','TracTickets','TracTicketsCustomFields','TracTimeline','TracUnicode','TracUpgrade','TracWiki','UbuntuInstallation','UbuntuInstallationOld','WikiDeletePage','WikiFormatting','WikiHtml','WikiMacros','WikiNewPage','WikiPageNames','WikiProcessors','WikiRestructuredText','WikiRestructuredTextLinks','WikiStart','WindowsInstallation','XMLConfigReference','XMLGettingStarted','XmlFormatDiscussion']

def wiki_pages(phenny,input): 
    try:
        phenny.say("http://trac.mapnik.org/wiki/%s" % (input.group(2).lstrip('.') ))
    except Exception, E:
        phenny.say("(%s)" % E)
    
wiki_pages.rule = r'''(?i).*(\s|^)+(%s)(\s|\.|\,|\?|$)''' % '|.'.join([ re.escape(entry) for entry in keywords])

def tickets(phenny,input):
    ticket = 0
    data = urllib.urlopen("http://trac.mapnik.org/ticket/%s?format=csv" % input.group(3)).read()
    try:
        ticket = data.split("\n")[1].split(",")[1]
        phenny.say("Ticket #%s: %s, http://trac.mapnik.org/ticket/%s" % (input.group(3), ticket, input.group(3)))
    except Exception, E:
        phenny.say("Ticket #%s: no such ticket. (%s)" % (input.group(3), E))
    
tickets.rule = r'''(?i).*(\s|^)+(#|t|ticket|Ticket|Ticket |ticket |Bug |Task )(\d+)(\s|\.|\,|\?|$)'''

def changesets(phenny,input):
     url = "http://trac.mapnik.org/changeset/%s" % input.group(3)
     data = urllib.urlopen(url).read()
     m = re.search(r'''<dd class="time">(.*?)''', data)
     time = input.group(1)
     m = re.search(r'''<dd class="author">(.*?)</dd>''', data)
     author = input.group(1)
     #c = re.compile(r'''<dd class="message" id="searchable">.*?<p>(.*?)</p>''', re.DOTALL)
     c = re.compile(r'''<dd class="message searchable">.*?<p>(.*?)</p>''', re.DOTALL)
     line = re.sub(r'''<[^>]*>''', "", c.search(data).group(1)).replace("\n", "")
     phenny.say("%s, at %s, by %s: %s" % (url, time, author, line[0:200]))
     
changesets.rule = r'''(?i).*(\s|^)+(r|changeset |commit )(\d+)(\s|\.|\,|\?|$)'''

def milestones(phenny,input):
     url = "http://trac.mapnik.org/query?status=new&status=assigned&status=reopened&format=csv&milestone=%s&order=priority" % urllib.quote(input.group(3))
     data = urllib.urlopen(url).read()
     tickets = []
     for i in data.split("\n"):
          line = i.split(",")
          if (line[0] != "id" and len(line) > 1):
                tix = '#%s %s' % (line[0],line[1])
                tickets.append(tix)
     reply = "%s open tickets in Milestone %s: %s" % (len(tickets), input.group(3), ", ".join(tickets))
     if tickets:
          if len(reply) > 400:
                reply = reply[0:400]+"..."
          phenny.say(reply)
          
          link = '%s' % url.replace('&format=csv','')
          phenny.say(link)
          roadmap = 'http://trac.mapnik.org/milestone/%s' % input.group(3)

          phenny.say('Milestone Roadmap: ' + roadmap)
     else:
          phenny.say('No Milestone for that release number')
     
milestones.rule = r'''(?i).*(\s|^)+(roadmap |milestone )(.*)(\s|\.|\,|\?|$)'''