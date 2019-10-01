from bs4 import BeautifulSoup
from selenium import webdriver
from shutil import which
import re
import urllib
from selenium.webdriver.firefox.options import Options as firefoxOptions

print('program started')
options = firefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(firefox_options=options)

#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,browser):
    browser.get(url)
    res_html = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

def scrape_dir_page(dir_url, browser):
    print('-'*20, 'Scrapping directory page', '-'*20)
    faculty_links = []
    # faculty_base_url = 'https://www.bitmesra.ac.in/'
    faculty_base_url = "https://www.iima.ac.in/"

    # execute js on webpage to load faculty listings on webpage and get ready to parse the loaded HTML
    soup = get_js_soup(dir_url, browser)
    for staff_group in soup.find_all('div',class_='faculty-wrapper'): #get list of all <div> of class 'photo nocaption'
        for full_time_f in staff_group.find_all('div', class_='full-time-f'):
            for s in full_time_f.find_all('a', href=True):
                rel_link = s.get('href')
                #url returned is relative, so we need to add base url
                faculty_links.append(faculty_base_url+rel_link)

    print ('-'*20,'Found {} faculty profile urls'.format(len(faculty_links)),'-'*20)
    print(faculty_links)
    return faculty_links

# dir_url = 'https://cs.illinois.edu/people/faculty/department-faculty'
# dir_url = 'https://www.bitmesra.ac.in/Show_Faculty_List?cid=1&deptid=70'
dir_url = "https://www.iima.ac.in/web/faculty/faculty-profiles/areawise-list"
browser.get(dir_url)
faculty_links = scrape_dir_page(dir_url, browser)

#tidies extracted text
def process_bio(bio):
    bio = bio.encode('ascii',errors='ignore').decode('utf-8')       #removes non-ascii characters
    bio = re.sub('\s+',' ',bio)       #repalces repeated whitespace characters with single space
    return bio

''' More tidying
Sometimes the text extracted HTML webpage may contain javascript code and some style elements. 
This function removes script and style tags from HTML so that extracted text does not contain them.
'''
def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup


#Checks if bio_url is a valid faculty homepage
def is_valid_homepage(bio_url,dir_url):
    try:
        #sometimes the homepage url points to the faculty profile page
        #which should be treated differently from an actual homepage
        ret_url = urllib.request.urlopen(bio_url).geturl()
    except:
        print("something went wrong with bio url")
        return False       #unable to access bio_url
    urls = [re.sub('((https?://)|(www.))','',url) for url in [ret_url,dir_url]] #removes url scheme (https,http) or www
    return not(urls[0]== urls[1])

def scrape_faculty_page(fac_url,browser):
    # fac_url = "https://www.iima.ac.in/web/faculty/faculty-profiles/akhileshwar-pathak"
    soup = get_js_soup(fac_url, browser)
    # print("fac_url: ", fac_url)

    homepage_found = False
    bio_url = ''
    bio = ''
    #find overview tab
    try:
        overview_tab = soup.find('div',class_='tab-inr-box-right')
    except:
        print (soup)

    # ot = overview_tab.find('h1')
    # if ot is not None:
    #     faculty_last_name = ot.get_text()
    # # print("name ", faculty_last_name)

    for my_ref in soup.find('div', class_='tab-inr-box-left').find_all('a', href=True):
        ref = my_ref.get('href')
        if "http" in ref:
            bio_url = ref
            homepage_found = True
            # check if homepage url is valid
            bio_soup = remove_script(get_js_soup(bio_url, browser))
            bio = process_bio(bio_soup.get_text(separator=' '))
            break

    if not homepage_found:
        bio_url = fac_url #treat faculty profile page as homepage
        #we're only interested in some parts of the profile page namely the address
        #and information listed under the Overview, Research, Publication and Awards tab
        bio = soup.find('div',class_='page-tab-content').get_text(separator=' ')+': '
        for tab in soup.find_all('div',class_='tab-pane'):
            bio += tab.get_text(separator=' ')+'. '
        bio = process_bio(bio)
    return bio_url,bio

#Scrape all faculty homepages using profile page urls
bio_urls, bios = [],[]
tot_urls = len(faculty_links)
cnt = 0
for i,link in enumerate(faculty_links):
    print ('-'*20,'Scraping faculty url {}/{}'.format(i+1,tot_urls),'-'*20)
    bio_url,bio = scrape_faculty_page(link,browser)
    bio_urls.append(bio_url)
    bios.append(bio)
    cnt = cnt + 1
    # if cnt == 100:
    #     break


def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')

bio_urls_file = 'bio_urls.txt'
bios_file = 'bios.txt'
write_lst(bio_urls,bio_urls_file)
write_lst(bios,bios_file)


