import re

import spacy

def i_var_format(arg_par, i_lem, parenthesis="("):
    arg_par = re.sub("\.|,|-", "_", arg_par)
    i_lem = i_lem + arg_par.lower() + parenthesis
    return i_lem

def check_none(idx, i_lem):
    if idx == 0:
        i_lem = i_lem + "None" 
    else:
        i_lem = i_lem + ", None"
    return i_lem

def i_concat_children(token, i_lem):
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
                i_lem = check_none(idx, i_lem)
            for child in token.children:
                if child.dep_ == i_var:
                    if child.dep_ == "punct" and child.text in [".", ",", ":", "!", ";"]:
                        i_lem = check_none(idx, i_lem)
                    else: 
                        if idx != 0:
                            i_lem = i_lem + ", "
                        i_lem = token_i_lemma(child, i_lem)

    i_lem = i_lem + ")"
    return i_lem

def token_i_lemma(token, i_lem):
    if token.n_rights + token.n_lefts == 0:
        arg_name = f"{token.text}_{token.pos_}"
        i_lem = i_var_format(arg_name, i_lem, "")
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
            i_lem = i_var_format(pred_name, i_lem, "")
        else:
            i_lem = i_var_format(pred_name, i_lem)      
            i_lem = i_concat_children(token, i_lem)
    elif token.dep_ not in ["nummod"]:
        pred_name = f"{token.text}_{token.pos_}"
        i_lem = i_var_format(pred_name, i_lem)
        i_lem = i_concat_children(token, i_lem)
    return i_lem

def ecw_trf_doc(text):
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(text)
    return doc

def doc_i_lemma(doc):
    full_span = doc[0:]
    fs_root = full_span.root
    i_lem = ""
    i_lem = token_i_lemma(fs_root, i_lem)
    return i_lem

def str_i_lemma(text):
    doc = ecw_trf_doc(text)
    i_lem = doc_i_lemma(doc)