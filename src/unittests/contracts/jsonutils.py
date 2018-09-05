def setvar(source, var, except_var=None):
    if isinstance(source, dict):
        for key, value in source.items():
            if isinstance(value, str) and (value[:5] == '#var ') and (value[5:] in var):
                if isinstance(except_var, list) and (value[5:] in except_var):
                    continue
                elif isinstance(except_var, str) and (except_var in value[5:]):
                    continue
                source[key] = var[value[5:]]
            else:
                setvar(source[key], var, except_var)
    if isinstance(source, list):
        for item in source:
            setvar(item, var, except_var)
        


def compare(expected, source, mp = {}, ignore_excess = False):
    if isinstance(source, dict) and isinstance(expected, dict):
        if not ignore_excess and (len(expected) != len (source)):
            return False
        for key, value in expected.items():
            if not key in source:
                return False
            else:
                if not compare(expected[key], source[key], mp, ignore_excess):
                    break
        else:
            return True
        return False
    
    if isinstance(source, list) and isinstance(expected, list):
        if(len(expected) > 0 and expected[0]=='#ignoreorder'):
            if(len(expected) - 1 != len (source)):
                return False
            else:
                bufs = source[:]
                bufe = expected[1:]
                for e in expected[1:]:
                    for s in source:
                        if compare(e, s, mp, ignore_excess):
                            bufs.remove(s)
                            bufe.remove(e)
                            break
                    else:
                        return False
                if len(bufs) == len(bufe) == 0:
                    return True
                return False
        else:
            if len(expected) != len(source):
                return False
            for i in range(len(source)):
                if not compare(expected[i], source[i], mp, ignore_excess):
                    break
            else:
                return True
            return False
    if isinstance(expected, str) and ('#var ' in expected) :
        mp[expected[5:]] = source
        return True
    
    if (isinstance(expected, str) and ('#ignore' in expected)) or (expected == source):
        return True
    return False


def find_by_field(e, field, value):
    if isinstance(e, dict):
        for key, val in e.items():
            if key == field and val == value:
                return e
            fitem = find_by_field(val, field, value)
            if fitem != None:
                return fitem
    if isinstance(e, list):
        for item in e:
            fitem = find_by_field(item, field, value)
            if fitem != None:
                return fitem
        return None