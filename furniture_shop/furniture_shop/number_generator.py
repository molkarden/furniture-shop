import random
from typing import Iterator, List


def generate_numbers(count: int = 10, start: int = 1, end: int = 100) -> List[int]:
    """Generate a list of random integers."""
    return [random.randint(start, end) for _ in range(count)]


def generate_sequence(start: int = 1, step: int = 1) -> Iterator[int]:
    """Generate an infinite arithmetic sequence of integers."""
    current = start
    while True:
        yield current
        current += step


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate numbers.")
    parser.add_argument("--count", type=int, default=10, help="Number of random numbers to generate.")
    parser.add_argument("--start", type=int, default=1, help="Start of range or sequence.")
    parser.add_argument("--end", type=int, default=100, help="End of random range.")
    parser.add_argument("--step", type=int, default=1, help="Step for generated sequence.")
    parser.add_argument("--mode", choices=["random", "sequence"], default="random", help="Generation mode.")

    args = parser.parse_args()

    if args.mode == "random":
        numbers = generate_numbers(count=args.count, start=args.start, end=args.end)
        print("Generated random numbers:")
        print(numbers)
    else:
        seq = generate_sequence(start=args.start, step=args.step)
        print("Generated sequence:")
        for _ in range(args.count):
            print(next(seq))
