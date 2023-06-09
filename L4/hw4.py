import sys
from collections import deque
import pandas as pd

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            # Find the titles without "_".
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        # Initialize the link count.
        for id in self.titles.keys():
            link_count[id] = 0

        # self.titles = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F'}
        # self.titles.key() = [1, 2, 3, 4, 5, 6]
        # self.links = {1: [2], 2: [3, 4], 3: [1, 2, 5, 6], 4: [2, 5, 6], 5: [4], 6: [3]}
        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Get the key from the value(title).
    #
    # |val|: The title of the page.
    def get_key_from_value(self, val):
        for key, value in self.titles.items():
            if val == value:
                return key
        return False
    
    
    # Find the shortest path.
    #
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_key = self.get_key_from_value(start)
        goal_key = self.get_key_from_value(goal)
        if not start_key or not goal_key or start_key == goal_key:
            print("Invalid input")
            print()
            return
        # Use deque for the queue.
        queue = deque()
        visited = {}
        # Save the path. e.g. {"B":"A", "C":"B", "D":"B"}  A->B->D
        path = {}
        visited[start_key] = True
        queue.append(start_key)
        # BFS
        while len(queue) > 0:
            # Deque from the queue.
            node = queue.popleft()
            for child in self.links[node]:
                # If the child is not visited, then add it to the queue.
                if not child in visited:
                    visited[child] = True
                    queue.append(child)
                    # Save the path {child: node}
                    path[child] = node
                # If the child is the goal key, then print the path.
                if child == goal_key:
                    # Get the path in correct order.
                    ans = []
                    ans.append(goal_key)
                    while path[child] != start_key:
                        ans.append(path[child])
                        child = path[child]
                    ans.append(start_key)
                    ans.reverse()
                    # Print the path.
                    print("The shortest path is:\n",[self.titles[i] for i in ans])
                    print()
                    return
        print("Not found")
        print()
    
  
    # Calculate the page ranks and print the top 10 popular pages.
    def find_most_popular_pages(self):
        # Initialize the page ranks to 1. (Use key of self.titles)
        ranks = {key: 1 for key in self.titles.keys()}
        prev_sum = 0
        for i in range(10):
            # Initialize the update page ranks to 0.
            update_ranks = {key: 0 for key in self.titles.keys()}
            nolink_keys = []
            for key in ranks:
                # If the page has no linked page, then add the page rank to the nolink_keys.
                if len(self.links[key]) == 0:
                    nolink_keys.append(ranks[key])
                else:
                    # Distribute the 85% of the page rank to the linked pages.
                    for dst in self.links[key]:
                        update_ranks[dst] += 0.85 * ranks[key] / len(self.links[key])
            # Calculate the 15% of the page rank (sum of all page ranks - sum of nolink_keys) per page.
            with_link =  0.15 * (sum(ranks.values()) - sum(nolink_keys))
            # Calculate the 100% of the page rank (sum of nolink_keys) per page.
            no_link = 1.0 * sum(nolink_keys)
            # Distribute them to all pages.
            for key in ranks:
                update_ranks[key] += (with_link + no_link) / len(ranks)
            # Update the page ranks.
            ranks = update_ranks
            current_sum = sum(ranks.values())
            # If the sum of the page ranks is not changed, then finish the iteration.
            if abs(current_sum - prev_sum) < 1e-4: # 0.0001
                break
            prev_sum = current_sum
        # Sort the page ranks and get the top 10.
        s = pd.Series(ranks)
        sorted = s.sort_values(ascending=False)
        max_rank_keys = sorted.head(10).index
        print("The most popular pages are (Top 10):")
        j = 1
        for i in max_rank_keys:
            print(j,":",self.titles[i])
            j += 1
        print()

    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass 

# python3 hw4.py wikipedia_dataset/pages_small.txt wikipedia_dataset/links_small.txt
# python3 hw4.py wikipedia_dataset/pages_medium.txt wikipedia_dataset/links_medium.txt
# python3 hw4.py wikipedia_dataset/pages_large.txt wikipedia_dataset/links_large.txt
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    if sys.argv[1] == "wikipedia_dataset/pages_small.txt":
        wikipedia.find_shortest_path("A", "D")
        wikipedia.find_shortest_path("A", "B")
        wikipedia.find_shortest_path("C", "E")
        wikipedia.find_shortest_path("B", "E")
        wikipedia.find_shortest_path("D", "A")
        wikipedia.find_shortest_path("E", "A")
        wikipedia.find_shortest_path("E", "E") # Invalid input
        wikipedia.find_shortest_path("G", "A") # Invalid input
    else:
        wikipedia.find_shortest_path("渋谷", "小野妹子")
        wikipedia.find_shortest_path("渋谷", "HUNTER×HUNTER")
        wikipedia.find_shortest_path("数学", "コンブ")
    wikipedia.find_most_popular_pages()
