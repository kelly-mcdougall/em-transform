import xml.etree.ElementTree as ET
import sys
import fileinput
import os

fn = sys.argv[1]
path, filename = os.path.split(fn)

    
tree = ET.parse(fn)
root = tree.getroot()

pref_text = ' '
gn = ''
roles = []
filename = filename + '_' + "output.txt"

file = open(filename, "w+")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


file.writelines('Role Information:\n')
for contrib in root.iter('contrib'):
    ctype = contrib.attrib
    if str(ctype['contrib-type']) != "author":
        break
    print(ctype)
    roles = []
    for gn in contrib.iter('given-names'):
        gn_text = gn.text
        file.writelines(gn_text + ' ')
    for sn in contrib.iter('surname'):
        sn_text = sn.text
        file.writelines(sn_text + ': ')
    for f in contrib.iter('role'):
        d = f.attrib
        try:
            r = d['content-type']
            if is_number(r) == False:
                roles.append(r)
        except KeyError as e:
            pass
    try:
        last_role = roles[-1]
    except IndexError as e:
        last_role = ''
    for role in roles:
        if role != last_role: 
            file.writelines(role + '; ')
        else:
            file.writelines(role + '. ')

file.writelines('\n\nFunding Information:\n')
for award_group in root.iter('award-group'):
    for award_recipient in award_group.iter('principal-award-recipient'):
        file.writelines(award_recipient.text + ', ')
    for funding_source in award_group.iter('funding-source'):
        file.writelines(funding_source.text )
    for funder_id in award_group.iter('named-content'):
        file.writelines(' (' +  funder_id.text + ')')
    for award_id in award_group.iter('award-id'):
        file.writelines(', Award ID: ' + award_id.text + '. ')

