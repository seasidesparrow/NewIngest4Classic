from adsingestp.parsers import arxiv, crossref, datacite, jats
from newparse.translator import Translator
from pyingest.serializers.classic import Tagged
import json


def load_file(filename):
    try:
        with open(filename, 'rb') as fx:
            data = fx.read()
    except Exception as err:
        print("error loading file: %s" % err)
    else:
        return data


def main():
    infiles=['../VOR_10.1119_10.0009409.xml']
    filetype = 'jats'
    publisher = 'aip'
    documents=[]

    for f in infiles:
        data = load_file(f)
        if data:
            if filetype == 'arxiv':
                parser = arxiv.ArxivParser()
            elif filetype == 'crossref':
                parser = crossref.CrossrefParser()
            elif filetype == 'datacite':
                parser = datacite.DataciteParser()
            elif filetype == 'jats':
                parser = jats.JATSParser()
            else:
                parser = None

            if parser:
                parsed = parser.parse(data)
                if parsed:
                    with open('test.json','w') as fj:
                        fj.write(json.dumps(parsed, indent=2, sort_keys=True))
                    xlator = Translator(data=parsed)
                    xlator.translate()
                    documents.append(xlator.output)
        else:
            print("No useful data from %s, skipping..." % f)

    for d in documents:
        x = Tagged()
        with open('test.tag','a') as fw:
            try:
                x.write(d, fw)
            except Exception as err:
                print('serializer problem... %s' % err)


if __name__ == '__main__':
    main()
