import argparse
import json

from generators import (
    generate_arithmetic,
    generate_combination,
    generate_comparison,
    generate_figure,
    generate_numbers,
    generate_ordering,
)


def generate_to_file(path='template_dataset.json', num_per_class=1):
    results = generate(num_per_class)
    json.dump(results, open(path, 'w'), ensure_ascii=False, indent=2)


def generate(num_per_class=1):
    results = []

    # Choose proper ratio between class
    print('Generating arithmetic')
    arithmetic_samples = generate_arithmetic(int(num_per_class))
    print('Generating numbers')
    numbers_samples = generate_numbers(num_per_class)
    results.extend([{
        'code': model_output,
        'text': question,
        'answer': answer,
        'q_type': q_type,
    } for question, model_output, code, answer, q_type in arithmetic_samples + numbers_samples])

    for func in [generate_ordering, generate_comparison, generate_figure, generate_combination]:
        print(f'Generating {func.__name__}')
        results += [{
            'code': model_output,
            'text': question,
            'answer': answer,
        } for question, model_output, code, answer in func(num_per_class)]

    print(f"finished generating total of {len(results)}", results[0], sep='\n')
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Korean Math Word Problem Python")
    parser.add_argument("-o", "--output", type=str, default="problem.json", help="Output file to write generated data")
    parser.add_argument("-n", "--num_per_class", type=int, default=1, help="Number of data to generate for each class")
    args = parser.parse_args()
    generate_to_file(args.output, args.num_per_class)
