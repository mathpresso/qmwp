import json

from generators import (
    generate_arithmetic,
    generate_combination,
    generate_comparison,
    generate_figure,
    generate_numbers,
    generate_ordering,
)


def generate_to_file(path='template_dataset.json', num_per_class=10_000):
    results = generate(num_per_class)
    json.dump(results, open(path, 'w'), ensure_ascii=False, indent=2)


def generate(num_per_class=10_000):
    results = []

    # Choose proper ratio between class
    print('Generating arithmetic')
    arithmetic_samples = generate_arithmetic(int(1.5 * num_per_class))
    print('Generating numbers')
    numbers_samples = generate_numbers(3 * num_per_class)
    results.extend([{
        'code': model_output,
        'text': question,
        'answer': answer,
    } for question, model_output, code, answer in arithmetic_samples + numbers_samples])

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
    generate(10)