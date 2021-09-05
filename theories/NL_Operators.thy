section \<open>Natural Language Operators\<close>

theory NL_Operators
  imports Main
begin

lemma "((\<forall> a1. is_aux(a1, None) \<longrightarrow> \<not>is_aux(a1, not_part)) \<and>
is_aux(change, None))
\<longrightarrow> \<not>is_aux(change, not_part)"
  by auto

lemma "((\<forall> a1 a2. means_verb(a1, a2) \<longrightarrow>  a1 = a2) \<and>
means_verb(cat, feline))
\<longrightarrow> cat = feline"
  by auto


end