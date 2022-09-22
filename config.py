ISSN2BIBSTEM_file = 'newparse/data/issn2bibstem.txt'
ISSN2BIBSTEM = dict()
with open(ISSN2BIBSTEM_file, 'r') as fi:
    for l in fi.readlines():
        (issn, bibstem) = l.strip().split('\t')
        ISSN2BIBSTEM[issn] = bibstem

NAME2BIBSTEM_file = 'newparse/data/name2bibstem.txt'
NAME2BIBSTEM = dict()
with open(NAME2BIBSTEM_file, 'r') as fi:
    for l in fi.readlines():
        (bibstem, name) = l.strip().split('\t')
        NAME2BIBSTEM[name] = bibstem
