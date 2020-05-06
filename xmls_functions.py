import glob 
import argparse 
import lxml 
from bs4 import BeautifulSoup as bs # Needed for parsing sitemaps
import xlsxwriter # Needed for Excel file output


def parse_arguments():
    """Parsing the arguments and/or displaying help information"""
    parser = argparse.ArgumentParser(description="""
    Export all URLs from all XML sitemaps contained in the current 
        directory. Outputs URLs to a file which you can specify, with 
        support for Excel (.xlsx), comma-separated values (.csv), and plain 
        text (.txt). Features options for deduplication, ignoring of index 
        files, and sorting alphanumerically, detailed below.""",
    epilog="Feel free to email taylor@climbmarketing.com for further help.")
    
    parser.add_argument("--o", metavar="outputFileName", default="output.txt", 
    type=str, help="""file name for output (defaults to output.txt). 
        Ending in .xlsx will automatically format the output for Excel.""")
    
    parser.add_argument("--deduplicate", action="store_true", 
        help="add this argument to turn on URL deduplication")
    
    parser.add_argument("--ignore_index", action="store_true", 
        help="""add this argument to ignore sitemap index files. It will 
        still count links to other .xml files found in non-index files, 
        just in case they're not sitemaps.""")
    
    parser.add_argument("--sort", action="store_true", 
        help="add this argument to sort output alphanumerically.")
    
    namespace = parser.parse_args()
    
    return namespace


def detect_sitemaps():
    """Checking to ensure sitemaps present, announcing number found"""
    number_of_sitemaps = len(glob.glob('*.xml'))
    if number_of_sitemaps == 0:
        print("""Error: No sitemaps detected in current directory. 
            Ensure that they end in .xml, and that you've navigated to 
            the correct folder.""")
        exit()
    print(f"Detected {number_of_sitemaps} XML files in current directory.")
    return number_of_sitemaps


def process_sitemap(filename, namespace):
    """Extracting the URLs from each sitemap and returning a list"""
    urls_from_this_sitemap = []

    # Get the entire contents of each XML sitemap as a string.
    with open(filename, "r") as f:

        # Next we use BeautifulSoup to parse the data in XML format.
        soup = bs(f.read(), 'lxml')
        URLs = soup.find_all("loc") # This finds everything in <loc> tags.

    # If the user has opted to ignore sitemap indeces and the 
    # sitemapindex tag is detected in a file, pass over that sitemap.
    if (namespace.ignore_index and soup.find("sitemapindex")):
        return []

    # Then we have to strip off the <loc> and </loc> tags.
    for URL in URLs:
        urls_from_this_sitemap.append(str(URL)[5:len(URL)-7])

    return urls_from_this_sitemap


def deduplicate_urls(cleaned_urls):
    """Simple deduplication via conversion to a set, with user feedback"""
    lengthBefore = len(cleaned_urls)
    print("Deduplicating output...", end=" ")
    cleaned_urls = set(cleaned_urls) # fast but unsorted deduplication
    print(f"removed {lengthBefore-len(cleaned_urls)} URLs via deduplication.")
    return cleaned_urls


def output_urls(cleaned_urls, filename):
    """Writing the output to a file"""
    if not filename.endswith(".xlsx"):
        # Because our data is single-column, CSV is actually the 
        # same format as plain text in this instance. So as long
        # as the user doesn't want Excel, we can just do a standard
        # file write.  
        with open(filename, "w+") as g:
            g.write("\n".join(cleaned_urls))
    else: 
        # Excel limits worksheets to 65,530 URLs. We can get around 
        # this, if necessary, by turning off string to URL conversions.
        if len(cleaned_urls) > 65530: 
            workbook = xlsxwriter.Workbook(filename, {'strings_to_urls': False})
        else:
            workbook = xlsxwriter.Workbook(filename, {'strings_to_urls': True})
        worksheet = workbook.add_worksheet()

        # Writing one URL per row using enumerate() for row numbers.
        # Also filters out any data that begins with "=" in order to
        # prevent exploitation of a known Excel vulnerability.
        for row_num, data in enumerate(cleaned_urls):
            if not data.startswith("="): 
                worksheet.write(row_num, 0, data)
        workbook.close()
