#!
import requests
from bs4 import BeautifulSoup
from ghost import Ghost, Session
import yaml
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import io
import threading

##############################
def get_checkout_info():
  global name, email, tel, address1, address2,  zip, city, state, card, cvv, month, year
  name = name_var.get()
  email = email_var.get()
  phone = tel_var.get()
  tel = '(%s) %s-%s' % (phone[0:3], phone[3:6], phone[6:10])
  address1 = address1_var.get()
  address2 = address2_var.get()
  zip = zip_var.get()
  city = city_var.get()
  state = "\'%s\'" % state_var.get()
  cc = cc_var.get()
  card = "%s %s %s %s" % (cc[0:4], cc[4:8], cc[8:12], cc[12:16])
  cvv = cvv_var.get()
  month = "\'%s\'" % month_var.get()
  year = "\'%s\'" % year_var.get()


##############################
home = 'http://www.supremenewyork.com/mobile/#categories'
cart_url = 'http://www.supremenewyork.com/shop/cart'
checkout_url = 'https://www.supremenewyork.com/checkout'
json_url = 'http://www.supremenewyork.com/mobile_stock.json'
##############################
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
header = {'User-Agent':ua_mo}
def load_ghost():
  global se
  gh = Ghost()
  se = Session(gh, user_agent=ua, wait_timeout=20, wait_callback=None, display=True, viewport_size=(800, 680), download_images=True)

#se_mo = Session(gh, user_agent=ua_mo, wait_timeout=20, wait_callback=None, display=True, viewport_size=(375, 553), download_images=True)
##############################
def load_data():
  global categories
  global supreme_data
  print('Loading data...')
  supreme_json = requests.get(json_url, headers = header,verify=False).content.decode(encoding='utf-8')
  supreme_data = yaml.load(supreme_json)
  # Categories
  categories = list(supreme_data['products_and_categories'])
  #categories.remove('new')
  categories.sort()
  #categories = ['new']

load_data()
# All Items
#all_items = []
#for i in categories:
#  print("-----------------"+i+"-----------------")
#  for l in supreme_data['products_and_categories'][i]:
#    #print(l)
#    all_items.append(l)

#all_items
# Jackets_list etc.

# new1['style'][1][name]
def get_data_json(i, l):
    print('loading items data...')
    globals()[i+str(l)+'_json_url'] = 'http://www.supremenewyork.com/shop/%s.json' % globals()[i+str(l)+'_id']
    globals()[i+str(l)+'_json'] = requests.get(globals()[i+str(l)+'_json_url'], headers = header,verify=False).content.decode(encoding='utf-8')
    globals()[i+str(l)] = yaml.load(globals()[i+str(l)+'_json'])['styles']

def get_data():
  global threads_data
  threads_data = []
  for i in categories:
    globals()[i+'_list'] = supreme_data['products_and_categories'][i]
    for l in range(len(globals()[i+'_list'])):
      # new1_id
      globals()[i+str(l)+'_id'] = globals()[i+'_list'][l]['id']
      a = threading.Thread(target=get_data_json, args=(i, l))
      threads_data.append(a)
      a.start()
  #for t in threads_data:
  #  t.join()

get_data()
print('bbb')

##################

w = Tk()
w.title('Test')
##################################
# Load IMG

def get_image(i, l):
  img_url = 'http:'+globals()[i+'_list'][l]['image_url_hi']
  print(img_url)
  globals()[i+ str(l)+'_img'] = Image.open(io.BytesIO(requests.get(img_url, timeout=15).content))
  #print(globals()[i+ str(l)+'_img'])
  #type(globals()[i+ str(l)+'_img'])

def get_image_clr(i, l, m):
  print('Loading Image')
  img_url = 'http:' + globals()[i+str(l)][m]['swatch_url']
  globals()['frame_'+i+str(l)+'_clr'+str(m)+'_img'] = Image.open(io.BytesIO(requests.get(img_url, timeout=15).content))

