import re

import spacy

def i_var_format(arg_par, i_lem, parenthesis="("):
    arg_par = re.sub("\.|,|-", "_", arg_par)
    i_lem = i_lem + arg_par.lower() + parenthesis
    return i_lem

def i_concat_children(token, i_lem):
    child_deps = [child.dep_ for child in token.children]
    noun_deps = ["det", "nummod", "amod", "nmod", "advmod", "poss", "appos", "prep", "acl", "relcl", "cc", "conj"]
    dep_i_var_dict = {
        "ADP": ["pobj", "cc", "conj"],
        "NOUN": noun_deps,
        "PRON": noun_deps,
        "VERB": ["neg", "aux", "auxpass", "advmod", "npadvmod", "ccomp", "acomp", "xcomp", "prep", "mark", "nsubj", "nsubjpass", "dobj", "pobj", "agent", "advcl", "cc", "conj"],
        "ADJ": ["advmod", "amod", "cc", "conj"],
        "ADV": ["advmod", "prep"],
        "AUX": ["neg", "acomp", "xcomp", "attr", "nsubj"],
        "DET": ["prep", "pobj"]
    }
    il_vars = [key for key in dep_i_var_dict]
    non_vars = ["punct", "compound"]
    dep_in_vars = token.pos_ in il_vars
    if dep_in_vars:
        dep_i_vars = dep_i_var_dict[token.pos_]
        expected_vars = dep_i_vars + non_vars
        for idx, i_var in enumerate(dep_i_vars):
            for child in token.children:
                if child.dep_ not in expected_vars:
                    print("New token type:", child.text, child.dep_)
                if child.dep_ == i_var:
                    if idx != 0:
                        i_lem = i_lem + ", "
                    i_lem = doc_i_lemma(child, i_lem)
            if i_var not in child_deps:
                if idx == 0:
                    i_lem = i_lem + "None" 
                else:
                    i_lem = i_lem + ", None"
                
    elif token.dep_ not in non_vars:
        print("New token type:", token.text, token.pos_, token.dep_)

    i_lem = i_lem + ")"
    return i_lem

def doc_i_lemma(token, i_lem):
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

def str_i_lemma(text):
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(text)
    full_span = doc[0:]
    fs_root = full_span.root
    i_lem = ""
    i_lem = doc_i_lemma(fs_root, i_lem)
    return i_lem