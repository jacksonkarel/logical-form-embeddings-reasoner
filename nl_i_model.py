import re

import spacy

def i_var_format(name, i_lem, parenthesis="("):
    name_format = re.sub("\W", "_", name)
    i_lem = i_lem + name_format.lower() + parenthesis
    return i_lem

def doc_i_lemma(token, i_lem):
    if token.n_rights + token.n_lefts == 0:
        i_lem = i_var_format(token.text, i_lem, "")
    elif token.pos_ == "VERB":
        func_name = token.text
        for child in token.children:
            if child.dep_ == "aux":
                func_name = f"{child.text}_{func_name}"
        i_lem = i_var_format(func_name, i_lem)      
        for child in token.children:
            if child.dep_ not in ["conj", "aux"]:
                i_lem = doc_i_lemma(child, i_lem)
    else:
        i_lem = i_var_format(token.text, i_lem)
        for idx, child in enumerate(token.children):
            if idx != 0:
                i_lem = i_lem + ", "
            i_lem =  doc_i_lemma(child, i_lem)
        i_lem = i_lem + ")"
    return i_lem

nlp = spacy.load('en_core_web_trf')
doc = nlp("In the last twenty-five years, thousands of people have reported the persistent appearances of UFO phenomena.")

full_span = doc[0:]
i_lem = ""
fs_root = full_span.root
i_lem = doc_i_lemma(fs_root, i_lem)

        

    