def load_img():
  global threads_img
  threads_img = []
  for t in threads_data:
    t.join()
  for i in categories:
    for l in range(len(globals()[i+'_list'])):
      #a = threading.Thread(target=get_image, args=(i, l))
      #threads_img.append(a)
      #a.start()
      for m in range(len(globals()[i+str(l)])):
        a = threading.Thread(target=get_image_clr, args=(i, l, m))
        threads_img.append(a)
        a.start()
  #for t in threads_img:
  #  t.join()

load_img ()
print('Loading Frame...')
##################################
def load_main_frame():
  global top
  global info
  global cart
  global panel
  top = Frame(w, width=900, height=75)
  info = Frame(w, width=700, height=375)
  cart = Frame(w, width=200, height=375)
  panel = Frame(w, width=900, height=100)
  ####################################
  top.pack(side='top', expand=N, fill=X, padx=5, pady=5)
  panel.pack(side='bottom', expand=N, fill=BOTH, padx=5, pady=5)
  info.pack(side='left', expand=Y, fill=BOTH, padx=5, pady=5)
  cart.pack(side='right', expand=N, fill=BOTH, padx=5, pady=5)

load_main_frame()

def load_top():
  global logo_img
  logo_url = 'http://d17ol771963kd3.cloudfront.net/assets/logo-supreme-f71fe1ba25b4dc78c31dce2cda1178e1.png'
  logo_img = ImageTk.PhotoImage(Image.open(io.BytesIO(requests.get(logo_url).content)))
  logo = ttk.Label(top, image=logo_img)
  logo.pack(expand=N, anchor=CENTER, pady=4)

load_top()

################################

def load_panel():
  load_address_box()
  load_bill_box()
  crate_checkout_button()

def load_address_box():
  global name_var
  global address1_var
  global address2_var
  global zip_var
  global city_var
  global state_var
  global country_var
  address_box = ttk.LabelFrame(panel, text="Shipping Info", width=400, height=500)
  address_box.pack(side=LEFT, padx=5, pady=5, ipadx=5, ipady=2, expand=N)
  # Name
  name_text = ttk.Label(address_box, text='Name: ')
  name_text.grid(row=0, column=0, sticky=W, padx=2, pady=2)
  name_var = tk.StringVar()
  name_Entry = ttk.Entry(address_box, textvariable=name_var)
  name_Entry.grid(row=0, column=1, columnspan=2, sticky=EW)
  # Address
  address1_text = ttk.Label(address_box, text='Address: ')
  address1_text.grid(row=1, column=0, sticky=W, padx=2, pady=2)
  address1_var = tk.StringVar()
  address1_Entry = ttk.Entry(address_box, textvariable=address1_var, width=22)
  address1_Entry.grid(row=1, column=1, columnspan=2, sticky=EW)
  # Address2
  address2_text = ttk.Label(address_box, text='Address 2/Zip: ')
  address2_text.grid(row=2, column=0, sticky=W, padx=2, pady=2)
  address2_var = tk.StringVar()
  address2_Entry = ttk.Entry(address_box, textvariable=address2_var, width=10)
  address2_Entry.grid(row=2, column=1, sticky=EW)
  # Zip
  #zip_text = ttk.Label(address_box, text='Zip: ')
  #zip_text.grid(row=1, column=2, sticky=W, padx=2, pady=2)
  zip_var = tk.StringVar()
  zip_Entry = ttk.Entry(address_box, textvariable=zip_var, width=7)
  zip_Entry.grid(row=2, column=2, sticky=E)
  # City
  city_text = ttk.Label(address_box, text='City/State: ')
  city_text.grid(row=3, column=0, sticky=W, padx=2, pady=2)
  city_var = tk.StringVar()
  city_Entry = ttk.Entry(address_box, textvariable=city_var, width=10)
  city_Entry.grid(row=3, column=1, sticky=W)
  # State
  state_var = tk.StringVar()
  state_Combo = ttk.Combobox(address_box, width=10, textvariable=state_var)
  state_Combo['values'] = ("AL", "AK", "AS", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FM", "FL", "GA", "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MH", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "MP", "OH", "OK", "OR", "PW", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VI", "VA", "WA", "WV", "WI", "WY")
  state_Combo.grid(row=3, column=2)
  state_Combo.current(0)
  state = "\'" + state_var.get() + "\'"
  # Country
  country_text = ttk.Label(address_box, text='Country: ')
  country_text.grid(row=4, column=0, sticky=W, padx=2, pady=2)
  country_var = tk.StringVar()
  country_Combo = ttk.Combobox(address_box, width=10, textvariable=country_var)
  country_Combo['values'] = ("USA", "Canada")
  country_Combo.grid(row=4, column=1, sticky=W)
  country_Combo.current(0)

