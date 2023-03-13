#!/usr/bin/env python3

import re
import csv
import sys

def write_to_csv(filename, columns, func):
  with open(filename, 'w') as csvfile:
    fieldnames = columns
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    getattr(sys.modules[__name__], func)(writer)

def write_users(writer):
  for user, value in sorted(users_data.items()):
    writer.writerow({ 'Username': user, 'INFO': value.get('infos', 0), 'ERROR': value.get('errors', 0) })

def write_errors(writer):
  for found_error, value in sorted(errors_data.items(), key=lambda x:x[1], reverse=True):
    writer.writerow({ 'Error': found_error, 'Count': value })

def increment(key):
  num = users_data[username].get(key, 0)
  users_data[username][key] = num + 1

errors_data = {}
users_data = {}

with open('syslog.log') as file:
  for line in file:
    username = re.search(r"^.+\((.*)\)$", line).group(1)
    value = users_data.get(username)

    if value is None:
        users_data[username] = {}

    error_match = re.search(r"^.+ ERROR (.+) \(.+$", line)

    if not error_match:
      increment('infos')
      continue

    increment('errors')
    error_text = error_match.group(1)
    error_count = errors_data.get(error_text, 0)
    errors_data[error_text] = error_count + 1

write_to_csv('user_statistics.csv', ['Username', 'INFO', 'ERROR'], 'write_users')
write_to_csv('error_message.csv', ['Error', 'Count'], 'write_errors')


