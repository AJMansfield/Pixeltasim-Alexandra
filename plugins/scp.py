from whiffle import wikidotapi
from util import hook
import re
import time,threading

@hook.command
def unused(inp):
	api = wikidotapi.connection() 
	api.Site = "scp-wiki"
	pages = api.refresh_pages()
	scps = []
	for page in pages:
		try:
			if "scp" in taglist[page]:
				val = page 
				scps.append(val)
		except (KeyError,IndexError):
			pass
	for i in range(001,2999):
		x = str(i)
		if i<100:
			x="0"+str(i)
		if i<10:
			x="00"+str(i)
		if x in val:
			continue
		else:
			if api.page_exists("scp-"+x):
				continue 
			else:
				return "The first unused page found is SCP-"+x+" - http://www.scp-wiki.net/scp-"+x

def makeauthorstring(author):
	author = author or "unknown"
	if ":rewrite:" in author:
		bothauths = authorlist[page].split(":rewrite:")
		orgauth = bothauths[0]
		newauth = bothauths[1]
		return "Originally written by "+orgauth +", rewritten by "+newauth
	else if ":coauthor:" in author:
		bothauths = authorlist[page].split(":coauthor:")
		orgauth = bothauths[0]
		newauth = bothauths[1]
		return "Written by "+orgauth+" and "+newauth
	else:
		return "Written by "+author
	
@hook.regex("scp-")
def scpregex(match):
	if ' ' not in match.string:
		if match.string.lower().startswith("scp-") or match.string.lower().startswith("!scp-"):
			page = re.sub("[!,_,?,,,',.]",'',match.string.lower())
			if "--" in page:
				count = page.index("-")
				page = page[:count]+page[count+1:]
			try:
				rating = ratinglist[page]
				ratesign = ""
				if rating >= 0:
					ratesign = "+" #adds + or minus sign in front of rating
				ratestring = "Rating:"+ratesign+str(rating)+"" 
				author = authorlist[page]
				authorstring = makeauthorstring(author)
				title = titlelist[page]
				scptitle = scptitles[page]
				sepstring = ", "
				link = "http://scp-wiki.net/"+page.lower() 
				return ""+title+" ("+scptitle+sepstring+authorstring+sepstring+ratestring+") - "+link 
<<<<<<< HEAD
			except KeyError as e:
				api = wikidotapi.connection() 
				api.Site = "scp-wiki"
				if api.page_exists(page):
					rating = api.get_page_item(page,"rating")
					ratesign = ""
					if rating >= 0:
						ratesign = "+" #adds + or minus sign in front of rating
					ratestring = "Rating:"+ratesign+str(rating)+"" 
					author = api.get_page_item(page,"created_by")
					if author == "":
						author = "unknown"
					authorstring = "Written by "+author
					title = api.get_page_item(page,"title")
					sepstring = ", "
					link = "http://scp-wiki.net/"+page.lower() 
					return ""+title+" ("+ratestring+sepstring+authorstring+") - "+link 
				else:
					return "Page does not exist, but you can create it here: " + "http://scp-wiki.net/"+page
=======
			except KeyError:
				api = wikidotapi.connection() 
				api.Site = "scp-wiki"
				rating = api.get_page_item(page,"rating")
				ratesign = ""
				if rating >= 0:
					ratesign = "+" #adds + or minus sign in front of rating
				ratestring = "Rating:"+ratesign+str(rating)+"" 
				author = api.get_page_item(page,"created_by")
				if author == "":
					author = "unknown"
				authorstring = "Written by "+author
				title = api.get_page_item(page,"title")
				sepstring = ", "
				link = "http://scp-wiki.net/"+page.lower() 
				return ""+title+" ("+ratestring+sepstring+authorstring+") - "+link 
			#return "Page does not exist, but you can create it here: " + "http://scp-wiki.net/"+page
