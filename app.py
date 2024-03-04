from flask import Flask, render_template, request, jsonify
from itertools import combinations
from collections import defaultdict
import json

app = Flask(__name__, static_url_path='/static')

global_missing = []
global_not_first = []
global_high = []
global_all = []

def factorial(num):
    if num <= 1:
        return 1
    return num * factorial(num - 1)


def minimum_pairing(_map, people, w1, w2, w3):
    min_pairing = float('inf')
    a, b, c = 0, 0, 0

    for i in range(len(people)):
        for j in range(len(people)):
            for k in range(len(people)):
                if i == j or j == k or i == k:
                    continue

                working_sum = 0

                for el in _map[people[i]]:
                    if el[1] == w1:
                        working_sum += el[0]
                        break

                for el in _map[people[j]]:
                    if el[1] == w2:
                        working_sum += el[0]
                        break

                for el in _map[people[k]]:
                    if el[1] == w3:
                        working_sum += el[0]
                        break

                if working_sum < min_pairing:
                    min_pairing = working_sum
                    a, b, c = i, j, k

    if min_pairing > 999:
        global_missing.append([people[a], people[b], people[c], w1, w2, w3])

    if min_pairing >= 9:
        global_high.append([people[a], people[b], people[c], w1, w2, w3])

    first_choices = {_map[person][0][1] for person in people}
    if first_choices != {w1, w2, w3}:
        global_not_first.append([people[a], people[b], people[c], w1, w2, w3])

    global_all.append([people[a], people[b], people[c], w1, w2, w3])

    result = [a, b, c]
    
    return result


def cross_examination(list1, list2, list3):
    witnesses = ["Burke", "Cosmos", "Bahmani", "Nguyen", "Cage", "Nova", "Sands"]
    people = ["Arnav", "AJ", "Sarah"]

    lists = []
    lists.append(("Arnav", list1))
    lists.append(("AJ", list2))
    lists.append(("Sarah", list3))

    map_ = {}
    final_count = defaultdict(int)
    search = defaultdict(list)

    for lst in lists:
        working_witnesses = witnesses.copy()
        counts = []
        for j, w in enumerate(lst[1], start=1):
            counts.append((j, w))
            if w in working_witnesses:
                working_witnesses.remove(w)
        for el in working_witnesses:
            counts.append((999, el))
        map_[lst[0]] = counts

    for i in range(len(witnesses)):
        for j in range(i + 1, len(witnesses)):
            for k in range(j + 1, len(witnesses)):
                values = minimum_pairing(map_, people, witnesses[i], witnesses[j], witnesses[k])

                final_count[(people[values[0]], witnesses[i])] += 1
                final_count[(people[values[1]], witnesses[j])] += 1
                final_count[(people[values[2]], witnesses[k])] += 1

                search[(people[values[0]], witnesses[i])].append((witnesses[i], witnesses[j], witnesses[k]))
                search[(people[values[1]], witnesses[j])].append((witnesses[i], witnesses[j], witnesses[k]))
                search[(people[values[2]], witnesses[k])].append((witnesses[i], witnesses[j], witnesses[k]))


    denom = (6 * (factorial(7 - 3)))
    total = factorial(7) / denom

    result = []
    for key, value in final_count.items():
        result.append((key[0], key[1], value, value / total))
    
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_lists', methods=['POST'])
def process_lists_route():
    data = request.json
    list1 = data['list1'].split()  
    list2 = data['list2'].split()
    list3 = data['list3'].split()
    global global_missing
    global_missing = []

    global global_not_first
    global_not_first = []

    global global_high
    global_high = []

    global global_all
    global_all = []

    result = cross_examination(list1, list2, list3)

    grouped_result = defaultdict(list)
    for item in result:
        person = item[0]
        grouped_result[person].append(item)

    
    formatted_result = ""
    for person, items in grouped_result.items():
        formatted_result += f"{person}\n"
        formatted_result += "\n".join(f"{item[1]} {item[2]} *** {item[3]}" for item in items)
        formatted_result += "\n"

    formatted_result += "\n\n"   

    for missing in global_missing:
        formatted_result += f"{missing[0]}:{missing[3]}  ****  {missing[1]}:{missing[4]}  ****  {missing[2]}:{missing[5]}\n" 

    formatted_result += "\n\n"

    for not_first in global_not_first:
        formatted_result += f"{not_first[0]}:{not_first[3]}  ****  {not_first[1]}:{not_first[4]}  ****  {not_first[2]}:{not_first[5]}\n" 

    formatted_result += "\n\n"

    for high in global_high:
        formatted_result += f"{high[0]}:{high[3]}  ****  {high[1]}:{high[4]}  ****  {high[2]}:{high[5]}\n"

    formatted_result += "\n\n"

    for all in global_all:
        formatted_result += f"{all[0]}:{all[3]}  ****  {all[1]}:{all[4]}  ****  {all[2]}:{all[5]}\n"

    return formatted_result

if __name__ == '__main__':
    app.run(debug=True)
