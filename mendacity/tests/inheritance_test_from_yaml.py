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
n = 500
for test in y['cases']:
    new_alts = []
    for alt in test['alts'][0]:
        if alt == -1:
            alt = 2
        elif alt == 2:
            alt = 3
        new_alts.append(alt)
    efam.gt_types = new_alts
    print efam.auto_rec(), efam.auto_dom(), efam.de_novo(), new_alts
#for i in range(n):
#    efam.gt_types = [random.randint(0,3), random.randint(0,3), random.randint(0,3)]
#    print efam.gt_types, "auto_rec", efam.auto_rec(), "auto_dom", efam.auto_dom(), "de_novo", efam.de_novo()