>>>>>>> origin/master
	else:
		matches = match.string.lower().split()
		scp_match = ""
		for part in matches:
			if part.startswith("!scp-"):
				page = re.sub("[!,_,?,,,',.]",'',part.lower())
				try:
					rating = ratinglist[page]
					ratesign = ""
					if rating >= 0:
						ratesign = "+" #adds + or minus sign in front of rating
					ratestring = "Rating:"+ratesign+str(rating)+"" 
					author = authorlist[page]
					authorstring = makeauthorstring(author)
					title = titlelist[page]
					scptitle = scptitles[page]
					sepstring = ", "
					link = "http://scp-wiki.net/"+page.lower() 
					return ""+title+" ("+scptitle+sepstring+authorstring+sepstring+ratestring+") - "+link 
				except KeyError:
					api = wikidotapi.connection() 
					api.Site = "scp-wiki"
<<<<<<< HEAD
					if api.page_exists(page):
						rating = api.get_page_item(page,"rating")
						ratesign = ""
						if rating >= 0:
							ratesign = "+" #adds + or minus sign in front of rating
						ratestring = "Rating:"+ratesign+str(rating)+"" 
						author = api.get_page_item(page,"created_by")
						authorstring = makeauthorstring(author)
						title = api.get_page_item(page,"title")
						sepstring = ", "
						link = "http://scp-wiki.net/"+page.lower() 
						return ""+title+" ("+ratestring+sepstring+authorstring+") - "+link
					else:
						return "Page does not exist, but you can create it here: " + "http://scp-wiki.net/"+page
=======
					rating = api.get_page_item(page,"rating")
					ratesign = ""
					if rating >= 0:
						ratesign = "+" #adds + or minus sign in front of rating
					ratestring = "Rating:"+ratesign+str(rating)+"" 
					author = api.get_page_item(page,"created_by")
					authorstring = makeauthorstring(author)
					title = api.get_page_item(page,"title")
					sepstring = ", "
					link = "http://scp-wiki.net/"+page.lower() 
					return ""+title+" ("+ratestring+sepstring+authorstring+") - "+link 
				#return "Page does not exist, but you can create it here: " + "http://scp-wiki.net/"+page
>>>>>>> origin/master
@hook.command
def untagged(inp):
	api = wikidotapi.connection() 
	api.Site = "scp-wiki"
	pages = api.refresh_pages() 
	final = "The following pages are untagged: "
	first = 1
	for page in pages:
		try:
			if taglist[page]:
				continue
			else:
				if page.startswith("forum:") or page.startswith("system") or page.startswith("nav") or page.startswith("css") or page.startswith("admin")or page.startswith("component")or page.startswith("search"):
					continue
				else:
					first = 0 
					final +=" - "+ page
		except KeyError:
			first = 0 
			final += page+" - "
			continue
	if first == 1:
		final = "No untagged pages found!"
	return final
	
@hook.regex("scp-wiki.net/")
def linkregex(inp):
	substrings = inp.string.split()
	for ss in substrings:
		if "http://www.scp-wiki.net/"in ss or "http://scp-wiki.net/" in ss or "http://www.wikidot.scp-wiki.net/" in ss or "www.scp-wiki.net/" in ss:
			page = ss[24:]
			if page.startswith("com/"):
				page = ss[29:]
			rating = ratinglist[page]
			ratesign = ""
			if rating >= 0:
				ratesign = "+" 
			ratestring = "Rating:"+ratesign+str(rating)+"" 
			author = authorlist[page]
			authorstring = "Written by "+author
			if ":rewrite:" in author:
					bothauths = authorlist[page].split(":rewrite:")
					orgauth = bothauths[0]
					newauth = bothauths[1]
					authorstring = "Originally written by "+orgauth +", rewritten by "+newauth
			if author == "":
				author = "unknown"
			title = titlelist[page]
			sepstring = ", "
			if "scp" in taglist[page]:
				scptitle = scptitles[page]
				return ""+title+" ("+scptitle+sepstring+authorstring+sepstring+ratestring+") - http://scp-wiki.net/"+page.lower() 
			return ""+title+" ("+ratestring+sepstring+authorstring+") - http://scp-wiki.net/"+page.lower() 
				
@hook.regex("!chat-guide")
def chatguide(func):
	return "SCP Chat Guide - http://www.scp-wiki.net/chat-guide"
