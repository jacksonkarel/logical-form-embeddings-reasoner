import spacy
from spacy import displacy
from tqdm import tqdm

def ecw_trf_doc(text):
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(text)
    return doc

def str_i_lemma():
    for var in dep_vars:
        var_counter[var] = 0
    text = input("Enter your text: ")
    doc = ecw_trf_doc(text)
    doc_to_data(doc)
    data_to_lf(data["root node"])
    thy_end = '"\n  by auto\n\n\nend'
    append_i_file(thy_end)
    
    
def append_i_file(thy_part):
    i_file = open("Equality_Test.thy", "a")  
    i_file.write(thy_part)

def data_to_lf(node):
    append_i_file(node["name"])
    if len(node["grand children"]) > 0:
        append_i_file("(")
        for idx, grand_child in enumerate(tqdm(node["grand children"])):
            if grand_child in node["children"]:
                data_to_lf(data[grand_child])
            else:
                append_i_file(data[grand_child]["name"])
            if idx + 1 < len(node["grand children"]):
                append_i_file(", ")
            append_i_file(")")
        
def doc_to_data(doc):   
    lvl_counter = 0
    i_graph(lvl_counter, "root node")
    full_span = doc[0:]
    fs_root = full_span.root
    data["root node"]["name"] = f"{fs_root.text}_{fs_root.pos_}"
    t_root_children = fs_root.children
    var_root_children = data["root node"]["children"]
    token_i_dict(t_root_children, var_root_children, lvl_counter, None)

def token_i_dict(t_children, var_children, lvl_counter, parent):
    for token in t_children:
        for var in var_children:
            if lvl_counter >= 2:
                i_graph(lvl_counter, parent)
            if data[var]["dep"] == token.dep_ and not (token.dep_ == "punct" and token.text in [".", ",", ":", "!", ";"]):
                pred_name = f"{token.text}_{token.pos_}"
                if token.pos_ in ["NOUN", "NUM", "PROPN"]:
                    pred_name = token.text
                    for child in token.children:
                        if child.dep_ == "compound":
                            pred_name = f"{child.text}_{pred_name}"
                    pred_name = f"{pred_name}_{token.pos_}"
                data[var]["name"] = pred_name
                if token.n_rights + token.n_lefts > 0:
                    next_lvl_counter = lvl_counter + 1
                    token_i_dict(token.children, data[var]["children"], next_lvl_counter, var)

def i_graph(lvl_counter, parent):
    for dep in dep_vars:
        key = f"{dep}_{var_counter[dep]}"
        add_edges(dep, key, parent)
        if lvl_counter <= 1:
            next_lvl_counter = lvl_counter + 1
            i_graph(next_lvl_counter, key)

def add_edges(dep, key, parent):
    var_counter[dep] = var_counter[dep] + 1
    data[key] = {
        "name": "None",
        "dep": dep,
        "parents": [parent]
    }
    data[parent]["children"].append(key)
    data[parent]["grand children"].append(key)
    data[key]["children"] = []
    data[key]["grand children"] = []
    if "parents" in data[parent]:
        for grand_parent in data[parent]["parents"]:
            data[key]["parents"].append(grand_parent)
            data[grand_parent]["grand children"].append(key)

dep_vars = ["acl", "acomp", "advcl", "advmod", "agent", "amod", "appos", "attr", "aux", "auxpass", "case", "cc", 
"ccomp", "conj", "csubj", "csubjpass", "dative", "dep", "det", "dobj", "expl", "intj", "mark", "meta", 
"neg", "nmod", "npadvmod", "nsubj", "nsubjpass", "nummod", "oprd", "parataxis", "pcomp", "pobj", "poss", "preconj", 
"predet", "prep", "prt", "punct", "quantmod", "relcl", "xcomp"]

data = {
        "root node": {
            "dep": "ROOT",
            "children": [],
            "grand children": []
        }
    }
var_counter = {}

str_i_lemma()