# -*- coding: utf-8 -*-
"""BizCardX.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n9wm-N-qHphH2r2rMatnFT4xguCERx59
"""

pip install easyocr

pip install streamlit

pip install streamlit_option_menu

import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import sqlite3

def image_to_text(path):
  input_img=Image.open(path)
  #converting image to array format
  image_arr=np.array(input_img)

  reader= easyocr.Reader(['en'])
  text=reader.readtext(image_arr,detail=0)
  return text,input_img

text_img, input_img=image_to_text(r"/content/1.png")

def extracted_text(texts):
  extracted_dict={"NAME":[],"DESIGNATION":[],"COMPANYNAME":[],"CONTACT":[],"EMAIL":[],"WEBSITE":[],
                  "ADDRESS":[],"PINCODE":[]}
  extracted_dict["NAME"].append(texts[0])
  extracted_dict["DESIGNATION"].append(texts[1])

  for i in range(2,len(texts)):
    if texts[i].startswith("+") or (texts[i].replace("-","").isdigit() and '-' in texts[i]):
      extracted_dict["CONTACT"].append(texts[i])
    elif "@" in texts[i] and ".com" in texts[i]:
      extracted_dict["EMAIL"].append(texts[i])
    elif "WWW" in texts[i] or "www" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wwW" in texts[i]:
      small= texts[i].lower()
      extracted_dict["WEBSITE"].append(small)
    elif "Tamil Nadu" in texts[i] or "TamilNadu" in texts[i] or texts[i].isdigit():
      extracted_dict["PINCODE"].append(texts[i])
    elif re.match(r'^[A-Za-z]',texts[i]):
      extracted_dict["COMPANYNAME"].append(texts[i])
    else:
      remove_col=re.sub(r'[,;]','',texts[i])
      extracted_dict["ADDRESS"].append(remove_col)

  for key,value in extracted_dict.items():
    if len(value)>0:
      concatenate=" ".join(value)
      extracted_dict[key]=[concatenate]
    else:
      value="NA"
      extracted_dict[key]=[value]

  return extracted_dict

text_img, input_img=image_to_text(r"/content/2.png")

text_img, input_img=image_to_text(r"/content/3.png")

text_img, input_img=image_to_text(r"/content/4.png")

text_img, input_img=image_to_text(r"/content/5.png")

text_img

text_data=extracted_text(text_img)

df=pd.DataFrame(text_data)
df

input_img

#converting Image to bytes
Image_bytes=io.BytesIO()
input_img.save(Image_bytes,format="png")
image_data=Image_bytes.getvalue()

#creating dictionary
data={"IMAGE":[image_data]}

df_1=pd.DataFrame(data)
concat_df=pd.concat([df,df_1],axis=1)
concat_df

mydb =sqlite3.connect("bizcardx.db")
cursor = mydb.cursor()

#table creation
create_table_query='''CREATE TABLE IF NOT EXISTS bizcard_details(name varchar(300),
                                                                  designation varchar(300),
                                                                  company_name varchar(300),
                                                                  contact varchar(300),
                                                                  email varchar(300),
                                                                  website text,
                                                                  address text,
                                                                  pincode varchar(300),
                                                                  image text)'''

cursor.execute(create_table_query)
mydb.commit()


#insert query
insert_query='''INSERT INTO bizcard_details(name,designation,company_name,contact,
                                              email,website,address,
                                              pincode,image)
                                              values(?,?,?,?,?,?,?,?,?)'''
datas=concat_df.values.tolist()[0]
cursor.execute(insert_query,datas)
mydb.commit()

#select query
select_query="SELECT * from bizcard_details"
cursor.execute(select_query)
table=cursor.fetchall()
mydb.commit()

table_df=pd.DataFrame(table,columns=("NAME","DESIGNATION","COMPANY_NAME","CONTACT","EMAIL",
                                     "WEBSITE","ADDRESS","PINCODE","IMAGE"))
table_df

datas=concat_df.values.tolist()[0]
datas

