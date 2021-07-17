import spacy

from nl_to_lf import doc_i_lemma

nlp = spacy.load('en_core_web_trf')
doc = nlp("The scope and impact of this cultural change have received some attention, but no attempt has yet been made to understand its basic mechanism.")

full_span = doc[0:]
fs_root = full_span.root
i_lem = ""
i_lem = doc_i_lemma(fs_root, i_lem)   

    