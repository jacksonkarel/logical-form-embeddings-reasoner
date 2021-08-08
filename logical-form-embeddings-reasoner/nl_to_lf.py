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
        child_level = i_data["child level"]
        if 0 < child_level >= 3:
            i_data["higher pred idx"][child_level] = len(i_data["lemma"]) - 1
            
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
    full_span = doc[0:]
    fs_root = full_span.root
    i_data = {
        "lemma": "",
        "epvc": 0,
        "child level": 0,
        "higher pred idx": [0, 0, 0],
        "dep vars": ["acl", "acomp", "advcl", "advmod", "agent", "amod", "appos", "attr", "aux", "auxpass", "case", "cc", 
    "ccomp", "conj", "csubj", "csubjpass", "dative", "dep", "det", "dobj", "expl", "intj", "mark", "meta", 
    "neg", "nmod", "npadvmod", "nsubj", "nsubjpass", "nummod", "oprd", "parataxis", "pcomp", "pobj", "poss", "preconj", 
    "predet", "prep", "prt", "punct", "quantmod", "relcl", "xcomp"]
    }
    i_data = token_i_lemma(fs_root, i_data)
    return i_data

def str_i_lemma(text):
    doc = ecw_trf_doc(text)
    i_data = doc_i_lemma(doc)