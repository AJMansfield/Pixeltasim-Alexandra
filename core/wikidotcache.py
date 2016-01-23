from time import sleep
import threading
import datetime
from whiffle import wikidotapi
import pickle
import __builtin__
import twitter

def cache_refresh(): #calls itself automatically once called for the first time
	twitter_api = twitter.Api(consumer_key='',consumer_secret='', access_token_key='2288772386-', access_token_secret='')
	threading.Timer(3600, cache_refresh).start (); 
	api = wikidotapi.connection()
	#overwrite update
	overwritecache = {}
	api.Site = "05command"
	pages = api.refresh_pages() #refresh page list provided by the API, is only a list of strings
	source = api.server.pages.get_one({"site":api.Site,"page":"alexandra-rewrite"})
	content = source["content"]
	fs = content.split("-----")
	rewritelist = fs[1]
	invrewrite = rewritelist.split("\n")
	for rewrite in invrewrite:
		parts = rewrite.split("||")
		val = 0
		writelist = []
		first = ""
		author = ""
		for part in parts:
			val+=1
			if val ==2:
				#page
				first = part 
			if val ==3:
				#author
				author = part 
		if first != "Page":
			overwritecache[first.lower()] = author 
	print "Rewrite update complete."
	source = api.server.pages.get_one({"site":api.Site,"page":"alexandra-glossary"})
	content = source["content"]
	fs = content.split("-----")
	glossarylist = fs[1]
	invglossary = glossarylist.split("\n")
	localglossary = {}
	for terms in invglossary:
		parts = terms.split("||")
		val = 0
		writelist = []
		first = ""
		definition = ""
		for part in parts:
			val+=1
			if val ==2:
				#word
				first = part 
			if val ==3:
				#def
				definition = part 
		if first != "Word":
			localglossary[first] = definition 
	__builtin__.termlist = localglossary
	print "Glossary update complete."
	#file reading
	localauthorlist = {}
	localtitlelist = {}
	localtaglist = {}
	localratinglist = {}
	scpcache = {}
	api.Site = "scp-wiki"
	pages = api.refresh_pages()
	__builtin__.scppages = api.refresh_pages()
	try:
		with open("cache.cache","rb") as f:
			scpcache = pickle.load(f)
	except EOFError:
		pass
	if len(scpcache) != 0:
		print "Reading cache"
		__builtin__.scppagecache = scpcache
		for page in pages:
			for item in scpcache:
				try:
					localauthorlist[page] = item[page]["created_by"]
					if localauthorlist[page] == None:
						localauthorlist[page] = ""
					localtitlelist[page] = item[page]["title"]
					localtaglist[page] = item[page]["tags"]
					if localtaglist[page] == None:
						localtaglist[page] = ""
					localratinglist[page] = item[page]["rating"]
					if overwritecache[page.lower()]:
						localauthorlist[page] = localauthorlist[page]+":rewrite:"+overwritecache[page.lower()]
						if ":override:" in localauthorlist[page]:
							bothauths = localauthorlist[page].split(":rewrite:")
							newauth = bothauths[1]
							localauthorlist[page] = newauth[10:]
						else if ":coauthor:" in localauthorlist[page]:
							bothauths = localauthorlist[page].split(":rewrite:")
							newauth = bothauths[1]
							localauthorlist[page] = newauth[10:]
				except KeyError:
				 pass
	__builtin__.authorlist = localauthorlist
	__builtin__.titlelist = localtitlelist
	__builtin__.taglist = localtaglist
	__builtin__.ratinglist = localratinglist
	#scp titles 
	print "Updating SCP titles"
	localscptitles = {}
	api.site = "scp-wiki"
	pages = api.refresh_pages()
	page_one_blank = api.server.pages.get_one({"site":api.Site,"page":"scp-series"})
	page_one = page_one_blank["content"]
	page_two_blank = api.server.pages.get_one({"site":api.Site,"page":"scp-series-2"})
	page_two = page_two_blank["content"]
	page_three_blank = api.server.pages.get_one({"site":api.Site,"page":"scp-series-3"})
	page_three = page_three_blank["content"]
	page_j_blank = api.server.pages.get_one({"site":api.Site,"page":"joke-scps"})
	page_j = page_j_blank["content"]
	page_arc_b = api.server.pages.get_one({"site":api.Site,"page":"archived-scps"})
	page_arc = page_arc_b["content"]
	page_decon_b = api.server.pages.get_one({"site":api.Site,"page":"decommissioned-scps"})
	page_decon = page_decon_b["content"]
	page_ex_b = api.server.pages.get_one({"site":api.Site,"page":"scp-ex"})
	page_ex = page_ex_b["content"]
	
	page_one_split = page_one.split("\n")
	for part in page_one_split:
		if part.startswith("* [[[SCP-"):
			num = part[9:12]
			title = part[18:].encode("ascii","ignore")
			page = "scp-"+num  
			if "]" not in num:
				localscptitles[page.lower()] = title
	page_two_split = page_two.split("\n")
	for part in page_two_split:
		if part.startswith("* [[[SCP-"):
			num = part[9:13]
			title = part[19:].encode("ascii","ignore")
			page = "scp-"+num  
			if "]" not in num:
				localscptitles[page.lower()] = title
	page_three_split = page_three.split("\n")
	for part in page_three_split:
		if part.startswith("* [[[SCP-"):
			num = part[9:13]
			title = part[19:].encode("ascii","ignore")
			page = "scp-"+num  
			if "]" not in num:
				localscptitles[page.lower()] = title
	page_j_split = page_j.split("\n")
	for part in page_j_split:
		if part.startswith("* [[[SCP-"):
			segments = part.split(" - ")
			first = segments[0]
			end=first.index("]")
			num = part[9:end]
			if "|" in first:
				secend = num.index("|")
				num = num[:secend]
			title = segments[1].encode("ascii","ignore")
			page = "scp-"+num
			localscptitles[page.lower()] = title
	page_arc_split = page_arc.split("\n")
	for part in page_arc_split:
		if part.startswith("* [[[SCP-"):
			segments = part.split(" - ")
			first = segments[0]
			end=first.index("]")
			num = part[9:end]
			title = segments[1].encode("ascii","ignore")
			page = "scp-"+num
			localscptitles[page.lower()] = title
	page_decon_split = page_decon.split("\n")
	for part in page_decon_split:
		if part.startswith("* [[[SCP-"):
			segments = part.split(" - ")
			first = segments[0]
			end=first.index("]")
			num = part[9:end]
			title = segments[1].encode("ascii","ignore")
			page = "decomm:scp-"+num
			localscptitles[page.lower()] = title
	page_ex_split = page_ex.split("\n")
	for part in page_ex_split:
		if part.startswith("* [[[SCP-"):
			segments = part.split(" - ")
			first = segments[0]
			end=first.index("]")
			num = part[9:end]
			title = segments[1].encode("ascii","ignore")
			page = "scp-"+num
			localscptitles[page.lower()] = title
	__builtin__.scptitles = localscptitles
	#WL
	__builtin__.callsmade = 0
	api.Site = "wanderers-library"
	__builtin__.wlpages = api.refresh_pages()
	pages = api.refresh_pages()
	__builtin__.totalpagescurcache = len(pages)
	print "Refreshing WL cache"
	newpagecache = [] #the newpagecache is so that while it is updating you can still use the old one
	for page in pages:
		newpagecache.append(api.server.pages.get_meta({"site": api.Site, "pages": [page]}))
		time.sleep(0.4) #this keeps the api calls within an acceptable threshold
		__builtin__.callsmade+=1
	print "Cache refreshed!"
	__builtin__.pagecache= newpagecache #__builtin__ means that pagecache is global and can be used by plugins
	ts = time.time()
	__builtin__.lastcacherefresh = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	#SCP
	#SCP
	__builtin__.callsmade = 0
	api.Site = "scp-wiki"
	pages = api.refresh_pages()
	__builtin__.totalpagescurcache = len(pages)
	print "Refreshing SCP cache"
	__builtin__.totalpagescurcache = len(pages)
	newpagecache = [] #the newpagecache is so that while it is updating you can still use the old one
	localauthorlist = {}
	localtitlelist = {}
	localtaglist = {}
	localratinglist = {}
	__builtin__.oldratinglist = ratinglist
	for page in pages:
		x = api.server.pages.get_meta({"site": api.Site, "pages": [page]})
		cache = {}
		cache[page] = x[page]
		try:
			localauthorlist[page] = cache[page]["created_by"]
			if localauthorlist[page] == None:
				localauthorlist[page] = ""
			localtitlelist[page] = cache[page]["title"]
			localtaglist[page] = cache[page]["tags"]
			if localtaglist[page] == None:
				localtaglist[page] = ""
			localratinglist[page] = cache[page]["rating"]
			if overwritecache[page.lower()]:
				localauthorlist[page] = localauthorlist[page]+":rewrite:"+overwritecache[page.lower()]
				if ":override:" in localauthorlist[page]:
					bothauths = localauthorlist[page].split(":rewrite:")
					newauth = bothauths[1]
					localauthorlist[page] = newauth[10:]
				else if ":coauthor:" in localauthorlist[page]:
					bothauths = localauthorlist[page].split(":rewrite:")
					newauth = bothauths[1]
					localauthorlist[page] = newauth[10:]
		except KeyError:
			pass 
		newpagecache.append(x)
		time.sleep(0.3) #this keeps the api calls within an acceptable threshold
		__builtin__.callsmade +=1 
	__builtin__.authorlist = localauthorlist
	__builtin__.titlelist = localtitlelist
	__builtin__.taglist = localtaglist
	__builtin__.ratinglist = localratinglist
	
	print "Cache refreshed!"
	statuses = twitter_api.GetUserTimeline("scpwiki")
	final = ""
	for page in pages:
		done = 0
		for s in statuses:
			if titlelist[page].lower() in s.text.lower():
				done = 1
		if done ==0:
			try:
				if oldratinglist[page] < 20:
					if ratinglist[page] >=20:
						try:
							if scptitles[page]:
								final = scptitles[page]+"- "+titlelist[page]+" by "+authorlist[page]+". http://scp-wiki.net/"+page
								status = twitter_api.PostUpdate(final)
						except KeyError:
							final = "[ACCESS GRANTED] "+titlelist[page]+" by "+authorlist[page]+". http://scp-wiki.net/"+page
							status = twitter_api.PostUpdate(final)
			except KeyError:
				if ratinglist[page] >= 20:
					try:
						if scptitles[page]:
							final = scptitles[page]+"- "+titlelist[page]+" by "+authorlist[page]+". http://scp-wiki.net/"+page
							status = twitter_api.PostUpdate(final)
					except KeyError:
						final ="[ACCESS GRANTED] "+titlelist[page]+" by "+authorlist[page]+". http://scp-wiki.net/"+page
						status = twitter_api.PostUpdate(final)
	print "Tweets sent"
	__builtin__.scppagecache= newpagecache #__builtin__ means that pagecache is global and can be used by plugins

	with open("cache.cache","wb") as f:
		pickle.dump(newpagecache,f)

	#end	
	ts = time.time()
	lastcacherefresh = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def ban_refresh():
	threading.Timer(900, ban_refresh).start (); 
	api = wikidotapi.connection()
	#overwrite update
	localbancache = {}
	__builtin__.bancache = {}
	api.Site = "05command"
	pages = api.refresh_pages() #refresh page list provided by the API, is only a list of strings
	source = api.server.pages.get_one({"site":api.Site,"page":"alexandra-s-ban-page"})
	content = source["content"]
	fs = content.split("-----")
	banlist = fs[1]
	invbans = banlist.split("\n")
	for ban in invbans:
		parts = ban.split("||")
		val = 0
		_list = []
		nick = ""
		author = ""
		for part in parts:
			val+=1
			if val ==2:
				#Nick
				nick = part 
				_list.append(nick)
			if val ==3:
				#IP
				_list.append(part)
			if val ==4:
				#unban date
				if part != "Ban Status":
					if part != "Perma":
						date = datetime.datetime.strptime(part,"%m/%d/%Y")
						today =datetime.datetime.today()
						if date.date() <= today.date():
							part = "Unbanned"
						_list.append(part)
					else:
						_list.append(part)
			if val ==5:
				#Reason
				_list.append(part)
		if nick != "Nick(s)":
			localbancache[nick] = _list
	__builtin__.bancache = localbancache
	print "Ban update complete."
	__builtin__.hugs = 0
	ts = time.time()
	__builtin__.lastbanrefresh = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	

	
