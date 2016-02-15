from urllib2 import urlopen, URLError
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def is_numeric(x):

	if x == '':
		return True  # cast empty values as this as a nan
	
	if isinstance(x, int) or isinstance(x, float):
		return True
	else:
		try:
			float(x.replace(',','').replace('$',''))
			return True
		except:
			return False
	
def as_numeric(x):

	if x == '':
		return np.NaN 
	try:
		return int(x)
	except:
		return float(x)
	
def to_numeric(x):
	if is_numeric(x):
		if isinstance(x, unicode) or isinstance(x, str):
			return as_numeric(x.replace(',','').replace('$',''))
		else:
			return x
	else:
		if isinstance(x, str):
			x.replace('\n','').replace('\t','')
		return x

def format_values(x):
	if '%' in x:  # special case: values returned as percentages
		return .01 * to_numeric(x.replace('%',''))
	elif ':' in x:  # special case: times
		hour, minutes = x.split(':')
		hour = to_numeric(hour)
		minutes = float(to_numeric(minutes))/60
		return hour + minutes
	else:
		return to_numeric(x)

def format_columns(df):
	for col in df.columns:
		df[col] = df[col].apply(format_values)
	return df


def parse_entry(entry):
	entry_contents = entry.contents
	content_str = ''
	if entry_contents is not None:
		for c in entry_contents:
			if c.name is None or c.name == 'a':
				content_str += c.string.strip()
	return content_str

def parse_rows(table, valid_row_criterion):
	rows = table.find("tbody").find_all(valid_row_criterion)
	data = []
	for row in rows:
		entries = row.find_all("td")
		entry_data = [parse_entry(entry) for entry in entries]            
		data.append(entry_data)
			
	return data

def make_soup(url, parser='lxml'):
	try:
		resp = urlopen(url)
	except URLError as e:
		print 'An error occured fetching %s \n %s' % (url, e.reason)   
		return None
	return BeautifulSoup(resp.read(),parser)


def parse_tables_from_url(url, valid_table_criterion, parser='lxml'):
	
	soup = make_soup(url, parser)

	# get tables
	try:
		# deterimine if tables have useful data
		tables = soup.find_all(valid_table_criterion)
		return tables
	except AttributeError as e:
		print 'No tables found, exiting'
		print e
		return None


def parse_columns(table, verbose=False):
	headers = table.find("thead").find_all("th")
	column_names = []
	for header in headers:
		if header.string is None: 
			base_column_name = ''.join([v.string.strip() for v in header.contents])
		else: 
			base_column_name = header.string.strip()
		if base_column_name in column_names:
			i = 1
			column_name = base_column_name + "_%s" % str(i)
			while column_name in column_names:
				i += 1
				column_name = base_column_name + "_%s" % str(i)
			if verbose: 
				if base_column_name == "":
					print "Empty header relabeled as %s" % column_name
				else:
					print "Header %s relabeled as %s" % (base_column_name, column_name)
		else:
			column_name = base_column_name
		column_names.append(column_name)
	return column_names

class BaseballReferenceScraper(object):
	def __init__(self, parser='lxml'):
		self.parser = parser

	def is_valid_table(self, tag):
		# if "class" not in tag:
		if not tag.has_key("class"):  # strange bug: deprecated behavior works, but not standard
			return False
		return tag.name == "table" and "stats_table" in tag["class"] and "sortable" in tag["class"]

	def is_valid_row(self, tag):
		if not tag.name == "tr": 
			return False
		if "class" not in tag: 
			return True  # permissive
		return "league_average_table" not in tag["class"] and "stat_total" not in tag["class"]

	def parse_tables_from_url(self, url):
		return parse_tables_from_url(url, self.is_valid_table, parser=self.parser)

	def parse_rows(self, table):
		return parse_rows(table, self.is_valid_row)

	def data_from_url(self, url, table_ids=None):
		
		# get tables
		tables = self.parse_tables_from_url(url)
		# compile dataset {key, DataFrame} pairs

		data = {}
		for idx, table in enumerate(tables):

			# key collision, so don't overwrite	data
			# include info about position on page for 
			# back-reference
			table_id = table['id']
			if table_id in data:
				table_id += ' (table %d)' % (idx+1)
			
			# skip unspecified tables
			if table_ids is not None and table_id not in table_ids:  # skip non-requested tables
				continue

			columns = parse_columns(table)
			rows = self.parse_rows(table)
			
			# detect if there's a hierarchical organization,
			# use last column names for data column headers
			num_xtra_columns = len(columns) - len(rows[0])
			if num_xtra_columns > 0:
				print 'WARNING: extra columns for table `%s`:' % table_id
				print ','.join(columns[:num_xtra_columns])
				columns = columns[num_xtra_columns:]
			
			# create pandas dataframe from data
			df = pd.DataFrame(rows, columns=columns)
			
			# if more than half of columns in a row are bad, we ignore
			df.dropna(thresh=np.floor(len(df.columns)/2), inplace=True)
			
			# make columns useable and store in dataset
			data[table_id] = format_columns(df)

		return data
