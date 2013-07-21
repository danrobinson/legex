# encoding: UTF-8

import re
import sys
import requests
import os

XHTML = "{http://www.w3.org/1999/xhtml}"

REPORTERS = []

def reporter_fix(rep):
    return rep.rstrip('\n').replace('.', '.?').replace(' ', ' ?')

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'reporters.txt'), 'r') as f:
    REPORTERS = [reporter_fix(line) for line in f]

#ABBREVIATIONS_LIST = ["Acad\.", "Admin\.", "Adm'[rx]", "Adver\.", "Agric\.", "Alt\.", "Am\.", "&", "Assoc\.", "Ass'n", "Atl\.", "Auth\.", "Auto\.", "Ave\.", "Bankr\.", "Bd\.", "Broad\.", "Bhd\.", "Bros\.", "Bldg\.", "Bus\.", "Cas\.", "Ctr\.", "Cent\.", "Chem\.", "Coal\.", "Coll\.", "Comm'n", "Comm'r", "Comm\.", "Commc'n", "Cmty\.", "Co\.", "Comp\.", "Condo\.", "Cong\.", "Consol\.", "Constr\.", "Cont'l", "Coop\.", "Corp\.", "Corr\.", "Cnty\.", "Def\.", "Dep't", "Det\.", "Dev\.", "Dir\.", "Disc\.", "Distrib\.", "Dist\.", "Div\.", "E\.", "Econ\.", "Ed\.", "Educ\.", "Elec\.", "Emp\.", "Emp'[rt]", "Eng'r", "Eng'g", "Enter\.", "Entm't", "Env't", "Envtl\.", "Equal\.", "Equip\.", "Exam'r", "Exch\.", "Exec\.", "Ex'[rx]", "Exp\.", "Fed\.", "Fed'n", "Fid\.", "Fin\.", "Found\.", "Gen\.", "Gend\.", "Gov't", "Grp\.", "Guar\.", "Hosp\.", "Hous\.", "Imp\.", "Inc\.", "Indem\.", "Indep\.", "Indus\.", "Info\.", "Inst\.", "Ins\.", "Int'l", "Inv\.", "Lab\.", "Liab\.", "Ltd\.", "Litig\.", "Mach\.", "Maint\.", "Mgmt\.", "Mfr\.", "Mfg\.", "Mar\.", "Mkt\.", "Mktg\.", "Mech\.", "Med\.", "Mem'l", "Merch\.", "Metro\.", "Mortg\.", "Mun\.", "Mut\.", "Nat'l", "N\.", "Ne\.", "Nw\.", "No\.", "Op\.", "Org\.", "Pac\.", "P'ship", "Pers\.", "Pharm\.", "Pres\.", "Prob\.", "Prod\.", "Prof'l", "Prop\.", "Prot\.", "Pub\.", "Publ'n", "Publ'g", "R\.R\.", "Ry\.", "Ref\.", "Reg'l", "Rehab\.", "Reprod\.", "Res\.", "Rest\.", "Ret\.", "Rd\.", "Sav\.", "Sch\.", "Sci\.", "Sec'y", "Sec\.", "Serv\.", "S'holder", "Soc\.", "Soc'y", "S\.", "Se\.", "Sw\.", "S\.S\.", "St\.", "Subcomm\.", "Sur\.", "Sys\.", "Tech\.", "Telecomm\.", "Tel\.", "Temp\.", "Twp\.", "Transcon\.", "Transp\.", "Tr\.", "Tpk\.", "Unif\.", "Univ\.", "Util\.", "Vill\.", "W\."]

PARTY_WORD = "(?![Ss]ee|[Cc]f\.?)[A-Z0-9][A-Za-z0-9,/\.']+"

PARTYNAME_REGEX = "(?:(?:%s) ){1,}(?:(?:%s|and|of|re|for|de|&) ){0,}" % (PARTY_WORD, PARTY_WORD)

CASENAME_REGEX = "(?:(?:(?:(?P<first_party>%s)v\. )?(?P<second_party>(?:%s)?[A-Z0-9][a-z'0-9]+)), )?" % (PARTYNAME_REGEX, PARTYNAME_REGEX)

REPORTER_REGEX = "(?P<reporter>" + "|".join(REPORTERS) + ")"

CITATION_REGEX = "(?:(?P<volume>\d+) %s(?: (?P<page>\d+)(?:, (?P<pincite>[\d\-\–]+))?|(, at (?P<shortcite>[\d\-\–]+)))(?:, ?)?){1,}" % REPORTER_REGEX

YEAR_REGEX = " ?(?:\((?P<year>\d{4})\))?"

OPINION_REGEX = " ?(?:\((?P<justice>[A-Za-z]+), J\., (?P<con_or_diss>concurring|dissenting)\))?"

SIGNAL_REGEX = "(?:(?P<signal>(?:[Bb]ut )?(?:(?:[Ss]ee)|(?:[Cc]f.?))(?: generally)?(?: also)?(?:, e.g.,)?) )?"

CASE_REGEX = SIGNAL_REGEX + CASENAME_REGEX + CITATION_REGEX + YEAR_REGEX + OPINION_REGEX

SUPRA_REGEX = "(?P<shortname>[A-Z][A-Za-z']+), supra, at (?P<page>\d+)" + OPINION_REGEX

reg = re.compile(CASE_REGEX)

class Parser(object):

    def parse(self, t):
        print [(m.groupdict()["first_party"], m.groupdict()["second_party"], m.groupdict()["reporter"]) for m in reg.finditer(t)]
