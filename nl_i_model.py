import re

import spacy

def i_var_format(arg_par, i_lem, parenthesis="("):
    arg_par = re.sub("\.|,|-", "_", arg_par)
    i_lem = i_lem + arg_par.lower() + parenthesis
    return i_lem

def i_concat_children(token, i_lem):
    conjs = []
    child_deps = [child.dep_ for child in token.children]
    nonpobj_params = ["relcl", "det", "nummod", "amod", "prep"]
    dep_i_param_dict = {
        "prep": ["pobj"],
        "pobj": ["det", "nummod", "amod"],
        "nsubj": nonpobj_params,
        "nsubjpass": nonpobj_params,
        "dobj": nonpobj_params,
        "ccomp": ["aux", "auxpass", "advmod", "prep", "nsubj", "nsubjpass", "dobj"],
        "amod": ["advmod"],
        "acomp": ["advmod"],
        "relcl": ["aux", "auxpass", "advmod", "ccomp", "acomp", "prep", "nsubj", "nsubjpass", "dobj"]
    }
    il_params = [key for key in dep_i_param_dict]
    non_params = ["aux", "punct", "compound", "mark", "conj", "cc"]
    root_verb = token.dep_ == "ROOT" and token.pos_ == "VERB"
    dep_in_params = token.dep_ in il_params
    if root_verb or dep_in_params:
        if root_verb:
            dep_i_params = ["aux", "auxpass", "advmod", "ccomp", "acomp", "prep", "nsubj", "nsubjpass", "dobj"]
        else:
            dep_i_params = dep_i_param_dict[token.dep_]
        expected_params = dep_i_params + non_params
        for idx, param in enumerate(dep_i_params):
            for child in token.children:
                if child.dep_ not in expected_params:
                    print("New token type:", child.text, child.dep_)
                if child.dep_ == param:
                    if idx != 0:
                        i_lem = i_lem + ", "
                    i_lem = doc_i_lemma(child, i_lem)
            if param not in child_deps:
                if idx == 0:
                    i_lem = i_lem + "None" 
                else:
                    i_lem = i_lem + ", None"
                
    elif token.dep_ not in non_params:
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
        func_name = token.text
        for child in token.children:
            if child.dep_ == word_concat_map[token.pos_]:
                func_name = f"{child.text}_{func_name}"
        func_name = f"{func_name}_{token.pos_}"
        if token.dep_ in ["nummod"]:
            i_lem = i_var_format(func_name, i_lem, "")
        else:
            i_lem = i_var_format(func_name, i_lem)      
            i_lem = i_concat_children(token, i_lem)
    elif token.dep_ not in ["nummod"]:
        func_name = f"{token.text}_{token.pos_}"
        i_lem = i_var_format(func_name, i_lem)
        i_lem = i_concat_children(token, i_lem)
    return i_lem

nlp = spacy.load('en_core_web_trf')
doc = nlp("A careful examination of the patterns of these reports has already shown that they follow definite laws for which no explanation has been found.")

full_span = doc[0:]
i_lem = ""
fs_root = full_span.root
i_lem = doc_i_lemma(fs_root, i_lem)
print(i_lem)        

    