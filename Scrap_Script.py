def doctor_links(city,Specialist,i):
    doc_links=set()
    url=f"https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22{Specialist}%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city={city}&page={i}"
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    info = soup.find_all("div",class_="info-section")
    for j in info:
        try:
            doc_links.add("https://www.practo.com/"+j.find("a").get("href"))
        except:
            pass
    return doc_links
def extract_info(k,soup):
    l=[]
    key_class={"Name":"c-profile__title","Experience":"h2","Qualification":"c-profile__details","Speciality":"u-d-inlineblock","Votes":"u-smallest-font","fee":"u-f-right","dp_score":"u-green-text"}
    key_tags={"Name":"h1","Experience":"h2","Qualification":"p","Speciality":"h2","Votes":"span","fee":"span","dp_score":"span"}
    if k=="Experience":
        for j in soup.find_all(key_tags[k]):
            l.append(j.text)
        try:
            for k in l:
                if "Years Experience Overall" in k:
                    return int(k[:2])
        except:
            return np.NaN
    elif k=="Speciality":
        try:
            return soup.find_all(key_tags[k],class_="u-d-inlineblock")[2].text
        except:
            return np.NaN
    elif k=="fee":
        try:
            return soup.find_all(key_tags[k],class_="u-f-right")[-1].text
        except:
            return np.NaN        
    else:        
        try:
            return soup.find(key_tags[k],class_=key_class[k]).text
        except:
            return np.NaN

if __name__ == "__main__":
	
	from bs4 import BeautifulSoup
	import requests
	import re
	import numpy as np
	import pandas as pd
	city=input("Enter city to fetch doctors from that city\n")
	Specialist=input("Enter doctor speciality\n")
	n=int(input("Enter no of pages to scrap\n"))
	s=set()
	for i in range(1,n+1):
	    strrs=doctor_links(city,Specialist,i)
	    s=s.union(strrs)
	    break
	dictt={"Name":[],"Experience":[],"Qualification":[],"Speciality":[],"Votes":[],'fee':[],'dp_score':[]}
	for i in s:
	    r=requests.get(i)
	    soup=BeautifulSoup(r.text,"html.parser")
	    for k in dictt:
	        dictt[k].append(extract_info(k,soup))  
df=pd.DataFrame(dictt)
print(df)      