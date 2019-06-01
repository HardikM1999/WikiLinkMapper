import requests
from bs4 import BeautifulSoup
import sys
import networkx as nx 
import matplotlib.pyplot as plt

#Taking Arguments
#Starting string
start = sys.argv[1]

#No of repetitions
rep = int(sys.argv[2])
tot_list = []

#Creating graph
G = nx.Graph()
G.add_node(start)

#recur function to scrape links
def recur(url,depth,tot_list,parent,rep):
    if(depth<=rep):
        page = requests.get('https://www.wikipedia.org/wiki/' + url)
        #parsing the page
        soup = BeautifulSoup(page.text,'html.parser')
        cnt = 0
        #list for particular depth
        depth_list = []
        for para_tag in soup.select('p'):
            for anchor_tag in para_tag.select('a'):
                if cnt>rep:
                    break
                #getting the link
                check_string = anchor_tag['href']
                if check_string.startswith('#cite') == False and check_string.startswith('/wiki/Help') == False and check_string.startswith('/wiki///en:') == False and check_string.startswith('/wiki/Wikipedia') == False :
                    cnt = cnt + 1
                    depth_list.append(check_string[6:])
            if cnt>rep:
                break
        for link in depth_list:
            tot_list.append((link,parent))  
            recur(link,depth+1,tot_list,link,rep)
    return tot_list


tot_list = recur(start,0,tot_list,start,rep)
node_sizes = []
node_sizes.append(100*len(start))

#Adding tot_list to the graph
for a,b in tot_list:
    G.add_node(a)
    G.add_edge(a,b)
    node_sizes.append(100*len(a))

#Drawing the Graph
nx.draw(G,node_color = 'orange',node_size = node_sizes,with_labels = True)
plt.draw()
plt.show()