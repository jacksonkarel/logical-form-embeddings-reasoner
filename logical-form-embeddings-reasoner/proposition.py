import spacy
from spacy import displacy

class Proposition:
    def __init__(self):
        self.data = {
            "root node": {
                "dep": "ROOT",
                "children": [],
                "grand children": []
            }
        }
        self.dep_vars = ["acl", "acomp", "advcl", "advmod", "agent", "amod", "appos", "attr", "aux", "auxpass", "case", "cc", 
    "ccomp", "conj", "csubj", "csubjpass", "dative", "dep", "det", "dobj", "expl", "intj", "mark", "meta", 
    "neg", "nmod", "npadvmod", "nsubj", "nsubjpass", "nummod", "oprd", "parataxis", "pcomp", "pobj", "poss", "preconj", 
    "predet", "prep", "prt", "punct", "quantmod", "relcl", "xcomp"]
        self.var_counter = {}
        self.logical_form = ""
    
    def ecw_trf_doc(text):
        nlp = spacy.load('en_core_web_trf')
        doc = nlp(text)
        return doc

    def str_i_lemma(self, text):
        doc = self.ecw_trf_doc(text)
        self.doc_to_data(doc)
        self.data_to_lf(self.data["root node"])

    def print_lf(self):
        for var in self.dep_vars:
            self.var_counter[var] = 0
        text = input("Enter your text: ")
        doc = self.ecw_trf_doc(text)
        self.doc_to_data(doc)
        self.data_to_lf(self.data["root node"])
        print(self.logical_form)
        # displacy.serve(doc, style="dep")

    def data_to_lf(self, node):
        self.logical_form = "".join((self.logical_form, node["name"]))
        if len(node["grand children"]) > 0:
            self.logical_form = "".join((self.logical_form, "("))
            for idx, grand_child in enumerate(node["grand children"]):
                if grand_child in node["children"]:
                    self.data_to_lf(self.data[grand_child])
                else:
                    self.logical_form = "".join((self.logical_form, self.data[grand_child]["name"]))
                if idx + 1 < len(node["grand children"]):
                    self.logical_form = "".join((self.logical_form, ", "))
            self.logical_form = "".join((self.logical_form, ")"))
            
    def doc_to_data(self, doc):   
        lvl_counter = 0
        self.i_graph(lvl_counter, "root node")
        full_span = doc[0:]
        fs_root = full_span.root
        self.data["root node"]["name"] = f"{fs_root.text}_{fs_root.pos_}"
        t_root_children = fs_root.children
        var_root_children = self.data["root node"]["children"]
        self.token_i_dict(t_root_children, var_root_children, lvl_counter, None)

    def token_i_dict(self, t_children, var_children, lvl_counter, parent):
        for token in t_children:
            for var in var_children:
                if lvl_counter >= 2:
                    self.i_graph(lvl_counter, parent)
                if self.data[var]["dep"] == token.dep_ and not (token.dep_ == "punct" and token.text in [".", ",", ":", "!", ";"]):
                    pred_name = f"{token.text}_{token.pos_}"
                    if token.pos_ in ["NOUN", "NUM", "PROPN"]:
                        pred_name = token.text
                        for child in token.children:
                            if child.dep_ == "compound":
                                pred_name = f"{child.text}_{pred_name}"
                        pred_name = f"{pred_name}_{token.pos_}"
                    self.data[var]["name"] = pred_name
                    if token.n_rights + token.n_lefts > 0:
                        next_lvl_counter = lvl_counter + 1
                        self.token_i_dict(token.children, self.data[var]["children"], next_lvl_counter, var)

    def i_graph(self, lvl_counter, parent):
        for dep in self.dep_vars:
            key = f"{dep}_{self.var_counter[dep]}"
            self.add_edges(dep, key, parent)
            if lvl_counter <= 1:
                next_lvl_counter = lvl_counter + 1
                self.i_graph(next_lvl_counter, key)

    def add_edges(self, dep, key, parent):
        self.var_counter[dep] = self.var_counter[dep] + 1
        self.data[key] = {
            "name": key,
            "dep": dep,
            "parents": [parent]
        }
        self.data[parent]["children"].append(key)
        self.data[parent]["grand children"].append(key)
        self.data[key]["children"] = []
        self.data[key]["grand children"] = []
        if "parents" in self.data[parent]:
            for grand_parent in self.data[parent]["parents"]:
                self.data[key]["parents"].append(grand_parent)
                self.data[grand_parent]["grand children"].append(key)