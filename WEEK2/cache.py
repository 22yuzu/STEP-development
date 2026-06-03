import random, sys
import hash_table # Use the hash table you implemented in Homework #2

###########################################################################
#                                                                         #
# Implement a cache that stores the most recently accessed items from     #
# scratch!                                                                #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

class Page:
    def __init__(self, url, contents):
        # URL
        self.url = url
        # The contents of the URL
        self.contents = contents
        # Previous page
        self.prev = None
        # Next page
        self.next = None

        
class Cache:
    # Initialize the cache.
    # 'limit': The size limit of the cache.
    def __init__(self, limit):
        assert(limit >= 1)
        self.limit = limit
        self.hit_count = 0 # Increment on a cache hit
        #アクセスしたurlがcacheに入ってないこと
        self.miss_count = 0 # Increment on a cache miss
        self.hash_table = hash_table.HashTable()
        #dummyノードを作るメリットとしては、追加と削除が楽になる（先頭・末尾・空を考えなくて良い）
        self.head = Page("", "")  #dummy head, newest
        self.tail = Page("", "")  #dummy tail, oldest 
        #何もないから初期化
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    # Access a page and update the cache so that it stores the most recently
    # accessed pages up to the 'limit'. This needs to be done with mostly O(1).
    # 'url': The accessed URL
    # 'contents': The contents of the URL
    def access_page(self, url, contents):
        node, if_found = self.hash_table.get(url)
        #そのページがキャッシュにあったら
        if if_found: 
            self.hit_count += 1
            # remove the node
            node.prev.next = node.next
            node.next.prev = node.prev  
            # move the node to the head
            node.prev = self.head
            node.next = self.head.next
            self.head.next.prev = node
            self.head.next = node   
            return
        # Cache miss
        self.miss_count += 1
        node_new = Page(url, contents)
        node_new.prev = self.head
        node_new.next = self.head.next
        # move the node to the head
        self.head.next.prev = node_new
        self.head.next = node_new
        self.hash_table.put(url, node_new)
        self.size += 1
        #リミットを超えた場合には一番古い（tailにいるやつ）を消さないといけない
        if self.size > self.limit:
            old_url = self.tail.prev.url #save the URL before removing the node
            self.tail.prev.prev.next = self.tail
            self.tail.prev = self.tail.prev.prev
            self.hash_table.delete(old_url)
            self.size -= 1
        return


    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    #headからtailに一つずつ追加していくだけ
    def get_pages(self): #Why do we need this function??
        pages_list = []
        node = self.head.next   
        while node != self.tail:
            pages_list.append(node.url)
            node = node.next
        return pages_list


    # Return the cache hit rate.
    def get_hitrate(self):
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0

    
def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (new)<-- "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (new)<-- "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (new)<-- "d.com", "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (new)<-- "d.com", "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (new)<-- "a.com", "d.com", "c.com", "b.com" -->(old)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (new)<-- "e.com", "a.com", "c.com", "d.com" -->(old)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (new)<-- "f.com", "e.com", "a.com", "c.com" -->(old)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (new)<-- "e.com", "f.com", "a.com", "c.com" -->(old)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (new)<-- "a.com", "e.com", "f.com", "c.com" -->(old)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


def performance_test():
    # Set the size of the cache to 100.
    cache = Cache(100)

    # Generate queries based on the Zipf law.
    ALPHA = 1.5
    NUM_QUERIES = 1000000
    NUM_PAGES = 1000
    ranks = range(1, NUM_PAGES + 1)
    weights = [1.0 / (r ** ALPHA) for r in ranks]
    random.seed(1)
    queries = random.choices(ranks, weights=weights, k=NUM_QUERIES)    
    for query in queries:
        cache.access_page(str(query), "")

    # If your cache implementation is correct, the hit rate will be 91%.
    print("Cache hit rate = %d %%" % (cache.get_hitrate() * 100))
    print("Performance tests passed!")


if __name__ == "__main__":
    cache_test()
    performance_test()