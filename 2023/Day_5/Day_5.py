file = open("input", 'r')
lines = file.readlines()
lines.append('\n')  # for detection of the end of the last map

# part 1

# extract seeds:
seeds = [int(seed) for seed in lines[0].removesuffix('\n').split(":")[1].split()]
num_seeds = len(seeds)

source = []
destination = seeds.copy()

map_processing = False
for line_idx, line in enumerate(lines):

    if not map_processing:
        if "map" in line:
            map_processing = True
            source = destination.copy()
            destination = []
            continue
        else:
            continue
    else:
        if line == "\n":  # end of map portion (or last line of input)
            map_processing = False
            destination += source
        else:
            # mapping line
            destination_range_start, source_range_start, range_length = [int(value) for value in
                                                                         line.removesuffix('\n').split()]

            source_entries_to_remove = []
            for source_entry in source:
                if source_entry in range(source_range_start, source_range_start + range_length):
                    source_entries_to_remove.append(source_entry)
                    destination.append(destination_range_start + source_entry - source_range_start)
            for source_entry in source_entries_to_remove:
                source.remove(source_entry)

print(f"part 1: {min(destination)}")


# part 2

class mapp:
    source_start = 0  # inclusive
    source_end = 0  # exclusive
    destination_start = 0  # inclusive
    offset = 0
    range_length = 0
    range = range

    def print(self):
        print(
            f"\tsource start: {self.source_start}\n\tdestination start: {self.destination_start}\n\tlength: {self.range_length}")


def splitsource(source_to_split: range, value):
    if source_to_split.start == value:  # no split needed
        return [source_to_split]
    else:
        return [range(source_to_split.start, value), range(value, source_to_split.stop)]


seed_input = [int(seed) for seed in lines[0].removesuffix('\n').split(":")[1].split()]
seed_ranges = []

for i in range(0, len(seed_input), 2):
    seed_ranges.append(range(seed_input[i], seed_input[i] + seed_input[i + 1]))

destination_ranges = seed_ranges.copy()

map_processing = False
map_set = []

for line_idx, line in enumerate(lines):

    if not map_processing:
        if "map" in line:
            map_processing = True
            source_ranges = destination_ranges.copy()
            destination_ranges = []
            map_set = []
            continue
        else:
            continue
    else:
        if line == "\n":  # end of map portion (or last line of input)

            # for map in map_set:
            #     map.print()
            #     print()

            # print("end of map")

            # check for source ranges with map borders
            unchecked_sources = source_ranges.copy()
            checked_sources = []
            while unchecked_sources:
                source_split = False
                current_source = unchecked_sources.pop()

                for map in map_set:
                    if map.source_start in current_source and map.source_start != current_source.start:
                        unchecked_sources += (splitsource(current_source, map.source_start))
                        source_split = True
                        break
                    if map.source_end in current_source and map.source_end != current_source.start:
                        unchecked_sources += (splitsource(current_source, map.source_end))
                        source_split = True
                        break

                if not source_split:
                    checked_sources.append(current_source)

            # print("checked sources")
            # print(checked_sources)

            for current_source in checked_sources:
                source_mapped = False
                for map in map_set:
                    if current_source.start in map.range:
                        destination_ranges.append(range(current_source.start+ map.offset, current_source.stop + map.offset))
                        source_mapped = True
                        break

                if not source_mapped:
                    destination_ranges.append(current_source)

            # print("destination")
            # print(destination_ranges)
            map_processing = False

        else:
            # mapping line
            destination_range_start, source_range_start, range_length = [int(value) for value in
                                                                         line.removesuffix('\n').split()]
            new_map = mapp()
            new_map.source_start = source_range_start
            new_map.source_end = source_range_start + range_length
            new_map.destination_start = destination_range_start
            new_map.range_length = range_length
            new_map.offset = destination_range_start - source_range_start
            new_map.range = range(source_range_start, source_range_start + range_length)

            map_set.append(new_map)

print(f"part 2: {min([location_range.start for location_range in destination_ranges])}")