def load_bill_box():
  global tel_var
  global email_var
  global cc_var
  global cvv_var
  global month_var
  global year_var
  global cc_var
  bill_box = ttk.LabelFrame(panel, text="Billing Info", width=400, height=500)
  bill_box.pack(side=LEFT, padx=5, pady=5, ipadx=5, ipady=2, expand=N)
  # Tel
  tel_text = ttk.Label(bill_box, text='Tel: ')
  tel_text.grid(row=0, column=0, sticky=W, padx=2, pady=2)
  tel_var = tk.StringVar()
  tel_Entry = ttk.Entry(bill_box, textvariable=tel_var)
  tel_Entry.grid(row=0, column=1, columnspan=2, sticky=EW)
  # Email
  email_text = ttk.Label(bill_box, text='Email: ')
  email_text.grid(row=1, column=0, sticky=W, padx=2, pady=2)
  email_var = tk.StringVar()
  email_Entry = ttk.Entry(bill_box, textvariable=email_var)
  email_Entry.grid(row=1, column=1, columnspan=2, sticky=EW)
  # Credit_Card
  cc_text = ttk.Label(bill_box, text='Card Number: ')
  cc_text.grid(row=2, column=0, sticky=W, padx=2, pady=2)
  cc_var = tk.StringVar()
  cc_Entry = ttk.Entry(bill_box, textvariable=cc_var)
  cc_Entry.grid(row=2, column=1, columnspan=2, sticky=EW)
  # CVV
  cvv_text = ttk.Label(bill_box, text='CVV: ')
  cvv_text.grid(row=3, column=0, sticky=W, padx=2, pady=2)
  cvv_var = tk.StringVar()
  cvv_Entry = ttk.Entry(bill_box, width=5, textvariable=cvv_var)
  cvv_Entry.grid(row=3, column=1)
  # Month/Year
  month_text = ttk.Label(bill_box, text='Month/Year: ')
  month_text.grid(row=4, column=0, sticky=W, padx=2, pady=2)
  month_var = tk.StringVar()
  month_Combo = ttk.Combobox(bill_box, width=10, textvariable=month_var)
  month_Combo['values'] = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
  month_Combo.grid(row=4, column=1, sticky=W)
  # Year
  year_var = tk.StringVar()
  year_Combo = ttk.Combobox(bill_box, width=10, textvariable=year_var)
  year_Combo['values'] = ("2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025")
  year_Combo.grid(row=4, column=2, sticky=E)

