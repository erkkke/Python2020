linux = ('_~_', '(o o)', '/ V \\', '/( _ )\\', '^^ ^^')
linux_count = 5
for part in linux:
    print('  '.join(['{0:^7s}'.format(part)] * linux_count))