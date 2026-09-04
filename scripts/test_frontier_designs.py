#!/usr/bin/env python3
"""Run the local logic fixture for the completed advanced milestone-root test.

This checks fictional compact-JSON Deposit markers, occurrence indexing,
reconstruction, exact same-object eligibility, and the five-slot count logic.
It does not execute Element451 formulas or prove Element runtime behavior.
"""

import json
import re


def split_index(text, delimiter, index):
    parts = text.split(delimiter)
    return parts[index - 1] if 1 <= index <= len(parts) else ''


app_guid = 'school.applications.48217'
excluded_major = 'school.major.73104'
milestones = [
    {'name': 'Record Created', 'type': 'CREATED', 'date': {'$date': {'$numberLong': '1700000000000'}}},
    {'name': 'Client Import', 'application_guid': app_guid, 'term': 'school.terms.59321', 'type': 'DEPOSIT', 'date': {'$date': {'$numberLong': '1760000000000'}}},
    {'name': 'Deposit Page', 'application_guid': app_guid, 'term': 'school.terms.BAD', 'type': 'DEPOSIT', 'date': {'$date': {'$numberLong': '1770000000000'}}},
    {'name': 'Manual Entry', 'application_guid': app_guid, 'term': 'school.terms.59322', 'major': excluded_major, 'type': 'DEPOSIT', 'date': {'$date': {'$numberLong': '1780000000000'}}},
    {'name': 'Another Name', 'application_guid': app_guid, 'term': 'school.terms.59322', 'type': 'DEPOSIT', 'date': {'$date': {'$numberLong': '1790000000000'}}},
]
root = json.dumps(milestones, separators=(',', ':'))
type_marker = '"type":"DEPOSIT"'
next_milestone = '},{"name":"'
application_marker = '"application_guid":"' + app_guid + '"'
excluded_marker = '"major":"' + excluded_major + '"'
allowed = ['"term":"school.terms.59321"', '"term":"school.terms.59322"']
date_marker = '"date":{"$date":{"$numberLong":"'
count = 0
for index in range(2, 7):
    raw = split_index(root, type_marker, index)
    if not raw:
        continue
    prefix_segment = split_index(root, type_marker, index - 1)
    match = re.match(r'.*("name":.*)$', prefix_segment, flags=re.S)
    prefix = match.group(1) if match else ''
    suffix = split_index(raw, next_milestone, 1)
    obj = prefix + type_marker + suffix
    has_app = split_index(obj, application_marker, 2) != ''
    no_excluded = split_index(obj, excluded_marker, 2) == ''
    has_term = any(split_index(obj, item, 2) != '' for item in allowed)
    timestamp = split_index(split_index(obj, date_marker, 2), '"', 1)
    if has_app and no_excluded and has_term and timestamp:
        count += 1

assert count == 2, count
print('Local design-fixture check passed: guarded Deposit reconstruction/count.')
