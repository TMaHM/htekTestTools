def basic_call(phone_a, phone_b):
    cnt_success = 0
    failed_list = []
    if phone_a.dial(phone_b.ext) == 200:
        cnt_success += 1
    else:
        cnt_success -= 1
        failed_list.append('phone_a failed.')
    if phone_b.answer('f1') == 200:
        cnt_success += 1
    else:
        cnt_success -= 1
        failed_list.append('phone_b failed.')

    if cnt_success == 2:
        return True
    else:
        return failed_list


def transfer_flow(phone_a, phone_b, phone_c):
    phone_a.dial(phone_b.ext)
    phone_b.transfer(phone_c)