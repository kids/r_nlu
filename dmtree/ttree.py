# -*- coding: utf-8 -*-

class Node(dict):
    def __init__(self, key, l_name='', weight=0):#, kwargs=None):
        self.key = key
        self.l_names = []
        self.weight = weight
        if l_name:
            self.l_names.append(l_name)

    def __str__(self):
        return '<Node key:{} names:{} Subnodes: {}>'.format(
                    self.key, self.l_names, self.items())

    def add_subnode(self, node):
        self.update({node.key: node})

    def get_subnode(self, key):
        return self.get(key)

    def has_subnode(self):
        return len(self) > 0

    def get_top_node(self, prefix):
        top = self
        for k in prefix:
            top = top.get_subnode(k)
            if top is None:
                return None
        return top


    def depth_walk(self, node):
        # return candidates with same prefix
        result = []
        
        if len(node) > 0:
            for k in node.keys():
                s = self.depth_walk(node.get(k))
                result.extend([(k + subkey, snode) for subkey, snode in s])
            return result
        if node.l_names:
            result=[('', node)]
            return result


    def search(self, prefix, limit=None, is_case_sensitive=False):

        result = []
        nd=self

        if nd is None:
            print('None root')
            return result
        
        for ch in range(len(prefix)):
            nd = nd.get_subnode(prefix[ch]) # last node of prefix
            if nd is None:
                return result
            if nd.l_names:
                result.append((prefix[:ch+1],nd))

        if limit:
            result = [(prefix + subkey, pnode) for subkey, pnode in self.depth_walk(nd)]
            result.sort(key=lambda x: x[1].weight, reverse=True)
            result = result[:limit] if limit is not None else result

        return result


    def add(self, keyword, l_name, weight=0, **kwargs):
        one_node = self

        index = 0
        last_index = len(keyword) - 1
        for c in keyword:
            if c not in one_node:
                if index != last_index:
                    one_node.add_subnode(Node(c, weight=weight))
                else:
                    one_node.add_subnode(Node(c, l_name=l_name, weight=weight)) #kwargs=kwargs
                one_node = one_node.get_subnode(c) 
            else:
                one_node = one_node.get_subnode(c)

                if index == last_index:
                    if l_name not in one_node.l_names:
                        one_node.l_names.append(l_name)
                    one_node.weight = weight
#                     for key, value in kwargs.items():
#                         setattr(one_node, key, value)
            
            index += 1

        
    def delete(self, keyword, l_name):
        if not keyword:
            return

        top_node = self.get_top_node(keyword)
        if top_node is None:
            return
            
        if l_name in top_node.l_names:
            top_node.l_names.remove(l_name)
            return 1


