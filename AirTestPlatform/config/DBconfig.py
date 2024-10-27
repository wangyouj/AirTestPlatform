from common.Tools import getEncodeStr

'''
host, user, password, database, port, charset=db_airResource()
host = getEncodeStr(host)
print(host)
user = getEncodeStr(user)
print(user)
password = getEncodeStr(password)
print(password)
E = getEncodeStr(database)
print(database)
'''


def db_airOpen():
    '''
    数据库配置
    :return:
    '''
    host = 'gAAAAABmsdSLYy82M1iBNfyBqGZBiGjlgNFaXUG0q2TrzEMEZrKUk639e9-tX2RKa7pCCWNdKBIIfg8ZCVVT0JPGlBHqOFTWtftKnJ-O2prEbcctv3QL2NelrX-_yjDpqshF4d7Qny_P'
    user = 'gAAAAABmsdQ2OUs9pIkgASQ8slTr8Vggp7aGnDzRcYm1zUhRPVdNiB3WmXsTDHY1tDtDz1o--5XVsPU4g4bx3dp33iw9CMocSQ=='
    password = 'gAAAAABmsdO90pvu1oj6z3SBxOtVaUN9FwQU_RIzbebELVsR9a4LSPVp0JOEbVG5TOKaLpxsGGDMM9gd3YCldew--4CtldnlgA=='
    database = 'gAAAAABmsdReX3XlbTI7iYgn2BPCzuvEO3fd9rOOtogBBhCov0mB7ssivrP9etsaSGd9PGqC-vh1Xl1tWissA1Tcl6axuujwSg=='
    port = 3306
    charset = 'utf8'
    # 返回数据库配置信息
    return host, user, password, database, port, charset


def db_airTest():
    '''
    数据库连接信息
    :return:
    '''
    host='gAAAAABmwcgr8Me18js9USEOo_3rF2kqg67h65uijFsd0t7QERIrBvAHn-4OiRNthQMAHV49ERQTvCAWhmSCobDoy4yYzTE8sfCHY6Ztv4lwKTMRyoDPn2c='
    user='gAAAAABmwch7wueEMmGDA1NOqJpqEVLU4ujvu_H64T0XQyQiZ5EuGPwVdsqTEEa7GZHTQJygIb13P7NGnzvPkccnuaHIIsZ1Jw=='
    password='gAAAAABmwch7ZD7AdXI28xhjWQfEga73SH_zp6_iRq4Hksx3-zSR-pscgtsLyHwYfboTHv4OUhKqWl1dL0Ap_9Lf57-UdU9RqQ=='
    database='gAAAAABmwch7lu4SEenivoc-DknDKaSaTr_fDhWTV0gQx7DQpZm5H1g5Ep9UWlN1W4Us3O6sQeQykwzx0oo3bVhej7KMoE3B-w=='
    port=3306
    charset='utf8'
    return host,user,password,database,port,charset

def db_airSit():
    '''
    数据库连接信息
    :return:
    '''
    host='gAAAAABmyqBu2QbIufRSgWHb-SYKGqYFmFXK6qYRx6xRhfm1p3CYQ4odJVNFcz1xYyS5xiKaUCP4HZJc_E20MuXvHY2BN6ACoPAB9D39mMsE-gTAjrDf2XQ='
    user='gAAAAABmyqBuv33KcS3QOiz3qJccehTwZ7ph8v6yYaVyVrcij0R6BK07d7Q1nzUtEwFVQPzUSqvDhWMw5FtfitIPNQQ6PWRV7w=='
    password='gAAAAABmyqBuaSBc7sqbDcjGP0Vcw2SbIZoJTkYoU_rgtHAz9K464vbTOLrO6wqe34af94dl4EWCGcOfu3XthxEH8SNypFh4lQ=='
    database='gAAAAABmyqBuxTK6OARZzH0ixgG7CLmhgKxo5iEMG1hOBk0PmqHKuXyVRBmuhZLEuhHe9WDN10jNu2FLaR7CC6gVNvc5_YtP7A=='
    port=3306
    charset='utf8'
    return host,user,password,database,port,charset


def db_di():
    '''
    数据库连接信息
    :return:
    '''
    host='gAAAAABm0perEA39M2JsWEzsxl87OE7DFDFmF9cmkaFFefm7H8JuG2G9bezzRvdSXF1koTjx_kV7t4aPiH4wbAu0uPzhQN3hpkLdKPt7F_XL3dXh_yCm-jE='
    user='gAAAAABm0perpVk5CVJe_G68xCLkAyJQQ3bkzCLkyT7YANLAYG6P573p8NRudN7J8y4JWfPXbtOHlUC_2AV7OqMBWrqqFNoAZQ=='
    password='gAAAAABm0perAheW7O0lq1CJETNyYNu86WhoQN736NwM7lW1zI5L7eoBQ3cBh3--J-n4sOL2ckcTFkXvp3I54-qwj3Yl524rbQ=='
    database='gAAAAABm0per_6KoSHVZhMLV_ntBd2WGtW9pNz3F_s9uOrXqpFGcaxVpDr1ZqPiqUuzHdvGIn-qjK2UUzfC-mQDwATx2U8Eg2A=='
    port=3306
    charset='utf8'
    return host,user,password,database,port,charset

