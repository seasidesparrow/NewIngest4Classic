from habanero import Crossref
from pyingest.serializers import classic
import json


class CrossrefHarvestError(Exception):
    pass


class EmptyBodyError(Exception):
    pass


class DOIHarvester(object):

    def __init__(self):
        pass

    def harvest(self, doi=None):
        try:
            cr = Crossref(mailto="ads@cfa.harvard.edu", ua_string="NASA ADS @ Harvard.edu")
            doi_meta_json = cr.works(ids=doi)
        except Exception as err:
            raise CrossrefHarvestError(err)
        else:
            return doi_meta_json


class CrossrefJSONParser(object):

    def __init__(self):
        pass

    def parse(self, xref_json=None):
        if xref_json:
            output_metadata = dict()
            # The record is already a json object, but it has a different
            # structure than our IngestDataModel.  You need a translator to
            # turn this into a record to pass to 
            # pyingest.serializers.classic.Tagged
            # similar to newparse.translator
            # MAKE A JAZZ NOISE HERE.
            output_metadata['NOISE'] = 'JAZZ'

            return output_metadata
        else:
            raise EmptyBodyError('No data to parse.')


def main():

    # Plos ONE example from Habanero docs
    # doi = '10.1371/journal.pone.0033693'

    # MDPI Galaxies -- has abstract
    doi = '10.3390/galaxies9040111'

    # PNAS volume 1 paper (1915)
    # doi = '10.1073/pnas.1.1.51'

    try:
        x = DOIHarvester()
        foo = x.harvest(doi)
        # uncomment next line to see the raw return from crossref
        #print(foo)

        # uncomment next line to see return from crossref, but rendered nicely
        #print(json.dumps(foo, sort_keys=True, indent=4))

        # uncomment next 3 lines to see what would happen if you write
        # something for the JSON parser (in place of jazz noises...)
        translate = CrossrefJSONParser()
        output_dictionary = translate.parse(foo)
        print('Output dictionary: %s' % output_dictionary)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()

