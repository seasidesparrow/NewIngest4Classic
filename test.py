from adsingestp.parsers import jats
from newparse.translator import Translator
from pyingest.serializers.classic import Tagged
import json



infiles=['test.xml']
documents=[]

for f in infiles:
    try:
        with open(f, 'rb') as fx:
            data = fx.read()
    except Exception as err:
        print("problem with %s: %s" % (f, err))
    else:
        try:
            lol = jats.JATSParser()
            output = lol.parse(data)
            with open('test.json','w') as fj:
                fj.write(json.dumps(output, indent=2, sort_keys=True))
        except Exception as err:
            print("Well, fuck.... %s" % err)
        else:
            trans = Translator(data=output)
            trans.translate()
            documents.append(trans.output)


for d in documents:
    x = Tagged()
    with open('test.tag','a') as fw:
        try:
            x.write(trans.output, fw)
        except Exception as err:
            print('serializer problem... %s' % err)


