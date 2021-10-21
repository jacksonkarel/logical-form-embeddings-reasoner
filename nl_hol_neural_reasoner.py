import argparse

from proposition import Proposition 

nlr_parser = argparse.ArgumentParser(description='Translate a natural language sentence to a higher-order logical form and add it to an Isabelle theory')

nlr_parser.add_argument('I_file',
                    metavar='isabelle',
                    type=str,
                    help='isabelle file output')

args = nlr_parser.parse_args()

I_path = args.I_file

test_prop = Proposition()
test_prop.i_path = I_path
test_prop.str_i_lemma()