def checkout():
  get_checkout_info()
  se.open(checkout_url)
  checkout_html = se.content
  checkout_soup =  BeautifulSoup(checkout_html, "html.parser")
  card_id = str(checkout_soup.select('input.string')[7].get('id'))
  cvv_id = str(checkout_soup.select('input.string')[8].get('id'))
  se.click("input[id=order_billing_name]", expect_loading=False)
  se.click(".has-checkbox > div:nth-child(2) > ins:nth-child(2)", expect_loading=False)
  # Fill
  se.set_field_value("input[id=order_billing_name]", name)
  se.set_field_value("input[id=order_email]", email)
  se.set_field_value("input[id=order_tel]", tel)
  se.set_field_value("input[id=bo]", address1)
  se.set_field_value("input[id=oba3]", address2)
  se.set_field_value("input[id=order_billing_zip]", zip)
  se.set_field_value("input[id=order_billing_city]", city)
  se.set_field_value("input[id=" + card_id + "]", card)
  se.set_field_value("input[id=" + cvv_id + "]", cvv)
  se.evaluate("document.getElementById('order_billing_state').value=" + state)
  se.evaluate("document.getElementById('credit_card_month').value=" + month)
  se.evaluate("document.getElementById('credit_card_year').value=" + year)
  se.show()

def crate_checkout_button():
  checkout_button = ttk.Button(panel, text='CHECKOUT', width=40, command=checkout)
  checkout_button.pack(side=RIGHT, expand=N, fill=None)

###############################
# Buttons
def reload_tab():
  current_index = tabControl.index(tabControl.select())
  tabControl.forget(current_index)
  load_img()
  load_canvas()
  check_stock()

def reload_all():
  load_data()
  get_data()
  load_img()
  for i in categories:
    globals()['cv_'+i].destroy()
    globals()['sbar_'+i].destroy()
  load_canvas()
  check_stock()

def check_stock():
  for i in categories:
    for l in range(len(globals()[i+'_list'])):
      for m in range(len(globals()[i+str(l)])):
        for n in range(len(globals()[i+str(l)][m]['sizes'])):
          if globals()[i+str(l)][m]['sizes'][n]['stock_level'] == 0:
            globals()['frame_'+i+str(l)+'_clr'+str(m)+'_size'+str(n)].config(state = DISABLED)

def add_item(i, l, m, n):
  item_id = globals()[i+'_list'][l]['id']
  size_id = globals()[i+str(l)][m]['id']
  for s in range(0, n):
    if globals()[i+str(l)][m]['sizes'][s]['stock_level'] == 0:
      n -= 1
  item_cat = supreme_data['products_and_categories'][i][l]['category_name']
  if item_cat == 'Tops/Sweaters':
    item_cat = 'Tops_Sweaters'
  item_url = 'http://www.supremenewyork.com/shop/%s/%s/%s' % (item_cat, item_id, size_id)
  print(item_url)
  se.open(item_url)
  se.evaluate("document.getElementById('s').selectedIndex=%s" % n)
  se.evaluate("""document.querySelector('input[name="commit"]').click();""")
  se.sleep(0.5)
  #globals()['frame_'+i+str(l)+'_clr'+str(m)+'_size'+str(n)].config(state = ACTIVE)
  if se.exists('input.remove') == True:
    pass
    #globals()['frame_'+i+str(l)+'_clr'+str(m)+'_size'+str(n)].config(background='#234')
  else:
    pass
    #globals()['frame_'+i+str(l)+'_clr'+str(m)+'_size'+str(n)].config(background=orig_color)
  #se.evaluate("document.getElementById('s').selectedIndex = " + size + ';')

def add(i, l, m, n):
  global threads_add
  threads_add = []
  a = threading.Thread(target=add_item, args=(i, l, m, n))
  threads_add.append(a)
  a.start()

def view_cart():
  se.open(cart_url)
  cart_html = se.content
  cart_soup = BeautifulSoup(cart_html, "html.parser")
  cart_items = cart_soup.select('tr')
  print ('-----------------------Cart List-----------------------')
  for i in range(len(cart_items)):
    globals()['item'+str(i)] = cart_items[i].select('.cart-description')[0].text
    globals()['price'+str(i)] = cart_items[i].select('.cart-price-span')[0].text
    print ('\033[1;35mItem: ' + '\033[1;34m' + globals()['item'+str(i)] + '\033[1;35m   Price: ' + '\033[1;31m' + globals()['price'+str(i)] + '\033[0m')
  print ('-------------------------End--------------------------')

