class GraphShow():
    """"Create demo page"""
    def __init__(self, fullPath,events,TranslateJ2E=False, TranslateE2J=False):
        from googletrans import Translator 
        self.TranslateJ2E = TranslateJ2E
        self.TranslateE2J = TranslateE2J
        self.translate =Translator()
        self.events = events
        self.fullPath = fullPath
        self.data_nodes = []
        self.data_edges =[]
        fb = open('basefile.txt','r')
        self.base = fb.read()


    

    def create_page(self):
        # import re
        """Read data"""
        nodes = []
        if self.TranslateJ2E == True:
            for i, event in enumerate (self.events):
                event[0] = self.translate.translate(str(event[0]), src='ja', dest='en').text
                event[1] = self.translate.translate(str(event[1]), src='ja', dest='en').text
                self.events[i] = event 
                nodes.append(event[0])
                nodes.append(event[1])
        elif self.TranslateE2J == True:
            for i, event in enumerate (self.events):
                event[0] = self.translate.translate(str(event[0]), src='en', dest='ja').text
                event[1] = self.translate.translate(str(event[1]), src='en', dest='ja').text
                self.events[i] = event 
                nodes.append(event[0])
                nodes.append(event[1])
        else:
            for event in self.events:
                nodes.append(event[0])
                nodes.append(event[1])
        node_dict = {node: index for index, node in enumerate(nodes)}

        for node, id in node_dict.items():
            data = {}
            data["group"] = 'Event'
            data["id"] = id
            data["label"] = node
            self.data_nodes.append(data)

        for edge in self.events:
            data = {}
            data['from'] = node_dict.get(edge[0])
            data['label'] = ''
            data['to'] = node_dict.get(edge[1])
            
            self.data_edges.append(data)

        self.create_html()
        return

    def create_html(self):
       
        """Generate html file"""
#         filepath = Path(filePath)
#         fullPath= filepath/filename
        f = open(self.fullPath, 'w+')
        print(self.fullPath)
        print("!")
        html = self.base.replace('data_nodes', str(self.data_nodes)).replace('data_edges',str(self.data_edges)).replace("\ufb02","")
        f.write(html)
        f.close()
#         f = open('graph_show.html', 'w+')
#         html = self.base.replace('data_nodes', str(data_nodes)).replace('data_edges', str(data_edges))
#         f.write(html)
#         f.close()