def db_diTest():
    '''
    数据库连接信息
    :return:
    '''
    host='gAAAAABm0pgOp0dda0adiEYo9w0WzAFl56Od8oN_tGrmjloN-E4-btxSW7fdrVsE7NLAO_X_7OdmzZfsB_NcqGEk888X_S7ICnZjYjZoK4f8m9h-0cbVIb8='
    user='gAAAAABm0pgOrvVpRrnrMB51McTS9S4UxL1gvhWWerqxJ5oHF7gOPQDv5oY6CkHEhr3PoSBB2j-iBwKP7WDd49VWuSIuNpuKAg=='
    password='gAAAAABm0pgOItef3KLy-r4f0YltxiUWfRch-Ly7LqDn_e5qy_7QT4cnBz4JLjKIEdjstaPKYk46CuExvArnMCBDwFx3g4yDBQ=='
    database='gAAAAABm0pgO3ycobaeftu3_2NwzQrncIfmAxvKBdTBZfaqleezSXFlr-ro-qt0xhxhWGNPFdIenMi9oxearOTW0VheRFGqiIQ=='
    port=3306
    charset='utf8'
    return host,user,password,database,port,charset


def db_costbase():
    '''
    数据库连接信息
    :return:
    '''
    host = 'gAAAAABm0pjRQlTi4lKbeGCRiZb0Ka88K7Rg9T68umKADiAHip4OZ7vS3jwbwWGqgTqncohcxB1F0BHtIwnHg58sGYzaO2Bl7v8hEWdhMXjXJnmYICxxOYu8toiLzNbrrDv8Ob_QZGMz'
    user = 'gAAAAABm0pjRdGRrtT6sDGW5oyFftH-zYbDUq3JyDIBaKQ1QSOMHSk7PltEF2-NyYskNi9q3UoLskjEXeJCeTqUS-qKfT73BvA=='
    password = 'gAAAAABm0pjRyWSyhIhbGa8umEPLmyIKqwrhlSG0C1q1hLtc0aQD1Wtu_Jpl4SAme_V10493OKxQRwheOdEVaZrnTA6Co3CqXQ=='
    database = 'gAAAAABm0pjR0kXpBBRGEzMdGorD7Niww1kGcUlIaESt6zOeRwjcA0KnX_jQbFVycsnwnOkEsOW3-wru0yE5SxB-ZDsOBfBSbg=='
    port = 3306
    charset = 'utf8'
    return host, user, password, database, port, charset

def db_atms():
    '''
    数据库连接信息
    :return:
    '''
    host = 'gAAAAABm0pknRp5kkc-bhKE0spzIAdQ93OWpv9CyRDU09eSgND1oLgkbrA8SSqs8AHD08vtN_iTUhP3jbkt6bTlfTG-gefAd9WtRB02H0q52xvVVgQmSlwQomCK2NRjgpRoNRRyXI24d'
    user = 'gAAAAABm0pknUEHO7wizNjMwnh_2nx2c1_I7L7ZE7P_r1qqHatKlBj2H13wBJmTkNFkaaNhTbsGp92R7qxDo-DfklYypbc9Sqw=='
    password = 'gAAAAABm0pknNhLhbX_kwmF8khzQ2aYdgtn0jNFkB2Ushgv-TmT0TduJh1v187uu-QZZXDUEtY3DPgl4_3v-EHyBUB0QUsP1tA=='
    database = 'gAAAAABm0pknvpwH_yhTUEkyneutlu8D2PP1jwq5D929mkwe-d8bO7G82JLKqiTowvXhIdwTLjCGugJwf5877BNS3N74WPc1pQ=='
    port = 3306
    charset = 'utf8'
    return host, user, password, database, port, charset

def db_report():
    '''
    数据库连接信息
    :return:
    '''
    host = 'gAAAAABm0pmDJST2dT5tef76_6S-BvM-CnlDKV4nI_iM7fYBW74sAF4CMLIOfbFXdtKHt0khNTtSQL1aUXuYo9z-FwQ8uF708RbZt8np1WSWR_VMrpDb8Js='
    user = 'gAAAAABm0pmD_fbhiiI8ymzk3o4t0-49_c73XIqbnrLc-jki57hD0rjwyYcaQX04KEpVfeMo9u4Vog1rzDdftf1W7ZnY5N_e1Q=='
    password = 'gAAAAABm0pmDN90mRnP9UhG6uvuTGgcmdGm4df3Y9WgHrRZnE7T-Id4qLfwh8Lu_B6MyjCSMihOZUZq2jKng_03e2V95qk__zg=='
    database = 'gAAAAABm0pmD5gLfYUPQaBvrxeGZf6lQnXy0XqTaxQTLWUYxhI_5q3z3KOURw4i_3pyGGDixNz_tMIVGSbE7SLl_lrZqz57XHQ=='
    port = 3306
    charset = 'utf8'
    return host, user, password, database, port, charset


