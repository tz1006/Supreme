#! 
from ghost import Ghost, Session
from datetime import datetime

item_url = 'http://www.supremenewyork.com/shop/jackets/paqit58sw/zsq01xw7m'
checkout_url = 'https://www.supremenewyork.com/checkout'
##############################
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
header = {'User-Agent':ua}
gh = Ghost()
se = Session(gh, user_agent=ua, wait_timeout=20, wait_callback=None, display=True, viewport_size=(1080, 1680), download_images=True)
##############################

se.open(item_url)
se.evaluate("""document.querySelector('input[name="commit"]').click();""")
se.sleep(0.5)
se.open(checkout_url)

ISOFORMAT='%Y%m%d'
today =datetime.today()
filename = today.strftime(ISOFORMAT)
f = open('supreme'+'/'+filename+'.html', 'w') 
f.write(se.content) 
f.close() 

import code
code.interact(banner = "", local = locals())
