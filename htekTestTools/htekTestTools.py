def basic_call(phone_a, phone_b):
    phone_a.dial(phone_b.ext)


def transfer_flow(phone_a, phone_b, phone_c):
    phone_a.dial(phone_b.ext)
    phone_b.transfer(phone_c)