import pickle

def deserialize(fich):    
    pkl_file = open(fich, 'r')
    requetes = pickle.load(pkl_file)
    pkl_file.close()
    return requetes

def serialize(fich, data):
    output = open(fich, 'w')
    pickle.dump(data, output)
    output.close()
