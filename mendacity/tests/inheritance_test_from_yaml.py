from inheritance import Sample, Family, EvalFamily
import yaml
import inheritance
import sys
import random

def make_ped(yaml_ped):
    """
    Input: 
        Pedigree info from a yaml file containing 'pedigree'
        Obtained using pop from yaml
        Is a nested list containing
    Output:
        A temporary ped file
    """
    ped = open("tmp.ped", 'w')
    header = ['#family_id', 'sample_id', 'paternal_id', 'maternal_id', 'sex', 'phenotype']
    ped.write('\t'.join(header) + "\n")
    for ind in yaml_ped:
        fam_id = 1
        sam_id = ind['id']
        pat_id = 0
        if 'father' in ind.keys():
            pat_id = ind['father']['id']
        mat_id = 0
        if 'mother' in ind.keys():
            mat_id = ind['mother']['id']
        if ind['sex'] == 'male':
            sex = 1
        if ind['sex'] == 'female':
            sex = 2
        if ind['status'] == 'affected':
            pheno = 2
        else:
            pheno = 1
        ind_info = [str(fam_id), str(sam_id), str(pat_id), str(mat_id), str(sex), str(pheno)]
        ped.write('\t'.join(ind_info) + "\n")

yaml_file = sys.argv[1]
y = yaml.load(open(yaml_file))
yaml_ped = y.pop('pedigree')
make_ped(yaml_ped)
fam = Family.from_ped(open("tmp.ped", 'r'))
efam = EvalFamily(fam)
rgtdict = {0: "G/G", 1: "G/A", 2: "A/A", -1: "./."}
for test in y['cases']:
    new_alts = []
    gts = []
    for alt in test['alts'][0]:
        gt = rgtdict[alt]
        gts.append(gt)
        if alt == -1:
            alt = 2
        elif alt == 2:
            alt = 3
        new_alts.append(alt)
    efam.gt_types = new_alts
    print gts, efam.auto_rec(strict=False), efam.auto_rec(strict=True), efam.auto_dom(strict=False), efam.auto_dom(strict=True), efam.de_novo(strict=False), efam.de_novo(strict=True), efam.x_rec(), efam.x_dom(), efam.x_denovo()



