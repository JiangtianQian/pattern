from urllib import urlopen
from urllib import FancyURLopener
import json
from requests.exceptions import ConnectionError
from httplib import IncompleteRead

def formatNonAscii(text):
    text = text.replace('\n', ' ').replace('\r', '')
    return ''.join([i if ord(i) < 128 else '' for i in text])

class MyOpener(FancyURLopener):
            version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
            
def main(petitionUrl):
    offset = 0
    title = petitionUrl[0:]
    print title
    baseUrl = 'https://www.change.org/api-proxy/-/petitions/%s/comments?limit=10&offset=%d&order_by=voting_score'
    while(True):
        try:
            url = baseUrl % (title, offset)
            #outfile = "%s_comment_info.txt" % (title)
            myopener = MyOpener()
            raw = myopener.open(url)
            try:
                d = json.loads(raw.read())
            except ValueError,e:
                return False
            if d.has_key('items'):            
                for comment in d['items']:
                    write_dict = {}
                    write_dict["user_id"] = comment['user_id']
                    write_dict["timestamp"] = comment['created_at']
                    #write_dict['likes'] = comment['likes']
                    write_dict["city"] = comment['user']['city']
                    write_dict["country_code"] = comment['user']['country_code']
                    write_dict["state_code"] = comment['user']['state_code']     
                    #write_dict['comment'] = comment['comment']
                    #write_dict['id'] = comment['id']
                    write_dict['petition'] = comment['petition']['is_victory']
                    write_dict["petition_overview"] = comment['petition']['petition_title']
                    write_dict["petition_status"] = comment['petition']['petition_status']
                    write_dict["petition_id"] = comment['petition_id']
                    write_dict["created_at"] = comment['petition']['created_at']              
                    write_dict["petition_text"] = comment['petition']['description']
                    write_dict["creator"] = comment['petition']['user']['id']
                    write_dict["tags"] = comment['petition']['tags']
    
                    open("result.txt",'a').write("%s\n" % write_dict)
                if (d["last_page"] == True):
                    #print "done"
                    break
                else:
                    offset += 10
            else: 
                return False
        except ConnectionError:
            print "Connection Issue"
            continue
        except IncompleteRead:
            print "IncompleteRead"
            continue
            
    return


