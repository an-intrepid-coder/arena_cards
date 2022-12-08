import random
import curses

def generate_fuzzed_value(base, fuzz_multiplier):
        val = base
        fuzz_max = int(val * fuzz_multiplier)
        fuzz_value = random.randrange(0, fuzz_max)
        negative_fuzz = random.randrange(0, 2) == 0
        if negative_fuzz:
            fuzz_value *= -1
        val += fuzz_value
        return val

