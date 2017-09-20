from os.path import join
import os
import random

ROOT_DIR = join(os.path.dirname(os.path.abspath(__file__)), '../../../')
ROOT_DIR2 = '/home/roys/work/deep_srl/'
EFS_DIR = "/net/efs/aristo/dlfa/roys/science-terms/glove.6B.100/"
EFS_DIR2 = "/net/efs/aristo/dlfa/roys/embeddings/"
MED_OUTPUT_DIR = "/home/roys/corpora/scientific/medline/hinged/merged/"

RANDOM_SEED = 12345
random.seed(RANDOM_SEED)

SRL_CONLL_EVAL_SCRIPT  = join(ROOT_DIR, 'scripts/run_eval.sh')
WORD_EMBEDDINGS = { "glove50": join(ROOT_DIR2, 'data/glove/glove.6B.50d.txt'),
                    "glove100": join(ROOT_DIR2, 'data/glove/glove.6B.100d.txt'),
                    "glove200": join(ROOT_DIR2, 'data/glove/glove.6B.200d.txt'),
                    "dsrl_medline_50_lc_10_100_hinged_g0.2_l0.00005_C0.1_0.5_0.3": join(MED_OUTPUT_DIR, 'dsrl_medline_50_lc_10_100_hinged_g0.2_l0.00005_C0.1_merged_0.5_0.3.dat'),
                    "dsrl_medline_50_lc_10_100_hinged_g0.2_l0.00005_C0.1_-1_-1": join(MED_OUTPUT_DIR, 'dsrl_medline_50_lc_10_100_hinged_g0.2_l0.00005_C0.1_merged_-1_-1.dat'),
                    "glove100_medline_50_lc_10_100_hinged_g0.2_l0.00005_C0.1_merged_-1_-1": join(MED_OUTPUT_DIR, 'glove100_medline_50_lc_10_100_hinged_g0.2_l0.00005_C0.1_merged_-1_-1.dat')
                    }

START_MARKER  = '<S>'
END_MARKER    = '</S>'
UNKNOWN_TOKEN = '*UNKNOWN*'
UNKNOWN_LABEL = 'O'
#UNKNOWN_FEATURE = 'FEAT_NONE'

TEMP_DIR = join(ROOT_DIR, 'temp')

assert os.path.exists(SRL_CONLL_EVAL_SCRIPT)
if not os.path.exists(TEMP_DIR):
  os.makedirs(TEMP_DIR)

