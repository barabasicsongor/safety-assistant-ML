import preprocessing
import output
import utilities

if __name__ == '__main__':
    # READ DATA
    crimes = preprocessing.preprocess_crimes(['files/datasets/Police_Department_Incidents_2016.csv',
                                              'files/datasets/Police_Department_Incidents_2017.csv'], [1, 3, 4, 5, 9, 10])
    nhoods = preprocessing.preprocess_neighbourhoods('files/datasets/SFN.json')
    crimes = preprocessing.group_crimes_by_nhood(crimes, nhoods)

    # SAVE PREPROCESSED CRIME DATA TO JSON
    output.crimes_to_json('files/output/crimes.json', crimes)

    # GENERATE HEATMAP AND SAVE TO JSON FILE

    # Get crime frequency list for the hoods
    # List of dictionaries having detailed stats
    crime_freq = preprocessing.hood_crime_frequency(crimes, nhoods)
    # Sort the two arrays, simultaneously, according to crime_freq[i]['total']
    crime_freq, nhoods = utilities.sim_sort(crime_freq, nhoods)
    crime_freq_totals = [d['total'] for d in crime_freq]

    # Generate color gradient for map coloring
    gradient = ['#89e21b', '#f7ef54', '#e5a735', '#E53935']

    # Assigning colors to the Neighbourhood objects from the gradient
    max = max(crime_freq_totals)

    for i in range(0, len(nhoods)):

        p = float(crime_freq_totals[i] / max)

        if p >= 0 and p < 0.15:
            nhoods[i].color = gradient[0]
        elif p >= 0.15 and p < 0.4:
            nhoods[i].color = gradient[1]
        elif p >= 0.4 and p < 0.7:
            nhoods[i].color = gradient[2]
        else:
            nhoods[i].color = gradient[3]

    # Write hood details to JSON file
    output.gen_heatmap('files/output/heatmap.json', nhoods, crime_freq)