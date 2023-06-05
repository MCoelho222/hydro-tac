def sort_str_endswithnum(str_endwithnum_list, split_char):
    ints = []
    ordered_sites = []
    for k in str_endwithnum_list:
        if k[-1] == ' ':
            k.pop()
        point = k.split(split_char)[1]
        idx = -1
        while True:
            try:
                ints.append(int(point))
                break
            except ValueError:
                point = point[:-1]
                continue
    ints.sort()
    for k in range(len(ints)):
        for l in str_endwithnum_list:
            element = l.split(split_char)[1]
            while True:
                try:
                    if int(element) == ints[k]:
                        if l not in ordered_sites:
                            ordered_sites.append(l)
                    break
                except ValueError:
                    element = element[:-1]
                    continue
    for item in ordered_sites:
        if item not in str_endwithnum_list:
            idx = ordered_sites.index(item)
            ordered_sites.pop(idx)
    
    finallist = []
    for item in ordered_sites:
        if item not in finallist:
            finallist.append(item)

    return finallist


def sort_bespts(points):
    ints = []
    ordered_sites = []
    for k in points:
        point = k[3:]
        
        ints.append(int(point))
               
    ints.sort()
    for k in range(len(ints)):
        for l in points:
            element = l[3:]

            if int(element) == ints[k]:
                ordered_sites.append(l)
                    
    for item in ordered_sites:
        if item not in points:
            idx = ordered_sites.index(item)
            ordered_sites.pop(idx)
    
    finallist = []
    for item in ordered_sites:
        if item not in finallist:
            finallist.append(item)

    return finallist


def replace_as_lastcols(df, lastcols):

    df_cols = list(df.columns)
    for col in lastcols:
        pop_ind = df_cols.index(col)
        df_cols.pop(pop_ind)
    for col in lastcols:
        df_cols.append(col)
    df = df[df_cols]
    
    return df


def ordered_bes_sites(order, cols):
    tidal_col_ints = []
    for i in range(len(cols)):
        tidal_col_ints.append(int(cols[i][3:]))
    ordered_tidal_cols = []
    for i in range(len(order)):
        if order[i] in tidal_col_ints:
            ordered_tidal_cols.append(order[i])

    return ordered_tidal_cols


def ordered_hydro_sites(order, cols):
    ordered = []
    for i in range(len(order)):
        if order[i] in cols:
            ordered.append(order[i])

    return ordered