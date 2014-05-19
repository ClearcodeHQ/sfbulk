def loadFromCSVFile(filename, max_count=10000, omit_header=False):
    """
    Simple utility to load from csv file.
    Assumption : first line will be the field name
    """
    sane_files = []
    retval = u''
    linecount = 0
    headerLines = u''
    for line in open(filename):
        retval += line
        linecount += 1
        if headerLines == u'' and not omit_header:
            headerLines = line
            linecount = 0
        if linecount >= max_count:
            linecount = 0
            sane_files.append(retval)
            retval = u''
            retval += headerLines

    if retval != u'' and retval != headerLines:
        sane_files.append(retval)
    return sane_files
