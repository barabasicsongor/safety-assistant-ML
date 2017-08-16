# Operations for writing to file

"""

Writes heatmap to JSON file
Structure is "items": []
In the array the items keys are: hood_name, color, total_crimes, polygon

"""


def gen_heatmap(fname, nhoods, crime_freq):
    f = open(fname, 'w')
    f.write('{\n"items": [\n')

    N = len(nhoods)
    for i in range(0, (N - 1)):

        # Get the polygon coordinates
        x, y = nhoods[i].polygon.exterior.coords.xy
        poly = []
        for j in range(0, len(x)):
            poly.append(x[j])
            poly.append(y[j])

        f.write('{')
        f.write('"hood_name":"{}","color":"{}","total_crimes":{},"polygon":{}'.format(nhoods[i].name, nhoods[i].color,
                                                                                      crime_freq[i]['total'], poly))
        f.write('},\n')

    # Write the last one out
    # Get the polygon coordinates
    x, y = nhoods[N - 1].polygon.exterior.coords.xy
    poly = []
    for j in range(0, len(x)):
        poly.append(x[j])
        poly.append(y[j])

    f.write('{')
    f.write(
        '"hood_name":"{}","color":"{}","total_crimes":{},"polygon":{}'.format(nhoods[N - 1].name, nhoods[N - 1].color,
                                                                              crime_freq[N - 1]['total'], poly))
    f.write('}\n')

    f.write(']\n}')
    f.close()

"""

Generate JSON file for heatmap

"""
def gen_ar_map(fname, cr_groups):
    f = open(fname, 'w')
    f.write('{\n"items": [\n')
    
    lower_color = '#89e21b'
    mid_color = '#f7ef54'
    up_color = '#E53935'
    
    group_count = [len(x) for x in cr_groups]
    
    lower_bound = int(sum(group_count)/len(cr_groups))
    mid_bound = lower_bound * 2
    
    for x in range(0, (len(cr_groups)-1)):
        gr = cr_groups[x]
        l = len(gr)
        
        if l < lower_bound:
            color = lower_color
        elif l >= lower_bound and l < mid_bound:
            color = mid_color
        else:
            color = up_color
        
        f.write('{')
        f.write('"title": "{}", "color": "{}", "lat": {}, "lng": {}'.format(str(l), color, gr[0].lat, gr[0].lng))
        f.write('},\n')
    
    # Write out the last one   
    gr = cr_groups[len(cr_groups) - 1]
    l = len(gr)
    
    if l < lower_bound:
        color = lower_color
    elif l >= lower_bound and l < mid_bound:
        color = mid_color
    else:
        color = up_color
        
    f.write('{')
    f.write('"title": "{}", "color": "{}", "lat": {}, "lng": {}'.format(str(l), color, gr[0].lat, gr[0].lng))
    f.write('}\n')
    
    f.write(']\n}')
    f.close()

"""

Write all the crimes to a JSON file, so it is easier to read and link them 
with neighbourhoods during data preprocessing

"""


def crimes_to_json(fname, crimes):
    f = open(fname, 'w')
    f.write('{\n"items": [\n')

    N = len(crimes)
    for i in range(0, (N - 1)):
        f.write(crimes[i].to_json() + ',')
    f.write(crimes[N - 1].to_json())
    f.write(']\n}')
    f.close()