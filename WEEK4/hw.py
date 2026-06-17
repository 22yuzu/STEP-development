import sys
import collections
import collections

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

    # ヘルパー関数：タイトルからIDを探す
    def get_id_from_title(self, title):
        for id, page_title in self.titles.items():
            if page_title == title:
                return id
        return None

    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        id_start = self.get_id_from_title(start)
        id_goal = self.get_id_from_title(goal)
        # if start or goal page does not exist
        if id_start is None:
            print("Start page not found:", start)
            print()
            return
        if id_goal is None:
            print("Goal page not found:", goal)
            print()
            return
        queue = collections.deque([id_start])
        visited = collections.deque([id_start])
        parent = {}
        found = False
        while queue:
            curr = queue.popleft()
            if curr == id_goal:
                found = True
                break
            links = self.links[curr]
            for link in links:
                if link not in visited:
                    visited.append(link)
                    parent[link] = curr
                    queue.append(link)
        # if there is no path from start to goal
        if not found:
            print("No path found from %s to %s" % (start, goal))
            print()
            return
        # restore the path using parent after finding the goal
        path = []
        curr = id_goal
        while curr != id_start:
            path.append(curr)
            curr = parent[curr]
        path.append(id_start)
        path.reverse()
        # print the path as page titles
        print("Shortest path from %s to %s:" % (start, goal))
        for id in path:
            print(self.titles[id])
        print()

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        pagerank = {}
        for id in self.titles.keys():
            pagerank[id] = 1.0
        n = len(self.titles)
        diff = 1.0
        while diff >= 0.01:
            new_pagerank = {}
            for id in self.titles.keys():
                new_pagerank[id] = 0.0
            no_link_rank = 0.0 # the total pagerank of pages with no outgoing links
            total_rank = 0.0 # the total pagerank of all pages
            for id in self.titles.keys():
                total_rank += pagerank[id]
            for id in self.titles.keys():
                if len(self.links[id]) == 0:
                    no_link_rank += pagerank[id]
            # normal pages distribute 15% to all pages, and pages with no links 
            # distribute 100% to all pages
            original_rank = (0.15 * total_rank + 0.85 * no_link_rank) / n
            for id in self.titles.keys():
                new_pagerank[id] = original_rank
            # if the page has outgoing links
            for id in self.titles.keys():
                links = self.links[id]
                if len(links) > 0:
                    rank_to_give = 0.85 * pagerank[id] / len(links)
                    for dst in links:
                        new_pagerank[dst] += rank_to_give
            diff = 0.0
            for id in self.titles.keys():
                diff += (new_pagerank[id] - pagerank[id]) ** 2
            pagerank = new_pagerank
        # sort pages by pagerank in descending order
        pages = sorted(self.titles.keys(), key=lambda id: pagerank[id], reverse=True)
        print("The most popular pages are:")
        count = 0
        for id in pages:
            if count >= 10:
                break
            print(self.titles[id], pagerank[id])
            count += 1
        print()

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])
        visited = {}
        for node in path:
            assert(node not in visited)
            visited[node] = True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("A", "F")
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_shortest_path("Google", "長崎")
    wikipedia.find_shortest_path("東京", "経路積分")
    wikipedia.find_shortest_path("カンボジア", "船橋")
    wikipedia.find_shortest_path("渋谷", "渋谷")
    wikipedia.find_shortest_path("", "渋谷")
    wikipedia.find_shortest_path("渋谷", "")
    wikipedia.find_shortest_path("fhoarffdhi", "ejrofvhisa")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")