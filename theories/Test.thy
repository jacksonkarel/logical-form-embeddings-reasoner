section \<open>Test\<close>

theory Test
  imports Main
begin

lemma "(\<forall>e f g. is_aux(e, g, f(g, the_det)) \<longrightarrow>  e = f(g, the_det)) \<and>
e \<noteq> None \<and>
is_aux(change_noun, param1, actualization_noun(param1, the_det)) \<and>
is_aux(change_noun, None, feature_noun(real_adj, a_det, of_adp(world_noun(None, the_det, None, None)))) \<and>
change_noun(hello)
\<longrightarrow> is_aux(actualization_noun(param1, the_det), None, feature_noun(real_adj, a_det, of_adp(world_noun(None, the_det, None, None))))"
  by auto


end

  

  