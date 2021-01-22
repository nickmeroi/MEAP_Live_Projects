import operator
from itertools import chain, combinations

hours_in_day = 8

# task name: (blocks, total task time in minutes)
tasks = {'email': (3, 60),
         'meeting': (2, 60),
         'coding': (1, 300),
         'lunch': (1, 50),
         'training': (2, 120)
         }


def powerset(iterable):
    """
        Get 'all' possible combinations including single tasks/blocks combinations
    """
    s = list(iterable)

    return list(filter(None,
                       chain.from_iterable(combinations(iterable, r) for r in range(len(s)+1))
                       ))


def blocks(task_blocks):
    """
        Get expanded list of task broken down into the possible blocks for those task
        and time allocated to each block
    """

    return [{key: round((item[1]/item[0])/60, 2)}
            for key, item in task_blocks.items()
            for block in range(item[0])]


def block_combinations(task_blocks):
    return list(powerset(task_blocks))


def candidate_combination(tasks_combo):
    """
            Get list of potential winning tasks:
                - The total length of time that the subset of tasks takes must fit in the day
                - The the total length of time that the subset of tasks takes leaves
                  the smallest amount of free time left over at the end of the day
    """
    candidate_tasks = []

    for combo in tasks_combo:
        blocks_set = tuple(chain.from_iterable(combo))
        total_time = sum([sum(list(sub.values())) for sub in combo])
        if total_time <= hours_in_day:
            candidate_tasks.append((hours_in_day - total_time, blocks_set))

    return [min(candidate_tasks, key=operator.itemgetter(0)), ]


def main():

    # expanded tasks
    all_blocks = blocks(tasks)
    # all tasks combinations
    all_blocks_combinations = block_combinations(all_blocks)
    # candidate combinations that meet the "time left" criteria
    candidate_combinations = candidate_combination(all_blocks_combinations)

    # display the "winning" tasks combinations
    for i, one_candidate_combination in enumerate(candidate_combinations, 1):
        print(f'Candidate Combination ID: {i}\n\t'
              f'Time Left: {one_candidate_combination[0]}\n\t'
              f'Blocks: {", ".join(one_candidate_combination[1])}')


if __name__ == '__main__':
    main()
