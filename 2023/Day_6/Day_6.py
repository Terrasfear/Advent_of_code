import math

file = open("input", 'r')
lines = file.readlines()

Times_str = lines[0].split(":")[1].split()
Times = [int(time) for time in Times_str]

Time_kerned = int("".join(Times_str))

Distances_str = lines[1].split(":")[1].split()
Distances = [int(time) for time in Distances_str]

Distance_kerned = int("".join(Distances_str))

# Part 1
Num_winning_options = []
for idx in range(len(Times)):
    Race_duration = Times[idx]
    Target_distance = Distances[idx]

    Hold_times = [Race_duration / 2 - 0.5 * math.sqrt(Race_duration**2 - 4 * Target_distance),
                  Race_duration / 2 + 0.5 * math.sqrt(Race_duration**2 - 4 * Target_distance)]

    if Hold_times[0].is_integer():
        Hold_times[0] = Hold_times[0] + 1
    else:
        Hold_times[0] = math.ceil(Hold_times[0])

    if Hold_times[1].is_integer():
        Hold_times[1] = Hold_times[1] - 1
    else:
        Hold_times[1] = math.floor(Hold_times[1])

    Num_winning_options.append(Hold_times[1] - Hold_times[0] + 1)

print(f"part 1: {math.prod(Num_winning_options)}")

# Part 2
Hold_times = [Time_kerned / 2 - 0.5 * math.sqrt(Time_kerned**2 - 4 * Distance_kerned),
              Time_kerned / 2 + 0.5 * math.sqrt(Time_kerned**2 - 4 * Distance_kerned)]

if Hold_times[0].is_integer():
    Hold_times[0] = Hold_times[0] + 1
else:
    Hold_times[0] = math.ceil(Hold_times[0])

if Hold_times[1].is_integer():
    Hold_times[1] = Hold_times[1] - 1
else:
    Hold_times[1] = math.floor(Hold_times[1])

Num_winning_options = Hold_times[1] - Hold_times[0] + 1

print(f"Part 2: {Num_winning_options}")