# Commented out IPython magic to ensure Python compatibility.
# %%writefile bizcard.py
# import streamlit as st
# from streamlit_option_menu import option_menu
# import easyocr
# from PIL import Image
# import pandas as pd
# import numpy as np
# import re
# import io
# import sqlite3
# 
# def image_to_text(path):
#   input_img=Image.open(path)
#   #converting image to array format
#   image_arr=np.array(input_img)
# 
#   reader= easyocr.Reader(['en'])
#   text=reader.readtext(image_arr,detail=0)
#   return text,input_img
# 
# 
# def extracted_text(texts):
#   extracted_dict={"NAME":[],"DESIGNATION":[],"COMPANYNAME":[],"CONTACT":[],"EMAIL":[],"WEBSITE":[],
#                   "ADDRESS":[],"PINCODE":[]}
#   extracted_dict["NAME"].append(texts[0])
#   extracted_dict["DESIGNATION"].append(texts[1])
# 
#   for i in range(2,len(texts)):
#     if texts[i].startswith("+") or (texts[i].replace("-","").isdigit() and '-' in texts[i]):
#       extracted_dict["CONTACT"].append(texts[i])
#     elif "@" in texts[i] and ".com" in texts[i]:
#       extracted_dict["EMAIL"].append(texts[i])
#     elif "WWW" in texts[i] or "www" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wwW" in texts[i]:
#       small= texts[i].lower()
#       extracted_dict["WEBSITE"].append(small)
#     elif "Tamil Nadu" in texts[i] or "TamilNadu" in texts[i] or texts[i].isdigit():
#       extracted_dict["PINCODE"].append(texts[i])
#     elif re.match(r'^[A-Za-z]',texts[i]):
#       extracted_dict["COMPANYNAME"].append(texts[i])
#     else:
#       remove_col=re.sub(r'[,;]','',texts[i])
#       extracted_dict["ADDRESS"].append(remove_col)
# 
#   for key,value in extracted_dict.items():
#     if len(value)>0:
#       concatenate=" ".join(value)
#       extracted_dict[key]=[concatenate]
#     else:
#       value="NA"
#       extracted_dict[key]=[value]
# 
#   return extracted_dict
# 
# 
# # Streamlit part
# 
# st.set_page_config(layout="wide")
# # Set background color and size directly
# def setting_bg():
#   st.markdown(f"""
#     <style>.stApp{{
#       background:url("https://images.unsplash.com/photo-1551376347-075b0121a65b?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
#       background-size: cover}}
#     </style>""", unsafe_allow_html=True)
# setting_bg()
# st.title(":rainbow[EXTRACTING BUSINESS CARD DATA WITH OCR]")
# 
# with st.sidebar:
# 
#   select=option_menu("Main Menu",["HOME","Upload & Modify","Delete"])
# 
# if select=="HOME":
#   st.markdown("### Welcome to the Business Card Application!")
#   st.markdown("## :green[**Technologies Used :**] Python,easy OCR, Streamlit, SQL, Pandas")
#   st.markdown("## :green[**Overview :**] In this streamlit web app you can upload an image of a business card and extract relevant information from it using easyOCR. You can view, modify or delete the extracted data in this app. This app would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.")
#   img1=Image.open("/content/ocrpic.png")
#   st.image(img1,width=800)
#   st.write('### The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')
#   st.write("###   To Learn more about easyOCR [press here](https://pypi.org/project/easyocr/) ")
# 
# 
# elif select=="Upload & Modify":
# 
#   img=st.file_uploader("Upload the Image:",type=["png","jpg","jpeg"])
# 
#   if img is None:
#     st.write(":red[Card Is Not Uploaded]")
#   if img is not None:
#     st.image(img,width=500)
#     st.success("Card Is successfully Uploaded")
#     text_img, input_img= image_to_text(img)
#     text_dict=extracted_text(text_img)
# 
#     if text_dict:
#       st.success("TEXT IS SUCCESSFULLY EXTRACTED")
# 
#     df=pd.DataFrame(text_dict)
# 
#     #converting Image to bytes
#     Image_bytes=io.BytesIO()
#     input_img.save(Image_bytes,format="png")
#     image_data=Image_bytes.getvalue()
# 
#     #creating dictionary
#     data={"IMAGE":[image_data]}
# 
#     df_1=pd.DataFrame(data)
#     concat_df=pd.concat([df,df_1],axis=1)
#     st.dataframe(concat_df)
# 
#     button_1=st.button("SAVE",use_container_width=True)
#     if button_1:
#       mydb =sqlite3.connect("bizcardx.db")
#       cursor = mydb.cursor()
# 
#       #table creation
#       create_table_query='''CREATE TABLE IF NOT EXISTS bizcard_details(name varchar(300),
#                                                                         designation varchar(300),
#                                                                         company_name varchar(300),
#                                                                         contact varchar(300),
#                                                                         email varchar(300),
#                                                                         website text,
#                                                                         address text,
#                                                                         pincode varchar(300),
#                                                                         image text)'''
# 
#       cursor.execute(create_table_query)
#       mydb.commit()
# 
# 
#       #insert query
#       insert_query='''INSERT INTO bizcard_details(name,designation,company_name,contact,
#                                                     email,website,address,
#                                                     pincode,image)
#                                                     values(?,?,?,?,?,?,?,?,?)'''
#       datas=concat_df.values.tolist()[0]
#       cursor.execute(insert_query,datas)
#       mydb.commit()
#       st.success("SUCCESSFULLY SAVED")
# 
#   method=st.radio("Select the Method:",["None","Preview","Modify"])
#   if method=="None":
#     st.write("")
#   elif method=="Preview":
#     mydb =sqlite3.connect("bizcardx.db")
#     cursor = mydb.cursor()
# 
#     #select query
#     select_query="SELECT * from bizcard_details"
#     cursor.execute(select_query)
#     table=cursor.fetchall()
#     mydb.commit()
# 
#     table_df=pd.DataFrame(table,columns=("NAME","DESIGNATION","COMPANY_NAME","CONTACT","EMAIL",
#                                         "WEBSITE","ADDRESS","PINCODE","IMAGE"))
#     st.dataframe(table_df)
# 
#   elif method=="Modify":
# 
#     mydb =sqlite3.connect("bizcardx.db")
#     cursor = mydb.cursor()
# 
#     #select query
#     select_query="SELECT * from bizcard_details"
#     cursor.execute(select_query)
#     table=cursor.fetchall()
#     mydb.commit()
# 
#     table_df=pd.DataFrame(table,columns=("NAME","DESIGNATION","COMPANY_NAME","CONTACT","EMAIL",
#                                         "WEBSITE","ADDRESS","PINCODE","IMAGE"))
#     col1,col2=st.columns(2)
#     with col1:
# 
#       selected_name=st.selectbox("Select the Name",table_df["NAME"])
# 
#     df_3=table_df[table_df["NAME"]==selected_name]
# 
#     st.dataframe(df_3)
# 
#     df_4=df_3.copy()
# 
#     #col1,col2=st.columns(2)
#     #with col1:
#     modified_name=st.text_input("Name",df_3["NAME"].unique()[0])
#     modified_designation=st.text_input("Designation",df_3["DESIGNATION"].unique()[0])
#     modified_companyname=st.text_input("Company_Name",df_3["COMPANY_NAME"].unique()[0])
#     modified_contact=st.text_input("Contact",df_3["CONTACT"].unique()[0])
#     modified_email=st.text_input("Email",df_3["EMAIL"].unique()[0])
# 
#     df_4["NAME"]=modified_name
#     df_4["DESIGNATION"]=modified_designation
#     df_4["COMPANY_NAME"]=modified_companyname
#     df_4["CONTACT"]=modified_contact
#     df_4["EMAIL"]=modified_email
# 
#     #with col2:
#     modified_website=st.text_input("Website",df_3["WEBSITE"].unique()[0])
#     modified_address=st.text_input("Address",df_3["ADDRESS"].unique()[0])
#     modified_pincode=st.text_input("Pincode",df_3["PINCODE"].unique()[0])
#     modified_image=st.text_input("Image",df_3["IMAGE"].unique()[0])
# 
#     df_4["WEBSITE"]=modified_website
#     df_4["ADDRESS"]=modified_address
#     df_4["PINCODE"]=modified_pincode
#     df_4["IMAGE"]=modified_image
# 
# 
# 
#     button_3=st.button("Modify",use_container_width=True)
#     if button_3:
#       mydb =sqlite3.connect("bizcardx.db")
#       cursor = mydb.cursor()
# 
#       cursor.execute(f"DELETE from bizcard_details where NAME='{selected_name}'")
#       mydb.commit()
# 
#       #insert query
#       insert_query='''INSERT INTO bizcard_details(name,designation,company_name,contact,
#                                                     email,website,address,
#                                                     pincode,image)
#                                                     values(?,?,?,?,?,?,?,?,?)'''
#       datas=df_4.values.tolist()[0]
#       cursor.execute(insert_query,datas)
#       mydb.commit()
#       st.success("SUCCESSFULLY MODIFIED")
#       st.dataframe(df_4)
#       #img2=Image.open()
#       #st.image(img2,width=500)
# elif select=="Delete":
# 
#   mydb =sqlite3.connect("bizcardx.db")
#   cursor = mydb.cursor()
# 
#   col1,col2=st.columns(2)
# 
#   with col1:
#     select_query="SELECT NAME from bizcard_details"
#     cursor.execute(select_query)
#     table1=cursor.fetchall()
#     mydb.commit()
#     names=[]
#     for i in table1:
#       names.append(i[0])
# 
#     name_select=st.selectbox("Select the Name",names)
# 
#   with col2:
#     select_query=f"SELECT DESIGNATION from bizcard_details where NAME='{name_select}'"
#     cursor.execute(select_query)
#     table2=cursor.fetchall()
#     mydb.commit()
#     designations=[]
#     for j in table2:
#       designations.append(j[0])
# 
#     designation_select=st.selectbox("Select the designation",designations)
# 
#   if name_select and designation_select:
# 
#       st.write(f"Selected Name: {name_select}")
# 
#       st.write(f"Selected Designation: {designation_select}")
# 
#       remove=st.button("Delete",use_container_width=True)
#       if remove:
#         cursor.execute(f"DELETE FROM bizcard_details where NAME = '{name_select}' and DESIGNATION = '{designation_select}'")
#         mydb.commit()
# 
#         st.warning("DELETED")
# 
# 
# 
#

!wget -q -O - ipv4.icanhazip.com

! streamlit run bizcard.py & npx localtunnel --port 8501