import spacy

class Proposition:
    def __init__(self):
        self.data = {
            "root node": {
                "dep": "ROOT",
                "children": [],
            }
        }
        self.dep_vars = ["acl", "acomp", "advcl", "advmod", "agent", "amod", "appos", "attr", "aux", "auxpass", "case", "cc", 
"ccomp", "conj", "csubj", "csubjpass", "dative", "dep", "det", "dobj", "expl", "intj", "mark", "meta", 
"neg", "nmod", "npadvmod", "nsubj", "nsubjpass", "nummod", "oprd", "parataxis", "pcomp", "pobj", "poss", "preconj", 
"predet", "prep", "prt", "punct", "quantmod", "relcl", "xcomp", "compound"]
        self.var_counter = {}
        self.logical_form = ""
        self.i_path = ""

    def ecw_trf_doc(self, text):
        nlp = spacy.load('en_core_web_trf')
        doc = nlp(text)
        return doc

    def str_i_lemma(self):
        for var in self.dep_vars:
            self.var_counter[var] = 0
        text = input("Enter your text: ")
        doc = self.ecw_trf_doc(text)
        full_span = doc[0:]
        fs_root = full_span.root
        self.data["root node"]["name"] = f"{fs_root.text}_{fs_root.pos_}"
        stack = [("root node", fs_root)]
        for node in stack:
            token = node[1]
            node_key = node[0]
            for dep in self.dep_vars:
                key = f"{dep}_{self.var_counter[dep]}"
                for child in token.children:
                    if dep == child.dep_ and not (child.dep_ == "punct" and child.text in [".", ",", ":", "!", ";"]):
                        pred_name = f"{child.text}_{child.pos_}"
                        self.data[key] = {
                            "name": pred_name.lower()
                        }
                        if child.n_rights + child.n_lefts > 0:
                            stack.append((key, child))
                if key not in self.data:
                    self.data[key] = {
                        "name": "None"
                    }
                self.data[key]["dep"] = dep
                self.data[key]["children"] = []
                self.var_counter[dep] = self.var_counter[dep] + 1  
                self.data[node_key]["children"].append(key)

        self.data_to_lf(self.data["root node"])
        # thy_end = '"\n  by auto\n\n\nend'
        i_and = " \<and> "
        self.join_lf(i_and)
        self.append_i_file()

    def data_to_lf(self, node):
        self.join_lf(node["name"])
        if len(node["children"]) > 0:
            self.join_lf("(")
            for idx, child in enumerate(node["children"]):
                self.data_to_lf(self.data[child])
                if idx + 1 < len(node["children"]):
                    self.join_lf(", ")
            self.join_lf(")")

    def join_lf(self, lf_part):
        self.logical_form = "".join((self.logical_form, lf_part))
        
    def append_i_file(self):
        i_file = open(self.i_path, "a")  
        i_file.write(self.logical_form)