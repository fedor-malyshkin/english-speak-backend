import json
import os.path
import re

from . import storage

OFFENSIVE = "offensive!"

AUSTRALIAN_ENGLISH = "Australian English"

BRITISH_ENGLISH = "British English"

BRITISH_AND = "British and"

AMERICAN_AND = "American and"

AMERICAN_ENGLISH = "American English"

FORMAL = "FORMAL"

INFORMAL = "INFORMAL"


def json_file(file_name):
    with open(file_name) as f:
        return storage.Storage(json.load(f))


def is_empty(value):
    return value.isspace() or len(value.strip()) == 0


def is_comment(value):
    return value.strip().startswith("#")


def flat_file(file_name):
    return storage.Storage(wrap_flat_records(read_lines(file_name)))


def flat_file_pairs(file_name, transformer):
    t = read_lines(file_name)
    data = []
    for e in list(zip(t[::2], t[1::2])):
        rec = {"name": e[0], "meaning": e[1]}
        rec = transformer(rec)
        data.append(rec)
    return storage.Storage(data)


def read_lines(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name) as f:
        value = f.read().splitlines()
        return [rec for rec in value if not is_empty(rec) and not is_comment(rec)]


def wrap_flat_records(records):
    return [{"name": rec} for rec in records]


def phrasal_verb_record_transformer(original_record):
    verb = original_record.get("name")
    details = []
    if verb.find(INFORMAL) != -1:
        verb = verb.replace(INFORMAL, "")
        details.append(INFORMAL)
    if verb.find(FORMAL) != -1:
        verb = verb.replace(FORMAL, "")
        details.append(FORMAL)
    if verb.find(AMERICAN_ENGLISH) != -1:
        verb = verb.replace(AMERICAN_ENGLISH, "")
        details.append("AmE")
    if verb.find(AMERICAN_AND) != -1:
        verb = verb.replace(AMERICAN_AND, "")
        details.append("AmE")
    if verb.find(BRITISH_AND) != -1:
        verb = verb.replace(BRITISH_AND, "")
        details.append("BrE")
    if verb.find(BRITISH_ENGLISH) != -1:
        verb = verb.replace(BRITISH_ENGLISH, "")
        details.append("BrE")
    if verb.find(AUSTRALIAN_ENGLISH) != -1:
        verb = verb.replace(AUSTRALIAN_ENGLISH, "")
        details.append("AuE")
    if verb.find(OFFENSIVE) != -1:
        verb = verb.replace(OFFENSIVE, "")
        details.append(OFFENSIVE)

    reg_expression = r'\(([0-9]+)\)'
    m = re.search(reg_expression, verb)
    if m is not None:
        verb = re.sub(reg_expression, "", verb)
        details.append("var. " + m.group(1))

    original_record.update({"name": verb.strip(), "note": ", ".join(details)})
    return original_record


def dumb_transformer(original_record):
    return original_record


def flat_file_map(file_name, separator):
    result = {}
    lines = read_lines(file_name)
    first_line = False
    temp_list = []
    k = "x"
    for l in lines:
        if l.strip().startswith(separator):
            result[k] = storage.Storage(temp_list)
            first_line = True
            temp_list = []
            continue
        if first_line:
            k = re.sub(r' +', "_", l.strip().lower())
            first_line = False
        else:
            temp_list.append(l.strip())
    result[k] = storage.Storage(temp_list)
    del result["x"]
    return result
