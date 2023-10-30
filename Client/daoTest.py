
list = [["1","Tín", "21TCLC_KHDL2", "CNTT"],
        ["2","Hiếu", "21TCLC_KHDL2", "CNTT"],
        ["3","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["4","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["5","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["6","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["7","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["8","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["9","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["10","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["11","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["12","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["13","Phúc", "21TCLC_KHDL2", "CNTT"],
        ["14","Phúc", "21TCLC_KHDL2", "CNTT"],
        ]
def select_user(pageable):
    if pageable.searcher.search == 'Tín':
        list=[["1","Tín", "21TCLC_KHDL2", "CNTT"],
            ["2","Tín", "21TCLC_KHDL2", "CNTT"],
            ["3","Tín", "21TCLC_KHDL2", "CNTT"],
            ["4","Tín", "21TCLC_KHDL2", "CNTT"]
        ]
        return list
    if pageable.searcher.search == 'Phúc':
        list=[["1","Phúc", "21TCLC_KHDL2", "CNTT"],
            ["2","Phúc", "21TCLC_KHDL2", "CNTT"],
            ["3","Phúc", "21TCLC_KHDL2", "CNTT"],
            ["4","Phúc", "21TCLC_KHDL2", "CNTT"]
        ]
        return list
    if pageable.searcher.search == 'Hiếu':
        list=[["1","Hiếu", "21TCLC_KHDL2", "CNTT"],
            ["2","Hiếu", "21TCLC_KHDL2", "CNTT"],
            ["3","Hiếu", "21TCLC_KHDL2", "CNTT"],
            ["4","Hiếu", "21TCLC_KHDL2", "CNTT"]
        ]
        return list
    elif pageable.page == 1:
        list = [["1","Tín", "21TCLC_KHDL2", "CNTT"],
                ["2","Hiếu", "21TCLC_KHDL2", "CNTT"],
                ["3","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["4","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["5","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["6","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["7","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["8","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["9","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["10","Phúc", "21TCLC_KHDL2", "CNTT"]]
        return list
    elif pageable.page == 2:
        list = [["11","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["12","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["13","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["14","Phúc", "21TCLC_KHDL2", "CNTT"]]
        return list
    elif pageable.page == 3:
        list = [["21","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["22","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["23","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["24","Phúc", "21TCLC_KHDL2", "CNTT"]]
        return list
    elif pageable.page == 4:
        list = [["31","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["32","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["33","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["34","Phúc", "21TCLC_KHDL2", "CNTT"]]
        return list
    elif pageable.page == 5:
        list = [["41","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["42","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["43","Phúc", "21TCLC_KHDL2", "CNTT"],
                ["44","Phúc", "21TCLC_KHDL2", "CNTT"]]
        return list
    return []

def totalItems():
    return 20

def request():
    return list[0:11]