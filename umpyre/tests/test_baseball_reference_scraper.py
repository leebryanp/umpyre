from umpyre.data.scraper import BaseballReferenceScraper

# url = "http://www.baseball-reference.com/leagues/MLB/2015-misc.shtml"
url = "http://www.baseball-reference.com/players/a/aaronha01.shtml"
# url = "http://www.baseball-reference.com/teams/"
# url = "http://www.baseball-reference.com/teams/OAK/2014-schedule-scores.shtml"
# url = "http://www.baseball-reference.com/teams/TOR/1979.shtml"

scraper = BaseballReferenceScraper()
data = scraper.data_from_url(url)
print data.keys()
for k, v in data.items():
	print '-'*40
	print 'Dataset: %s' % k
	print '-'*40
	print v
