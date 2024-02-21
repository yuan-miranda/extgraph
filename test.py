import math

val = 100
val_len = len(str(val))
zero = "1"
for i in range(val_len):
    zero += "0"

# round_val = math.ceil(val / int(zero)) * int(zero)

print(int(zero))