def db_uranus():
    '''
    数据库连接信息
    :return:
    '''
    host = 'gAAAAABm0ppANy_VpTED7of6dR2iPkF36g0X3-l3s4nObTVmRSqddcHCK_9vBc65Ya83B2e2hIrzClr0C45ah2kii5URzvOnlv15oRVQ_lFFl7JsTLl0YUk='
    user = 'gAAAAABm0ppAHQKTgTlmfxMV1khbpWYLRn9n4RBXHy7v2bwW9BKFqa3OiX1BHoHZ_1uPkKCAqQ8d7ZByfICoaLPObaPEJQQyRw=='
    password = 'gAAAAABm0ppAYLXrcdz-LyLkDicV90ts1-liUVe60JMyasuOj1EI4EGKKON82ddP6JAygCj-fvOXGDyUTBJEScLsutTOikPoRw=='
    database = 'gAAAAABm0ppAt-hgk2hfS5JfaZk0-GQULrUapsnLIgDdwajP1vuf30vJk2_Yt6gJTMVoFuUAutBLorZYC10S6UC-l6eF1uQyIg=='
    port = 3306
    charset = 'utf8'
    return host, user, password, database, port, charset

def db_requirement():
    '''
    数据库连接信息
    :return:
    '''
    host = 'gAAAAABm0prg0v2hf2vH0itFbSpBwVdDyaV4yqNPpKMBqlfLLInIWePDGvkVVTGwLSoNxqDm4DWntVb00BipLbjQyXHZ6hq9L_LsP04z1HTznYL78v5xNFBrv5rReM4r-o6-FOJMTE9l'
    user = 'gAAAAABm0prgMrGhsQq1qnPe-xiZ9zoN4W8IlLHvAvkhzayvrrBuYour6mFVoIWSgxqUrmKVq4oPTBOOdiwcpkMLcYCnqWZSrQ=='
    password = 'gAAAAABm0prg-I5FRIrnx9oJCevitV3ZBuZMR23W8AuYtZcVoekbPavPfLBtyk2fkKEWPTu6M2YFz1IwewW9SXvAVAfF6NTxBQ=='
    database = 'gAAAAABm0prgxbJ20XaZl8-iWbSzT9Dm6v5nmfJkuvQp_OXgZWsY-ewJBBiJy3z3TnCWpcIePFpVn7sXKF_-2mV1wrhTpu0H9g=='
    port = 3306
    charset = 'utf8'
    return host, user, password, database, port, charset

def db_aviation():
    '''
    数据库连接信息
    :return:
    '''
    host = 'gAAAAABm0psqJcsVBL0imBVMBUT8WERNxgFTSssZMaAxGsA3svut19qBQDrlAHX_HFAOMc5yR_u66fcItTp_VLpk58suuP5eKvous0QwfqwZeZNrWkVTu89HB-nosIxD7Pggk6SQfDN7'
    user = 'gAAAAABm0psqzFxZSr41pruNEkXsTeDgzkqV9V6tlPl6V4ttreydi2Vv5XyBPwfdCfgLV-tRNE1S5DpLiIJxxiX1r0Uj6mToxA=='
    password = 'gAAAAABm0psqSyyyqoNGwFq3C6ly3dfX2ylrLG263QftKR3CzlQajI2k83-iGRWFWVy4o7mkofeCmzh4TKg4sB63bYGe5YxinA=='
    database = 'gAAAAABm0psqJEXnzbj8oWxJ7xnF4NSUwJty3DSLtooMD_YHXg1I98YumjCcbXuX_0sZSdrAL1mWkx9Lpm8qxb6JJ_2_ztt32A=='
    port = 3306
    charset = 'utf8'
    return host, user, password, database, port, charset

def db_airResource():
    '''
    数据库连接信息
    :return:
    '''
    host = 'gAAAAABm0puPl4rOiNnKX2IQkSxeLJ-aZnF9kR5B0JKY_AwxLJUHkikMNE-T96j2Z4sys7nyTAOo6G8fWwXJxjWFFP-MhStjFvaRK_VZuynZw0qnllYtPvDw11FdkNZa-Jr5-k2osYO4'
    user = 'gAAAAABm0puPx9yoi_jy3Qj-60idIIst0ty7eOuatB9JZ5FiUC8CPqWEJsNs6UcLdNh18ciqb_9kxe41MuntdQhbssjHEA68Nw=='
    password = 'gAAAAABm0puP7gzEX7RoGu4khj3XciDO70M0XrzXj3txFD_LBQgp7GAILDeYblhttbCxArsbaTBz7hWYI_yqZqw39QTCEthiCQ=='
    database = 'gAAAAABm0puPHZ5Xo_Eyh_TMP4M1Bt0os1JxyvJPc1qjcjwY6xqJMy5Xu44NpYfHiigF90lE0GilgL8T_-yLVQmDoYVn5BkH5Q=='
    port = 3306
    charset = 'utf8'
    return host, user, password, database, port, charset





