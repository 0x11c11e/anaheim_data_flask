import csv
import shelve
import collections
import os
import pickle

try:
    os.remove("data/shelve.db.bak")
    os.remove("data/shelve.db.dat")
    os.remove("data/shelve.db.dir")
except OSError:
    pass

# file = open("data/street_names.txt", "w")

# for key in sorted(d):
#     file.write(key + "\n")
# file.close()

def md5_hash(string):
    import hashlib
    return str(hashlib.md5(string.encode('utf-8')).hexdigest())

def write_pickle():
    with open('people.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        r = {}
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                street_name = f'{row[16]}'.lower()
                voter_id = f'{row[0]}'
                street_name_hash = md5_hash(street_name)

                if street_name_hash not in r:
                    r[street_name_hash] = {}
                r[street_name_hash][str(voter_id)] = row
                    
                line_count += 1
            print(f'Processed {line_count} lines.')
        with open('data/data.pickle', 'wb') as handle:
            pickle.dump(r, handle, protocol=pickle.HIGHEST_PROTOCOL)

def read_pickle():
    with open('data/data.pickle', 'rb') as handle:
        r = pickle.load(handle)
        for key in r.keys():
            print(key)
            for voter_id in r[key].keys():
                print(r[key][voter_id])

read_pickle()