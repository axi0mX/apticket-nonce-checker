#!/usr/bin/python
# Script which extracts packed SHSH into separate files.
# Author: axi0mX

import gzip, plistlib, sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'ERROR: Provide path to packed SHSH as argument to this script.'
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, 'rb') as f:
        data = f.read()

    if data.startswith('\x1f\x8b'):
        print 'Detected gzip comppression, will attempt to decompress file first.'
        with gzip.GzipFile(filename) as f:
            data = f.read()

    if data.startswith('bplist00'):
        print 'ERROR: This is a binary plist.'
        sys.exit(1)

    shsh = plistlib.readPlistFromString(data)

    if filename.endswith('.shsh'):
        new_filename_format = filename[:-5] + '-%s-%s.shsh'
    else:
        new_filename_format = filename + '-%s-%s.shsh'

    for build in shsh:
        if type(shsh[build]) is list:
            for i in range(len(shsh[build])):
                if 'LLB' in shsh[build][i]:
                    new_filename = new_filename_format % (build.replace(' ', '_'), i)
                    print 'Saving:', new_filename
                    with open(new_filename, 'wb') as f:
                        f.write(plistlib.writePlistToString(shsh[build][i]))
                else:
                    print 'WARNING: %s %s seems not to be valid SHSH, skipping.' % (build, i)
        else:
            for restore_type in shsh[build]:
                new_filename = new_filename_format % (build.replace(' ', '_'), restore_type)
                print 'Saving:', new_filename
                with open(new_filename, 'wb') as f:
                    f.write(plistlib.writePlistToString(shsh[build][restore_type]))
