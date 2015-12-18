from bs4 import BeautifulSoup
import urllib
import re
#import pickle
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#FOR TESTING
#htmlIn = urllib.urlopen("http://tilde.town/~fr4nk")
#soup=BeautifulSoup(htmlIn,'html.parser')
#text=soup.prettify()
#text = soup.get_text()
#print text

def getUsers():
    htmlIn = urllib.urlopen("http://tilde.town/")
    soup=BeautifulSoup(htmlIn,'html.parser')
    
    userL = '/~'
    tildeList = []
    for link in soup.find_all('a'):
        if re.search(userL,link.get('href')):
            tildeList.append( link.get('href'))
            
    return tildeList
      
userPageSet = []
userPageSplit = []
userList = []
for idx, user in enumerate(getUsers()):
    if re.search('http',user) is None:
        userList.append(user)        
        
        userUrl = "http://tilde.town" + user
        htmlIn = urllib.urlopen(userUrl)
        soup = BeautifulSoup(htmlIn,'html.parser')
        
        #clean user pages here for special characters such as \n or \t        
        
        userPageSet.append( soup.get_text() )
        userPageSplit.append(userPageSet[-1].split())
         
        print idx, user

#get basic word counts
wordcounts = []
for page in userPageSplit:
    wordcounts.append(len(page))



wcountdf = pd.DataFrame({'users': userList, 'words': wordcounts})
wcountdf = wcountdf.drop_duplicates()
wcountdf = wcountdf.sort(['words'],ascending=[0])

wcountTop = wcountdf[:10]

sns.barplot(x = "words", y = "users", data = wcountTop)
plt.title('Most Verbose Users')
plt.xlabel('# of words scraped from page')


#for page in userPageSet:
#    
#
#print userPageSet

# Saving the objects:
#with open('userPageSet.pickle', 'w') as f:
#    pickle.dump([userPageSet], f)

# Getting back the objects:
#with open('userPageSet.pickle') as f:
#    userPageSet = pickle.load(f)