###############################
def load_tabs():
  global tabControl
  tabControl = ttk.Notebook(info, width=1100, height=500)
  for i in categories:
    # add tab
    globals()['tab_'+i] = ttk.Frame(tabControl)
    tabControl.add(globals()['tab_'+i], text=i+str(len(globals()[i+'_list'])))
    tabControl.pack(expand=N, fill="both")
    # Reload All
    globals()['reload_all_'+i] = ttk.Button(globals()['tab_'+i], text='RELOAD ALL', command=reload_all)
    globals()['reload_all_'+i].pack(side=TOP, expand=N, fill=X)
    # Reload Buttons
    globals()['cart_button'] = ttk.Button(globals()['tab_'+i], text='View Cart', command=view_cart)
    globals()['cart_button'].pack(side=BOTTOM, expand=N, fill=X)

def load_canvas():
  for i in categories:
    # Create Canvas
    globals()['cv_'+i] = Canvas(globals()['tab_'+i], bg = 'white', width=850, height=900, scrollregion=(0,0,1050,1000))
    globals()['sbar_'+i] = ttk.Scrollbar(globals()['tab_'+i], orient=VERTICAL)
    globals()['sbar_'+i].pack(side='right', fill=Y, expand=N)
    globals()['sbar_'+i].config(command=globals()['cv_'+i].yview)
    globals()['cv_'+i].config(yscrollcommand=globals()['sbar_'+i].set)
    globals()['cv_'+i].pack(fill=X, expand=N)
    #globals()['cv'+str(i)].config(width=700,height=900)
    globals()['cv_Frame_'+i] = tk.Frame(globals()['cv_'+i], width=850, height=900)
    globals()['cv_Frame_'+i].pack(expand=N, fill=None)
    globals()['cv_'+i].create_window((0,0), window=globals()['cv_Frame_'+i],anchor='nw')
    ####
    for l in range(len(globals()[i+'_list'])):
      j = l % 5
      k = l // 5
      name = globals()[i+'_list'][l]['name']
      price = '$ %s' % (globals()[i+'_list'][l]['price']/100)
      id = 'ID: ' + str(globals()[i+'_list'][l]['id'])
      # Items/frame_jackets1
      globals()['frame_'+i+str(l)] = tk.Frame(globals()['cv_Frame_'+i], width=200, height=100, relief=SUNKEN, bg='yellow')
      globals()['frame_'+i+str(l)].grid(row=k, column=j, sticky="nsew", padx=10, pady=10)
      # Frame_kind
      globals()['frame_'+i+str(l)+'_kind'] = tk.Frame(globals()['frame_'+i+str(l)], width=200, height=100, bg='blue')
      globals()['frame_'+i+str(l)+'_kind'].pack(expand=N, fill=X, ipadx=3, ipady=3)
      # Kind_Name 
      globals()['frame_'+i+str(l)+'_kind_name'] = tk.Label(globals()['frame_'+i+str(l)+'_kind'], text=name, wraplength=200)
      globals()['frame_'+i+str(l)+'_kind_name'].pack(side=TOP, expand=N, fill=None)
      # Kind_Price
      globals()['frame_'+i+str(l)+'_kind_price'] = tk.Label(globals()['frame_'+i+str(l)+'_kind'], text=price, wraplength=200)
      globals()['frame_'+i+str(l)+'_kind_price'].pack(side=BOTTOM, expand=N, fill=None)
      # Kind_Id
      globals()['frame_'+i+str(l)+'_kind_id'] = tk.Label(globals()['frame_'+i+str(l)+'_kind'], text=id, wraplength=200)
      globals()['frame_'+i+str(l)+'_kind_id'].pack(side=BOTTOM, expand=N, fill=None)
      # 
      for m in range(len(globals()[i+str(l)])):
        # frame_new1_clr1
        globals()['frame_'+i+str(l)+'_clr'+str(m)] = tk.Frame(globals()['frame_'+i+str(l)], width=200, height=30, bg='red')
        globals()['frame_'+i+str(l)+'_clr'+str(m)].pack(expand=N, fill=None, padx=2, pady=2)
        # frame_new1_clr1_img
        for t in threads_img:
          t.join()
        globals()['frame_'+i+str(l)+'_clr'+str(m)+'_image'] = ImageTk.PhotoImage(globals()['frame_'+i+str(l)+'_clr'+str(m)+'_img'].resize((100, 100), Image.ANTIALIAS))
        globals()['frame_'+i+str(l)+'_clr'+str(m)+'_image_l'] = tk.Label(globals()['frame_'+i+str(l)+'_clr'+str(m)], image=globals()['frame_'+i+str(l)+'_clr'+str(m)+'_image'])
        globals()['frame_'+i+str(l)+'_clr'+str(m)+'_image_l'].pack(side=LEFT, expand=N, fill=None)
        # frame_new1_clr1_size1
        for n in range(len(globals()[i+str(l)][m]['sizes'])):
          globals()['frame_'+i+str(l)+'_clr'+str(m)+'_size'+str(n)] = ttk.Button(globals()['frame_'+i+str(l)+'_clr'+str(m)], text=globals()[i+str(l)][m]['sizes'][n]['name'][0], command=lambda a=i, b=l, c=m, d=n: add_item(a, b, c, d))
          globals()['frame_'+i+str(l)+'_clr'+str(m)+'_size'+str(n)].pack(side=TOP, expand=Y, fill=BOTH)
          #globals()['frame_'+i+str(l)+'_clr'+str(m)+'_size'+str(n)].config(command=lambda: exec("add_item(\'%s\', %s, %s, %s)" % globals()['frame_'+i+str(l)+'_clr'+str(m)+'_size'+str(n)+'_com']))
    globals()['cv_'+i].config(scrollregion=(0, 0, globals()['cv_Frame_'+i].winfo_width(), globals()['cv_Frame_'+i].winfo_height()))

