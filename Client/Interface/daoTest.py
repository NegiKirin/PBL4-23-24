
list = [["Tín", "21TCLC_KHDL2", "CNTT"],
        ["Hiếu", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"]
        ]

def select_user(pageable):
    if pageable.searcher.search == 'Tín':
        list=[["Tín", "21TCLC_KHDL2", "CNTT"],
            ["Tín", "21TCLC_KHDL2", "CNTT"],
            ["Tín", "21TCLC_KHDL2", "CNTT"],
            ["Tín", "21TCLC_KHDL2", "CNTT"]
        ]
        return list
    if pageable.searcher.search == 'Phúc':
        list=[["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"]
        ]
        return list
    if pageable.searcher.search == 'Hiếu':
        list=[["Hiếu", "21TCLC_KHDL2", "CNTT"],
            ["Hiếu", "21TCLC_KHDL2", "CNTT"],
            ["Hiếu", "21TCLC_KHDL2", "CNTT"],
            ["Hiếu", "21TCLC_KHDL2", "CNTT"]
        ]
        return list
    elif pageable.page == 1:
        list = [["Tín", "21TCLC_KHDL2", "CNTT"],
        ["Hiếu", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"]]
        return list
    elif pageable.page == 2:
        list = [["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"]]
        return list
    return []