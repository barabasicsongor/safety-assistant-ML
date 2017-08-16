import preprocessing
import utilities
import output

nhoods = preprocessing.preprocess_neighbourhoods(fpath='files/datasets/SFN.json')
crimes = preprocessing.preprocess_crimes_from_json(fname='files/output/crimes.json',nhoods=nhoods)

new_cr = []

for cr in crimes:
    if cr.type in preprocessing.CRIMES:
        new_cr.append(cr)

groups = []

for cr in new_cr:
    
    min = 305.0
    min_ind = -1
    index = -1
    
    for gr in groups:
        index += 1
        dist = utilities.get_distance_in_meters((cr.lat, cr.lng), (gr[0].lat, gr[0].lng))
        
        if dist < min:
            min = dist
            min_ind = index
            
                
    if min_ind == -1:
        groups.append([cr])
    else:
        groups[min_ind].append(cr)

output.gen_ar_map('files/output/ar_map.json',groups)