import re

import spacy

def i_var_format(arg_par, i_lem, parenthesis="("):
    arg_par = re.sub("\.|,|-", "_", arg_par)
    i_lem = i_lem + arg_par.lower() + parenthesis
    return i_lem

def i_concat_children(token, i_lem):
    conjs = []
    child_deps = [child.dep_ for child in token.children]
    nonpobj_vars = ["det", "nummod", "amod", "prep"]
    dep_i_var_dict = {
        "prep": ["pobj"],
        "pobj": ["det", "nummod", "amod", "prep"],
        "nsubj": nonpobj_vars,
        "nsubjpass": nonpobj_vars,
        "dobj": nonpobj_vars,
        "ccomp": ["aux", "auxpass", "advmod", "prep", "nsubj", "nsubjpass", "dobj"],
        "amod": ["advmod"],
        "acomp": ["advmod"],
        "relcl": ["aux", "auxpass", "advmod", "ccomp", "acomp", "prep", "nsubj", "nsubjpass", "dobj"],
        "aux": ["neg", "acomp"]
    }
    il_vars = [key for key in dep_i_var_dict]
    non_vars = ["aux", "punct", "compound", "mark", "conj", "cc"]
    root_verb = token.dep_ == "ROOT" and token.pos_ == "VERB"
    dep_in_vars = token.dep_ in il_vars
    if root_verb or dep_in_vars:
        if root_verb:
            dep_i_vars = ["aux", "auxpass", "advmod", "ccomp", "acomp", "prep", "nsubj", "nsubjpass", "dobj"]
        else:
            dep_i_vars = dep_i_var_dict[token.dep_]
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

    for idx, child in enumerate(token.children):
        if child.dep_ == "cc":
            conjs.append(child) 
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

nlp = spacy.load('en_core_web_trf')
doc = nlp("These statistical facts have been adequately documented elsewhere and will not concern us here.")

full_span = doc[0:]
fs_root = full_span.root
i_lem = ""
i_lem = doc_i_lemma(fs_root, i_lem)
for token in fs_root.children:
    if token.dep_ == "cc":
        ands = ("and", "but", "yet", "as")
        ors = ("or")
        cc_mapping = {
            ands: "\<and>",
            ors: "\<or>"
        }

    