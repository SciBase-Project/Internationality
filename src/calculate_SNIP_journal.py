
def calc_RIP_DCP(P, Y) :
    import re
    import pymongo
    client = pymongo.MongoClient("localhost", 27017)
    # db name - aminer
    db = client.acm_aminer
    # collection
    db.publications

    last_years = [str(Y - 1), str(Y - 2), str(Y - 3)]
    reg1 = re.compile('%s.*'%P)
    #reg2 = re.compile('%s'%P.lower())
    #reg = re.compile('(%s|%s)'%(P,P.lower()))
    # all papers in last 3 years
    citable_items = list(db.publications.find({"publication" : {'$regex' : reg1}, "$or" : [{"year" : last_years[0]}, {"year" : last_years[1]}, {"year" : last_years[2]}] }))
    citable_items_ids = []
    for cite in citable_items : citable_items_ids.append(cite['index'])

    RIP = 0
    DCP = 0

    # all papers in current year
    try :
        cursor = db.publications.find({"year" : str(Y)})
        current_year_cites = 0

        active_cite_count = 0
        subject_field_papers_count = 0
        for paper in cursor :

            count = 0

            for cite in paper['references'] :
                if cite in citable_items_ids :
                    current_year_cites += 1
                    count += 1

            if count > 0 :
                active_cite_count += count
                subject_field_papers_count += 1

        # print "active_cite_count", active_cite_count
        # print "subject_field_papers_count", subject_field_papers_count
        # print "current_year_cites", current_year_cites
        # print "count", count


        if subject_field_papers_count == 0 : DCP = 0
        else : DCP = 1.0 * active_cite_count / subject_field_papers_count

        if len(citable_items_ids) == 0 : RIP = 0
        else : RIP = 1.0 * current_year_cites / len(citable_items_ids)

    except pymongo.errors.CursorNotFound :
        RIP = 0
        DCP = 0

    print P, "RIP:", RIP, "DCP:", DCP

    return RIP, DCP



from os import system
system("brew services start mongodb")


print "[INFO] Processing journals to be considered"

journals_to_consider = []

'''
file = open("../../output/ACM_Elsevier_journal_list_curated_v2")
for line in file.readlines() :
    line = line.strip()
    journal = line
    journals_to_consider.append(journal)
file.close()
'''

# file = open("../../data/journal_list_IEEE.txt")
# for line in file.readlines() :
#     line = line.strip()
#     journal = line.split(" : ")[0]
#     journals_to_consider.append(journal)
# file.close()

file = open("../output/IEEE_sorted.txt")
for line in file.readlines() :
    line = line.strip()
    journal = line.split(" : ")[0]
    journals_to_consider.append(journal)
file.close()


print "[DEBUG] Journals : ", journals_to_consider
print "[INFO] Done processing journals to be considered"


print "[INFO] Calculating SNIP for journals"

lst_rip = []
lst_dcp = []
J = [] # to prevent median being shifted due to zero-valued RIPs
for journal in journals_to_consider :
    rip, dcp = calc_RIP_DCP(journal, 2010)
    if rip != 0 and dcp != 0 :
        lst_rip.append(rip)
        lst_dcp.append(dcp)
        J.append(journal)


import numpy

SNIP_values = {'Jname':[],'RIP':[],'DCP':[],'SNIP':[]}
median_dcp = numpy.median(numpy.array(lst_dcp))

for i in range(0, len(J)) :
    rip = lst_rip[i]
    dcp = lst_dcp[i]
    rdcp = 1.0 * dcp / median_dcp

    if rdcp == 0 : snip = 0
    else : snip = rip / rdcp

    print "[DEBUG] ", J[i], "RIP:", rip, "DCP:", dcp, "SNIP:", snip
    SNIP_values['RIP'].append(rip)
    SNIP_values['DCP'].append(dcp)
    SNIP_values['SNIP'].append(snip)
    SNIP_values['Jname'].append(J[i])

import csv
keys = sorted(SNIP_values.keys())
with open("../output/SNIP_IEEE.csv", "wb") as outfile:
    writer = csv.writer(outfile, delimiter = ",")
    writer.writerow(keys)
    writer.writerows(zip(*[SNIP_values[key] for key in keys]))

system("brew services stop mongodb")

