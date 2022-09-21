import string
<<<<<<< HEAD
import json
=======
from adsputils import u2asc
from config import *
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b

class BibstemException(Exception):
    pass

class NoPubYearException(Exception):
    pass

class NoBibcodeException(Exception):
    pass

<<<<<<< HEAD
class Bibcode(object):

    def __init__(self, bibstem=None, issn2bibstem=None, name2bibstem=None):
=======
class BibcodeGenerator(object):

    def __init__(self, bibstem=None, issn2bibstem=ISSN2BIBSTEM, name2bibstem=NAME2BIBSTEM):
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
        self.issn2bibstem = issn2bibstem
        self.name2bibstem = name2bibstem
        self.bibstem = bibstem

<<<<<<< HEAD
    def _int_to_letter(integer):
        try:
            return string.ascii_letters[integer - 1]
        except:
=======
    def _int_to_letter(self, integer):
        try:
            return string.ascii_letters[int(integer) - 1]
        except Exception as err:
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
            return integer

    def _get_author_init(self, record):
        try:
            author_init = record['authors'][0]['name']['surname'][0]
<<<<<<< HEAD
=======
            author_init = u2asc(author_init).upper()
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
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
<<<<<<< HEAD
            issue_meta = record['publication']['issueNum']
            issue = self._int_to_letter(int(issue_meta))
=======
            issue = str(record['publication']['issueNum'])
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
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
<<<<<<< HEAD
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

                    
=======
            page = page.replace(',', '')
            return page
        else:
            return None

    def _deletter_page(self, page):
        is_letter = None
        if 'L' in page or 'l' in page:
            page = page.replace('L', '.').replace('l', '.')
            is_letter = 'L'
        elif 'P' in page or 'p' in page:
            page = page.replace('P', '').replace('p', '')
            is_letter = 'P'
        elif 'S' in page or 's' in page:
            page = page.replace('S', '').replace('s', '')
            is_letter = 'S'
        elif 'A' in page:
            page = page.replace('A', '')
            is_letter = 'A'
        elif 'C' in page:
            page = page.replace('C', '')
            is_letter = 'C'
        elif 'E' in page:
            page = page.replace('E', '')
            is_letter = 'E'
        return (page, is_letter)

    def _get_normal_pagenum(self, record):
        page = self._get_pagenum(record)
        is_letter = None
        if page:
            (page, is_letter) = self._deletter_page(page)
            if len(str(page)) >= 5:
                page = str(page)[-5:]
            else:
                page = page.rjust(4, '.')
            if is_letter:
                page = page[-4:]
        return (page, is_letter)

    def _get_converted_pagenum(self, record):
        try:
            page = self._get_pagenum(record)
            (page, is_letter) = self._deletter_page(page)
            if page:
                page_a = None
                if len(str(page)) >= 6:
                    page = page[-6:]
                    page_a = self._int_to_letter(page[0:2])
                    page = page[2:]
                if page_a:
                    if not is_letter:
                        is_letter = page_a
                    # else:
                    #     logger.debug('warning, converted pagenum *and* issue letter found (%s, %s)' % (page_a, is_letter))
        except Exception as err:
            page = None
            is_letter = None
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
        return page, is_letter

    def _get_bibstem(self, record):
        if self.bibstem:
            return self.bibstem
        else:
            bibstem = None
<<<<<<< HEAD
            # print(json.dumps(record, indent=2))
=======
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
            try:
                if self.issn2bibstem:
                    issn_rec = []
                    try:
                        issn_rec = record['publication']['ISSN']
                    except Exception as err:
<<<<<<< HEAD
                        # print('bibstem: no issn... %s' % err)
=======
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
                        pass
                    for i in issn_rec:
                        issn = i.get('issnString', None)
                        try:
                            if len(issn) == 8:
                                issn = issn[0:4] + '-' + issn[4:]
                        except Exception as err:
<<<<<<< HEAD
                            # print('Problem record: %s' % json.dumps(record, indent=2))
                            pass
                        if issn:
                            # print('issn: %s' % issn)
                            if not bibstem:
                                bibstem = self.issn2bibstem.get(issn, None)
            except Exception as err:
                print('bibstem err: %s' % err)
=======
                            pass
                        if issn:
                            if not bibstem:
                                bibstem = self.issn2bibstem.get(issn, None)
            except Exception as err:
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
                pass
            if not bibstem:
                try:
                    if self.name2bibstem:
                        pub_name = record['publication']['pubName']
                        bibstem = self.name2bibstem.get(pub_name, None)
                except Exception as err:
                    print('bibstem err: %s' % err)
<<<<<<< HEAD
                    # raise BibstemException(err)
=======
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
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
<<<<<<< HEAD
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
=======
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
            author_init = self._get_author_init(record)
        except Exception as err:
            author_init = ''
        if not (year and bibstem):
            raise NoBibcodeException("You're missing year and or bibstem -- no bibcode can be made!")
        else:
            bibstem = bibstem.ljust(5, '.')
            volume = volume.rjust(4, '.')
<<<<<<< HEAD
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
=======
            author_init = author_init.rjust(1, '.')
            issue = None

            # Special bibstem, page, volume, issue handling
            if bibstem in IOP_BIBSTEMS:
                # IOP get converted_pagenum/letters for six+ digit pages
                (pageid, is_letter) = self._get_converted_pagenum(record)
                if bibstem == 'JCAP.':
                    # JCAP is an IOP journal
                    try:
                        issue = self._get_issue(record)
                        volume = issue.rjust(4, '.')
                        issue = None
                    except:
                        issue = None
                elif bibstem == 'ApJL.':
                    # ApJ/L are IOP journals
                    bibstem = 'ApJ..'
                    issue = 'L'
                if is_letter:
                    if not issue:
                        issue=is_letter
                    # else:
                       # logger.debug('warning: issue number AND letter indicator!')

            elif bibstem in APS_BIBSTEMS:
                # APS get converted_pagenum/letters for six+ digit pages
                (pageid, is_letter) = self._get_converted_pagenum(record)
                if is_letter:
                    if not issue:
                        issue=is_letter
                    # else:
                       # logger.debug('warning: issue number AND letter indicator!')

            elif bibstem in OUP_BIBSTEMS:
                # APS get converted_pagenum/letters for six+ digit pages
                (pageid, is_letter) = self._get_converted_pagenum(record)
                if is_letter:
                    if not issue:
                        issue=is_letter
                    # else:
                       # logger.debug('warning: issue number AND letter indicator!')

            elif bibstem in AIP_BIBSTEMS:
                #AIP: AIP Conf gets special handling
                (pageid, is_letter) = self._get_converted_pagenum(record)
                if bibstem == 'AIPC.':
                    if is_letter:
                        if not issue:
                            issue=is_letter
                        # else:
                           # logger.debug('warning: issue number AND letter indicator!')
                else:
                    issue = self._int_to_letter(self._get_issue(record))
            else:
                (pageid, is_letter) = self._get_normal_pagenum(record)
                if is_letter:
                    if not issue:
                        issue = is_letter
                    # else:
                       # logger.debug('warning: issue number AND letter indicator!')

            if not issue:
                pageid = pageid.rjust(5, '.')
                issue = ''
            else:
                pageid = pageid.rjust(4, '.')

            try:
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
                bibcode = year + bibstem + volume + issue + pageid + author_init
            except Exception as err:
                print('something is really wrong: %s' % err)
                bibcode = None
<<<<<<< HEAD
            else:
                return bibcode


=======
            return bibcode
>>>>>>> f9f8c8fcd1681a83e2daefc70edc6d18cd55363b
