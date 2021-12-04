# Imports
from bs4 import BeautifulSoup
import pandas
from urllib.request import Request, urlopen		# For submitting HTTP requests

baseURL = r'http://www.mp3quran.net'
AllReadersFile = 'AllReaders.html'

# Read the file with UTF8 because it contains Arabic characters
with open( AllReadersFile, encoding = "utf8" ) as streamReader:
    soup = BeautifulSoup( streamReader, 'html.parser' )
#print( soup.prettify() )   # Print the whole HTML

# Initialize an empty data frame
df = pandas.DataFrame( columns = ['الشيخ',
                                  'السور',
                                  'صفحة القارئ',
                                  'رقم السورة',
                                  'اسم السورة',
                                  'رابط السورة' ] )

readersHtml = soup.find_all( "div", { "class": "col-md-8" } )
print( "%s readers." % len( readersHtml ) )

if len( readersHtml ) > 0:
    print( 'Processing reader ', end = ' ' )
    i = 0   # Reader counter

for readerHtml in readersHtml:
    i += 1      # Increment reader counter to show progress
    print( '%d ' % i, end = ' ' )   # Print the reader number
    type = readerHtml.div["title"]  # عدد السور / أو القرآن كله
    reader = readerHtml.div.div.a.string    # اسم القارئ
    readerPage = baseURL + readerHtml.div.div.a["href"]     # صفحة القارئ

    # Open the reader details page
    with urlopen( Request (readerPage, headers={'User-Agent': 'Mozilla/5.0'} ) ) as streamReader:
#        print( streamReader.read().decode('utf-8'))
        soup = BeautifulSoup( streamReader.read(), 'html.parser')
        sorasHtml = soup.find_all( "div", { "class": "sora-item" } )
        print( "%s soras." % len( sorasHtml ) )
        
        for soraHtml in sorasHtml:
            soraNumber = soraHtml.find( "div", { "class": "sora-num" } ).string  # رقم السورة
            soraHyperlinkItem = soraHtml.find( "a", { "class": "card-reciter-name" } )  # Complete a tag
            soraName = soraHyperlinkItem.string  # اسم السورة
            soraURL = soraHyperlinkItem["href"] # رابط السورة

        # Append data frame row
        df = df.append( {
            "الشيخ": reader,
            "السور":  type,
            "صفحة القارئ": readerPage,
            'رقم السورة': soraNumber,
            'اسم السورة': soraName,
            'رابط السورة': soraURL
            }, ignore_index = True )

output = r'Readers.csv'
df.to_csv( output )

