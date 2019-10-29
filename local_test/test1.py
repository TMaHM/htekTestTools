from PhoneLib.htek_phones import Phone



test = Phone('10.3.3.18', '2054', line=3)
test2 = Phone('10.3.2.123', '412', line=1)

for number in test2.ext:
    test.press_key(number)