load_panel()
load_tabs()
load_canvas()
check_stock()
#############################################

#def get_inside(i, l):
#  #global img
#  img = ImageTk.PhotoImage(globals()[i+ str(l)+'_img'].resize((150, 150), Image.ANTIALIAS))
#  #globals()[i+ str(l)+'_img'] = globals()[i+ str(l)+'_img'].resize((200, 200), Image.ANTIALIAS)
#  globals()['frame_'+i+str(l)+'_kind_image'] = Label(globals()['frame_'+i+str(l)+'_kind'], image=img)
#  globals()['frame_'+i+str(l)+'_kind_image'].pack(side=TOP, expand=N, fill=None)
#  globals()['frame_'+i+str(l)+'_kind_image'].image=img

#def load_inside():
#  for t in threads_img:
#    t.join()
#  for i in categories:
#    for l in range(len(globals()[i+'_list'])):
#      get_inside(i, l)

def scroll():
  for i in categories:
    globals()['cv_'+i].config(scrollregion=(0, 0, globals()['cv_Frame_'+i].winfo_width(), globals()['cv_Frame_'+i].winfo_height()))
  w.after(1000, scroll)

scroll()
load_ghost()
print('Done')
#load_inside()
#def scroll():
#  for z in categories:
#    globals()['cv_'+z].config(scrollregion=(0, 0, 1000, 2000))
#
#ttt()
#print(globals()['cv_Frame_'+i].winfo_height())
#for i in categories:
#  globals()['cv_'+i].config(scrollregion=(0, 0, globals()['cv_Frame_'+i].winfo_width(), globals()['cv_Frame_'+i].winfo_height()))
#######################
mainloop()

import code
code.interact(banner = "", local = locals())



