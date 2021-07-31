from spacy import displacy

from nl_to_lf import ecw_trf_doc, doc_i_lemma

# while True:
text = input("Enter your text: ")
doc = ecw_trf_doc(text)
i_data = doc_i_lemma(doc)
i_lem = i_data["lemma"]
print(i_lem)
    # displacy.serve(doc, style="dep")