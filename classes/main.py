class TreeStore:
    def __init__(self, items):
        self.items = {}
        self.initItems(items)
        self.tree = {}
        self.makeTree()
        pass

    # Чтобы быстро найти дочерние элементы
    def makeTree(self):
        for i in self.items.keys():
            el = self.items[i]
            if(not el['parent'] in self.tree.keys()):
                self.tree[el['parent']] = [el['id']]
                continue
            self.tree[el['parent']].append(el['id'])
        pass

    # Чтобы найти элемент по id
    def initItems(self, items):
        for item in items:
            self.items[item['id']] = item
        pass

    def getAll(self):
        return self.items
    
    def getItem(self, id):
        return self.items[id]
    
    def getChildren(self, id):
        res = []
        if(not id in self.tree.keys()):
            return res
        for el in self.tree[id]:
            res.append(self.items[el])
        return res
    
    def getAllParents(self, id):
        res = []
        while(self.items[id]['parent'] in self.items.keys()):
            id = self.items[id]['parent']
            res.append(self.items[id])

        return res
            

items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]
ts = TreeStore(items)

# Примеры использования:
print(ts.getAll())
# [{"id":1,"parent":"root"},{"id":2,"parent":1,"type":"test"},{"id":3,"parent":1,"type":"test"},{"id":4,"parent":2,"type":"test"},{"id":5,"parent":2,"type":"test"},{"id":6,"parent":2,"type":"test"},{"id":7,"parent":4,"type":None},{"id":8,"parent":4,"type":None}]

print(ts.getItem(7))
# {"id":7,"parent":4,"type":None}

print(ts.getChildren(4))
# [{"id":7,"parent":4,"type":None},{"id":8,"parent":4,"type":None}]
print(ts.getChildren(5))
# []

print(ts.getAllParents(7))
# [{"id":4,"parent":2,"type":"test"},{"id":2,"parent":1,"type":"test"},{"id":1,"parent":"root"}]