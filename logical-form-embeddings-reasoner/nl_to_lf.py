import re

import spacy

def i_var_format(arg_par, i_data, parenthesis="("):
    arg_par = re.sub("\.|,|-", "_", arg_par)
    i_data["lemma"] = i_data["lemma"] + arg_par.lower() + parenthesis
    return i_data

def check_none(idx, t, i_data, dep_i_vars):
    i_lem = i_data["lemma"]
    i_data["epvc"] = i_data["epvc"] + 1
    epvc = i_data["epvc"]
    if idx == 0:
        i_data["lemma"] = f"{i_lem}{t.text}_v{epvc}"
    else:
        i_data["lemma"] = f"{i_lem}, {t.text}_v{epvc}"
    # if i_data["child level"] >= 3:
    #     for i_var in dep_i_vars:

    return i_data

def i_concat_children(token, i_data):
    child_deps = [child.dep_ for child in token.children]
    
    dep_i_vars = ["acl", "acomp", "advcl", "advmod", "agent", "amod", "appos", "attr", "aux", "auxpass", "case", "cc", 
    "ccomp", "conj", "csubj", "csubjpass", "dative", "dep", "det", "dobj", "expl", "intj", "mark", "meta", 
    "neg", "nmod", "npadvmod", "nsubj", "nsubjpass", "nummod", "oprd", "parataxis", "pcomp", "pobj", "poss", "preconj", 
    "predet", "prep", "prt", "punct", "quantmod", "relcl", "xcomp"]
    
    il_vars = ["ADJ", "ADP", "ADV", "AUX", "CONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", "PUNCT", 
    "SCONJ", "SYM", "VERB"]

    if token.pos_ in il_vars:
        for idx, i_var in enumerate(dep_i_vars):
            if i_var not in child_deps:
                i_data = check_none(idx, token, i_data)
            i_data["child level"] = i_data["child level"] + 1
            for child in token.children:
                if child.dep_ == i_var:
                    if child.dep_ == "punct" and child.text in [".", ",", ":", "!", ";"]:
                        i_data = check_none(idx, token, i_data)
                    else: 
                        if idx != 0:
                            i_data["lemma"] = i_data["lemma"] + ", "
                        i_data = token_i_lemma(child, i_data)

    i_data["lemma"] = i_data["lemma"] + ")"
    return i_data

def token_i_lemma(token, i_data):
    if token.n_rights + token.n_lefts == 0:
        pred_name = f"{token.text}_{token.pos_}"
        i_data = i_var_format(pred_name, i_data, "")
            
    elif token.pos_ in ["NOUN", "NUM"]:
        word_concat_map = {
            "NOUN": "compound",
            "NUM": "compound"
        }
        pred_name = token.text
        for child in token.children:
            if child.dep_ == word_concat_map[token.pos_]:
                pred_name = f"{child.text}_{pred_name}"
        pred_name = f"{pred_name}_{token.pos_}"
        if token.dep_ in ["nummod"]:
            i_data = i_var_format(pred_name, i_data, "")
        else:
            i_data = i_var_format(pred_name, i_data)      
            i_data = i_concat_children(token, i_data)
    elif token.dep_ not in ["nummod"]:
        pred_name = f"{token.text}_{token.pos_}"
        i_data = i_var_format(pred_name, i_data)
        i_data = i_concat_children(token, i_data)
    return i_data

def ecw_trf_doc(text):
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(text)
    return doc

def doc_i_lemma(doc):   
    
    # class root_node():
    #     def __init__(self):
    #         self.children = []
    
    # def ancestors_are_parents(node, parent):
    #     if parent != start:
    #         parent.children.append(node)
    #         ancestors_are_parents(node, parent.parent)
            

    # class i_var():
    #     def __init__(self, name, parent):
    #         self.name = name
    #         self.children = [] 
    #         ancestors_are_parents(self, parent)
    
    # def i_graph(parent, dep_i_vars, counter):
    #     if counter <= 3:
    #         for dep in tqdm(dep_i_vars):
    #             dep_node = i_var(dep, parent)
    #             i_graph(dep_node, dep_i_vars, counter)
    #             counter = counter + 1
    
    # start = root_node()
    # counter = 0
    # i_graph(start, dep_i_vars, counter)
    # print(start.children)
    lvl_counter = 0
    i_data = {
        "lemma": {
            "root node": {
                "dep": "ROOT",
                "children": [],
                "grand children": []
            }
        },
        "dep vars": ["acl", "acomp", "advcl", "advmod", "agent", "amod", "appos", "attr", "aux", "auxpass", "case", "cc", 
    "ccomp", "conj", "csubj", "csubjpass", "dative", "dep", "det", "dobj", "expl", "intj", "mark", "meta", 
    "neg", "nmod", "npadvmod", "nsubj", "nsubjpass", "nummod", "oprd", "parataxis", "pcomp", "pobj", "poss", "preconj", 
    "predet", "prep", "prt", "punct", "quantmod", "relcl", "xcomp"],
        "var counter": {}
    }
    for var in i_data["dep vars"]:
        i_data["var counter"][var] = 0
    i_data = i_graph(i_data, "root node")
    full_span = doc[0:]
    fs_root = full_span.root
    i_data["lemma"]["root node"]["name"] = f"{fs_root.text}_{fs_root.pos_}"
    t_root_children = fs_root.children
    var_root_children = i_data["lemma"]["root node"]["children"]
    i_data = token_i_dict(t_root_children, var_root_children, i_data, lvl_counter, None)

def token_i_dict(t_children, var_children, i_data, lvl_counter, parent):
    for token in t_children:
        for var in var_children:
            if lvl_counter >= 2:
                i_data = i_graph(i_data, lvl_counter, parent)
            if i_data["lemma"][var]["dep"] == token.dep_ and not (token.dep_ == "punct" and token.text in [".", ",", ":", "!", ";"]):
                pred_name = f"{token.text}_{token.pos_}"
                if token.pos_ in ["NOUN", "NUM", "PROPN"]:
                    pred_name = token.text
                    for child in token.children:
                        if child.dep_ == "compound":
                            pred_name = f"{child.text}_{pred_name}"
                    pred_name = f"{pred_name}_{token.pos_}"
                i_data["lemma"][var]["name"] = pred_name
                if token.n_rights + token.n_lefts > 0:
                    next_lvl_counter = lvl_counter + 1
                    i_data = token_i_dict(token.children, i_data["lemma"][var]["children"], i_data, next_lvl_counter, var)
                
    return i_data



    

    # i_data = token_i_lemma(fs_root, i_data)
    # return i_data

def i_graph(i_data, lvl_counter, parent):
    for dep in i_data["dep vars"]:
        key = f"{dep}_{i_data['var counter'][dep]}"
        i_data["var counter"][dep] = i_data["var counter"][dep] + 1
        i_data["lemma"][key] = {
            "name": key,
            "dep": dep,
            "parents": [parent]
        }
        i_data["lemma"][parent]["children"].append(key)
        i_data["lemma"][parent]["grand children"].append(key)
        if lvl_counter >= 1:
            for grand_parent in i_data["lemma"][parent]["parents"]:
                i_data["lemma"][key]["parents"].append(grand_parent)
                i_data["lemma"][grand_parent]["grand children"].append(key)
        if lvl_counter <= 1:
            i_data["lemma"][key]["children"] = []
            i_data["lemma"][key]["grand children"] = []
            next_lvl_counter = lvl_counter + 1
            i_data = i_graph(i_data, next_lvl_counter, key)
    return i_data

def str_i_lemma(text):
    doc = ecw_trf_doc(text)
    i_data = doc_i_lemma(doc)