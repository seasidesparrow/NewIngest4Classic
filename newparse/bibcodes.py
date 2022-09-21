import string
import json

class BibstemException(Exception):
    pass

class NoPubYearException(Exception):
    pass

class NoBibcodeException(Exception):
    pass

class Bibcode(object):

    def __init__(self, bibstem=None, issn2bibstem=None, name2bibstem=None):
        self.issn2bibstem = issn2bibstem
        self.name2bibstem = name2bibstem
        self.bibstem = bibstem

    def _int_to_letter(integer):
        try:
            return string.ascii_letters[integer - 1]
        except:
            return integer

    def _get_author_init(self, record):
        try:
            author_init = record['authors'][0]['name']['surname'][0]
        except Exception as err:
            author_init = '.'
        return author_init

    def _get_pubyear(self, record):
        try:
            pub_year = record['publication']['pubYear']
        except Exception as err:
            raise NoPubYearException(err)
        else:
            return pub_year

    def _get_volume(self, record):
        try:
            volume = record['publication']['volumeNum']
            volume = volume
        except Exception as err:
            volume = None
        return volume

    def _get_issue(self, record):
        try:
            issue_meta = record['publication']['issueNum']
            issue = self._int_to_letter(int(issue_meta))
        except Exception as err:
            issue = None
        return issue

    def _get_pagenum(self, record):
        pagination = record.get('pagination', None)
        if pagination:
            fpage = pagination.get('firstPage', None)
            epage = pagination.get('electronicID', None)
            rpage = pagination.get('pageRange', None)
            if fpage:
                page = fpage
            elif epage:
                page = epage
            elif rpage:
                page = rpage
            else:
                page = None
            if page:
                is_letter = False
                page_a = None
                if len(page) >= 6:
                    page = page[-6:]
                    page_a = self._int_to_letter(page[0:2])
                if 'L' in page:
                    page = page.replace('L', '.')
                    is_letter = True
                if page_a:
                    page = page_a + page[2:]

                    
        return page, is_letter

    def _get_bibstem(self, record):
        if self.bibstem:
            return self.bibstem
        else:
            bibstem = None
            # print(json.dumps(record, indent=2))
            try:
                if self.issn2bibstem:
                    issn_rec = []
                    try:
                        issn_rec = record['publication']['ISSN']
                    except Exception as err:
                        # print('bibstem: no issn... %s' % err)
                        pass
                    for i in issn_rec:
                        issn = i.get('issnString', None)
                        try:
                            if len(issn) == 8:
                                issn = issn[0:4] + '-' + issn[4:]
                        except Exception as err:
                            # print('Problem record: %s' % json.dumps(record, indent=2))
                            pass
                        if issn:
                            # print('issn: %s' % issn)
                            if not bibstem:
                                bibstem = self.issn2bibstem.get(issn, None)
            except Exception as err:
                print('bibstem err: %s' % err)
                pass
            if not bibstem:
                try:
                    if self.name2bibstem:
                        pub_name = record['publication']['pubName']
                        bibstem = self.name2bibstem.get(pub_name, None)
                except Exception as err:
                    print('bibstem err: %s' % err)
                    # raise BibstemException(err)
                    pass
        if bibstem:
            return bibstem
        else:
            raise BibstemException('Bibstem not found.')

    def make_bibcode(self, record):
        try:
            year = self._get_pubyear(record)
        except Exception as err:
            year = None
        try:
            bibstem = self._get_bibstem(record)
        except Exception as err:
            bibstem = None
        try:
            volume = self._get_volume(record)
        except Exception as err:
            volume = ''
        try:
            issue = self._get_issue(record)
        except:
            issue = None
        try:
            (pageid, is_letter) = self._get_pagenum(record)
            if is_letter:
                if not issue:
                    issue='L'
                else:
                    print('warning: issue number AND letter indicator!')
        except Exception as err:
            pageid = ''
        try:
            author_init = self._get_author_init(record)
        except Exception as err:
            author_init = ''
        if not (year and bibstem):
            raise NoBibcodeException("You're missing year and or bibstem -- no bibcode can be made!")
        else:
            bibstem = bibstem.ljust(5, '.')
            volume = volume.rjust(4, '.')
            pageid = pageid.rjust(5, '.')
            author_init = author_init.rjust(1, '.')
            if bibstem == 'JCAP.':
                volume = issue.rjust(4, '.')
            elif bibstem == 'ApJL.':
                bibstem = 'ApJ..'
                issue = 'L'
                
            elif bibstem == 'AIPC.':
                issue = pageid[0]
                pageid = pageid[1:]
            #if publisher == 'iop':
            #    else:
            #        issue = '.'
            #if publisher in ['aip', 'aps']:
            #    if len(pageid) == 5:
                        
                       
            if not issue:
                issue = '.'
            try:
                # bibcode = (year, bibstem, volume, issue, page, init)
                bibcode = year + bibstem + volume + issue + pageid + author_init
            except Exception as err:
                print('something is really wrong: %s' % err)
                bibcode = None
            else:
                return bibcode


