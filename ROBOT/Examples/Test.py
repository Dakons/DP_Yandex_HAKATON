name = "drive"
values = [12, 23, 44]
command = " ".join([name] + list(map(str, values)))
print(" ".join(command))
name, *values = command.split(" ")
print(name, values)