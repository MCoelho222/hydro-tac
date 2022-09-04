def sort_str_endswithnum(str_endwithnum_list, split_char):
    # print(str_endwithnum_list)
    ints = []
    ordered_sites = []
    for k in str_endwithnum_list:
        # print(str_endwithnum_list)
        point = k.split(split_char)[1]
        idx = -1
        while True:
            try:
                ints.append(int(point))
                break
            except ValueError:
                # print('POINT', str_endwithnum_list)
                point = point[:idx]
                continue
                
                # try:
                #     ints.append(int(point[:idx]))
                # except:
                #     idx -= 1
                #     continue
            # print(ints)
    # print(ints)
    ints.sort()
    # print(ints)
    for k in range(len(ints)):
        for l in str_endwithnum_list:
            element = l.split(split_char)[1]
            while True:
                try:
                    if int(element) == ints[k]:
                        ordered_sites.append(l)
                    break
                except ValueError:
                    element = element[:-1]
                    continue
                    # element = l.split(split_char)[1][:-1]
                    # if int(element) == ints[k]:
                    #     ordered_sites.append(l)
    for item in ordered_sites:
        if item not in str_endwithnum_list:
            idx = ordered_sites.index(item)
            ordered_sites.pop(idx)
    
    finallist = []
    for item in ordered_sites:
        if item not in finallist:
            finallist.append(item)
        

    # print(finallist)
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
