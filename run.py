from adsingestp.parsers import jats
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
    infiles=['test.xml']
    filetype = 'jats'
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
