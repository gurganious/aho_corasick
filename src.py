# Modification from https://carshen.github.io/data-structures/algorithms/2014/04/07/aho-corasick-implementation-in-python.html

from collections import deque

class Aho_Corasick():
    def __init__(self, keywords):
        self.adj_list = []
        # creates a trie of keywords, then sets fail transitions
        self.create_empty_trie()
        self.add_keywords(keywords)
        self.set_fail_transitions()

    def create_empty_trie(self):
        """ initalize the root of the trie """
        self.adj_list.append({'value':'', 'next_states':[],'fail_state':0,'output':[]})

    def add_keywords(self, keywords):
        """ add all keywords in list of keywords """
        for keyword in keywords:
            self.add_keyword(keyword)

    def find_next_state(self, current_state, value):
        for node in self.adj_list[current_state]["next_states"]:
            if self.adj_list[node]["value"] == value:
                return node
        return None

    def add_keyword(self, keyword):
        """ add a keyword to the trie and mark output at the last node """
        current_state = 0
        j = 0
        keyword = keyword.lower()
        child = self.find_next_state(current_state, keyword[j])
        while child != None:
            current_state = child
            j = j + 1
            if j < len(keyword):
                child = self.find_next_state(current_state, keyword[j])
            else:
                break

        for i in range(j, len(keyword)):
            node = {'value':keyword[i],'next_states':[],'fail_state':0,'output':[]}
            self.adj_list.append(node)
            self.adj_list[current_state]["next_states"].append(len(self.adj_list) - 1)
            current_state = len(self.adj_list) - 1
        self.adj_list[current_state]["output"].append(keyword)

    def set_fail_transitions(self):
        q = deque()
        child = 0
        for node in self.adj_list[0]["next_states"]:
           q.append(node)
           self.adj_list[node]["fail_state"] = 0
        while q:
            r = q.popleft()
            for child in self.adj_list[r]["next_states"]:
                q.append(child)
                state = self.adj_list[r]["fail_state"]
                while (self.find_next_state(state, self.adj_list[child]["value"]) == None
                      and state != 0):
                    state = self.adj_list[state]["fail_state"]
                self.adj_list[child]["fail_state"] = self.find_next_state(state, self.adj_list[child]["value"])
                if self.adj_list[child]["fail_state"] is None:
                    self.adj_list[child]["fail_state"] = 0
                self.adj_list[child]["output"] = self.adj_list[child]["output"] + self.adj_list[self.adj_list[child]["fail_state"]]["output"]

    def get_keywords_found(self, line):
        """ returns keywords in trie from line """
        line = line.lower()
        current_state = 0
        keywords_found = []

        for i, c in enumerate(line):
            while self.find_next_state(current_state, c) is None and current_state != 0:
                current_state = self.adj_list[current_state]["fail_state"]
            current_state = self.find_next_state(current_state, c)
            if current_state is None:
                current_state = 0
            else:
                for j in self.adj_list[current_state]["output"]:
                    yield {"index":i-len(j) + 1,"word":j}
    
    def pattern_found(self, line):
        ''' Returns true when the pattern is found '''
        return next(self.get_keywords_found(line), None) is not None
