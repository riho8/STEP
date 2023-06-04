import sys
from collections import deque

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
            if titles[index].find("_") == -1: #! これどういうこと?
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

    #! 追加
    def get_key_from_value(self, val):
        for key, value in self.titles.items():
            if val == value:
                return key
        return "Key not found"
    
    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_key = self.get_key_from_value(start)
        goal_key = self.get_key_from_value(goal)
        queue = deque()
        visited = {}
        path = {}
        get_shortest = False
        visited[start_key] = True
        queue.append(start_key)
        while len(queue) > 0:
            node = queue.popleft()
            if node == goal_key:
                get_shortest = True
                break 
            for child in self.links[node]:
                if not child in visited:
                    visited[child] = True
                    queue.append(child)
                    path[child] = node
                if child == goal_key:
                    get_shortest = True
                    break
            if get_shortest == True:
                break
        if get_shortest == True:
            ans = []
            ans.append(goal_key)
            while path[child] != start_key:
                ans.append(path[child])
                child = path[child]
            ans.append(start_key)
            ans.reverse()
            print("The shortest path is:\n",[self.titles[i] for i in ans])
        else:
            print("Not found")
        return


 


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass #! 何も実行しないときに書く


    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass

# python3 hw4-1.py wikipedia_dataset/pages_small.txt wikipedia_dataset/links_small.txt
# python3 hw4-1.py wikipedia_dataset/pages_medium.txt wikipedia_dataset/links_medium.txt
# python3 hw4-1.py wikipedia_dataset/pages_large.txt wikipedia_dataset/links_large.txt
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    if sys.argv[1] == "wikipedia_dataset/pages_small.txt":
        wikipedia.find_shortest_path("A", "F")
        wikipedia.find_shortest_path("A", "B")
        wikipedia.find_shortest_path("C", "E")
        wikipedia.find_shortest_path("B", "E")
    else:
        wikipedia.find_shortest_path("渋谷", "小野妹子")
    wikipedia.find_most_popular_pages()
