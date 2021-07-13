import re

import spacy

def i_parameter(t, i_lem, parenthesis="("):
    arg_par = f"{t.dep_}={t.text}"
    i_lem = i_var_format(arg_par, i_lem, parenthesis)
    return i_lem

def i_var_format(arg_par, i_lem, parenthesis="("):
    arg_par = re.sub("\.|,|-", "_", arg_par)
    i_lem = i_lem + arg_par.lower() + parenthesis
    return i_lem

def i_first_param_idx(first_param_idx, idx):
    if idx == 0:
        first_param_idx = 1
    return first_param_idx

def i_concat_children(token, i_lem):
    conjs = []
    first_param_idx = 0
    for idx, child in enumerate(token.children):
        if child.dep_ == "conj":
            conjs.append(child)
            first_param_idx = i_first_param_idx(first_param_idx, idx) 
        elif child.dep_ not in ["aux", "punct", "det"]:
            if idx != first_param_idx:
                i_lem = i_lem + ", "
            i_lem = doc_i_lemma(child, i_lem)
        else:
            first_param_idx = i_first_param_idx(first_param_idx, idx)

    i_lem = i_lem + ")"
    return i_lem

def doc_i_lemma(token, i_lem):
    if token.n_rights + token.n_lefts == 0:
        i_lem = i_parameter(token, i_lem, "")
    elif token.pos_ == "VERB":
        func_name = token.text
        for child in token.children:
            if child.dep_ == "aux":
                func_name = f"{child.text}_{func_name}"
        if token.dep_ not in ["ROOT"]:
            func_name = f"{token.dep_}={func_name}" 
        i_lem = i_var_format(func_name, i_lem)      
        i_lem = i_concat_children(token, i_lem)
    else:
        i_lem = i_parameter(token, i_lem)
        i_lem = i_concat_children(token, i_lem)
    return i_lem

nlp = spacy.load('en_core_web_trf')
doc = nlp("In the last twenty-five years, thousands of people have reported the persistent appearances of UFO phenomena.")

full_span = doc[0:]
i_lem = ""
fs_root = full_span.root
i_lem = doc_i_lemma(fs_root, i_lem)        

    