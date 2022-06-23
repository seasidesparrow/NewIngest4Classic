from pyingest.config.config import *
from bs4 import BeautifulSoup
import re

fix_ampersand = re.compile(r"(&amp;)(.*?)(;)")

class ParserException(Exception):
    pass

class Translator(object):
    '''
    translates an ingest data model (dict) object into something approximating
    what gets passed to the serializer for an ADS Classic Tagged record
    '''

    # INITIALIZATION
    def __init__(self, data=None, **kwargs):
        self.data = data
        self.output = dict()
        return

    # DETAGGER (from jats.py)
    def _detag(self, r, tags_keep, **kwargs):

        newr = BeautifulSoup(str(r), 'lxml')
        try:
            tag_list = list(set([x.name for x in newr.find_all()]))
        except Exception as err:
            tag_list = []
        for t in tag_list:
            elements = newr.findAll(t)
            for e in elements:
                if t in JATS_TAGS_DANGER:
                    e.decompose()
                elif t in tags_keep:
                    e.contents
                else:
                    if t.lower() == 'sc':
                        e.string = e.string.upper()
                    e.unwrap()

        # Note: newr is converted from a bs4 object to unicode here.
        # Everything after this point is string manipulation.

        newr = str(newr)

        amp_fix = fix_ampersand.findall(newr)
        for s in amp_fix:
            s_old = ''.join(s)
            s_new = '&' + s[1] + ';'
            newr = newr.replace(s_old, s_new)

        newr = newr.replace(u'\n', u' ').replace(u'  ', u' ')
        newr = newr.replace('&nbsp;', ' ')

        return newr

    # TITLE
    def _get_title(self):
        title = self.data.get('title', None)
        if title:
            title_en = title.get('textEnglish', None)
            title_tn = title.get('textNative', None)
            title_ln = title.get('langNative', None)
            if title_en:
                self.output['title'] = title_en
            else:
                if title_tn:
                    self.output['title'] = title_tn
                    self.output['language'] = title_ln


    # INDIVIDUAL NAME
    def _get_name(self, name):
        surname = name.get('surname', None)
        given_name = name.get('given-name', None)
        middle_name = name.get('middle-name', None)
        pubraw = name.get('pubraw', None)
        collab = name.get('collab', None)
        outname = None
        if surname:
            outname = surname
            if given_name:
                outname = outname + ', ' + given_name
                if middle_name:
                    outname = outname + ' ' + middle_name
        return outname

    # INDIVIDUAL AFFIL
    def _get_affil(self, contrib):
        attribs = contrib.get('attrib', None)
        affil = contrib.get('affiliation', None)
        affarray = []
        if affil:
            for a in affil:
                aff = a.get('affPubRaw', None)
                if aff:
                    affarray.append(aff)
        if attribs:
            orcid = attribs.get('orcid', None)
            if orcid:
                orcid = '<ID system="ORCID">' + orcid + '</ID>'
                affarray.append(orcid)
            email = attribs.get('email', None)
        else:
            orcid = None
            email = None

        outaffil=None
        if affarray:
            outaffil = '; '.join(affarray)
            if email:
                email = '<EMAIL>' + email + '</EMAIL>'
                outaffil = outaffil + ' ' + email
        return outaffil
            

    # ALL CONTRIB (NAME & AFFIL)
    def _get_auths_affils(self):
        authors = self.data.get('authors', None)
        if authors:
            author_list = list()
            affil_list = list()
            for a in authors:
                # person
                name = a.get('name', None)
                if name:
                    # person name
                    auth = self._get_name(name)
                # person attribs and affil
                aff = self._get_affil(a)
                author_list.append(auth)
                affil_list.append(aff)
            self.output['authors'] = author_list
            self.output['affiliations'] = affil_list


    # ABSTRACT
    def _get_abstract(self):
        abstract = self.data.get('abstract', None)
        if abstract:
            abstract_raw = abstract.get('textEnglish', None)
        tagset = JATS_TAGSET['abstract'] or None
        self.output['abstract'] = self._detag(abstract_raw, tagset)


    def _get_keywords(self):
        keywords = self.data.get('keywords', None)
        keyword_list = []
        for k in keywords:
            keyw = k.get('keyString', None)
            if keyw:
                keyword_list.append(keyw)
        if keyword_list:
            self.output['keywords'] = ', '.join(keyword_list)


    def _get_date(self):
        pubdate = self.data.get('pubDate', None)
        date = pubdate.get('printDate', None)
        if not date:
            date = pubdate.get('electrDate', None)
        if date:
            self.output['pubdate'] = date


    def _get_references(self):
        references = self.data.get('references', None)
        if references:
            self.output['refhandler_list'] = references


    def _get_pubdat(self):
        # This is where you send the data to get %R and %J
        self.output['publication'] = 'lol'
        self.output['bibcode'] = 'wut'
        


    def translate(self, data=None):
        if not self.data:
            raise ParserException('You need to supply data to translate!')
        else:
            self._get_title()
            self._get_abstract()
            self._get_keywords()
            self._get_auths_affils()
            self._get_pubdat()
            self._get_date()
            self._get_references()
