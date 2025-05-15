# friend_groups.py
import json, sqlite3, time, random, pathlib
from instagrapi import Client
import networkx as nx
from networkx.algorithms.community import louvain_communities
from tqdm import tqdm

USERNAME = input("Your Instagram @username: ")
PASSWORD = input("Your Instagram password (hidden): ")

sess_file = pathlib.Path("session.json")
cl = Client()
if sess_file.exists():
    cl.load_settings(str(sess_file))
cl.login(USERNAME, PASSWORD)
if not sess_file.exists():        
    sess_file.write_text(json.dumps(cl.get_settings()))


my_id = cl.user_id_from_username(USERNAME)
friends = cl.user_following(my_id, amount=0)           


G = nx.Graph()
for p in friends.values():
    G.add_node(p.pk, username=p.username, name=p.full_name)

print("\nScanning overlap among your followees (this can take 5-10 min)...")
for a_id, a_prof in tqdm(friends.items()):

    a_following = set(cl.user_following(a_id, amount=150).keys())
    for b_id in friends.keys():
        if a_id < b_id and b_id in a_following:
            G.add_edge(a_id, b_id, weight=1)
    time.sleep(2 + 2*random.random())  


groups = louvain_communities(G, weight="weight", resolution=1.0)
group_of = {uid: idx for idx, g in enumerate(groups) for uid in g}


bridges = [uid for uid, score in nx.betweenness_centrality(G).items() if score > 0.03]

out = pathlib.Path("bridges.txt").open("w", encoding="utf-8")
for uid in bridges:
    p = friends[uid]
    connected_groups = sorted({group_of[n] for n in G[uid]})
    out.write(f"{p.username:25}  links groups {connected_groups}\n")
out.close()
print("\nDone!  Open 'bridges.txt' in TextEdit or any text editor to see who links your friend groups.")


