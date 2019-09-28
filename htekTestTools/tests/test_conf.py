from data.conf import *


def _get_p_value_of_lk(line: int):
    lk_type = 'linekey%s' % line
    lk_type_pv = line_key_dir[lk_type]['type']
    print(lk_type_pv)


_get_p_value_of_lk(11)
