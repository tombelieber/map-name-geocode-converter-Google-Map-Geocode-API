import googlemaps

# key, do not disclose it!!!!!
key = 'Your Google API key'

# Testing
fname = 'test_input.csv'
outputName = 'test_output'

# 1. Read text file
with open(fname, encoding="utf-8-sig") as f:
    input = f.readlines()

# 2. Fine tune names: clean input data, remove unnecessary character
i = 0
for name in input:
    input[i] = name.strip()
    input[i] = name.replace('""', "")
    input[i] = name.replace('\n', "")
    i += 1

# 3. Name-Geocoding conversion: enquiry google Geocoding API to get geocode (x,y)
gmaps = googlemaps.Client(key=key)
# Geocoding an address
answer = []
error_list = []
j = 0
for name in input:
    if name != "":
        geocode_result = gmaps.geocode(name)
        # Try to search for geocode of places
        try:
            x = geocode_result[0]['geometry']['location']['lat']
            y = geocode_result[0]['geometry']['location']['lng']
            answer.append((x, y))
        # If fail to use geocoding API, return fail-x, fail-y
        except:
            print("Error! Failed to convert, adding error in to error list...")
            print("the %dth term, name=%s" % (j, name))
            error_list.append((name, 'fail-x', 'fail-y'))
            answer.append(('fail-x', 'fail-y'))
    # This name is empty
    else:
        print("empty string detected! skip this.")
        answer.append(("empty", "empty", "empty"))
    j += 1

# output file name,x,y
with open(outputName + '.csv', 'w', encoding="utf-8-sig") as f:
    i = 0
    f.write("name,x,y\n")
    for name in input:
        # Since empty string, fail-x, fail-y is in the list, use 2 format string
        if type(answer[i][0]) != str:
            f.write("%s,%f,%f\n" % (name, answer[i][0], answer[i][1]))
        else:
            f.write("%s,%s,%s\n" % (name, answer[i][0], answer[i][1]))
        i += 1