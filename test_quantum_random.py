
from matplotlib import pyplot as plt

from quantum_random import QuantumRandom


def test_quantum_random_integers():
    """
    Rigorous test for the randint function.
    """
    mini, maxi, num_iter = 1, 100, 100000
    q = QuantumRandom()
    samples = [q.randint(mini, maxi) for _ in range(num_iter)]
    frequencies = {i: samples.count(i) for i in range(mini, maxi + 1)}
    print("Integer Test Frequencies:", frequencies)

    plt.hist(samples, bins=[i + 0.5 for i in range(maxi)],
             align='mid', rwidth=0.8)
    plt.xticks(list(range(mini, maxi + 1)))
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(
        f'Distribution of QuantumRandom.randint({mini}, {maxi}) over {num_iter} samples')
    plt.show()


def test_quantum_random_uniform():
    """
    Rigorous test for the uniform function.
    """
    q = QuantumRandom()
    samples = [q.uniform(0, 1) for _ in range(100000)]

    # Print frequencies
    frequencies = {}
    for s in set(samples):
        frequencies[s] = samples.count(s)
    print("Uniform Test Frequencies:", frequencies)

    plt.hist(samples, bins=100, align='mid', rwidth=0.8)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Distribution of QuantumRandom.uniform(0, 1) over 100,000 samples')
    plt.show()


def test_quantum_random_randrange():
    """
    Rigorous test for the randrange function.
    """
    q = QuantumRandom()
    start, stop, step = 1, 100, 5
    num_iter = 100000
    samples = [q.randrange(start, stop, step) for _ in range(num_iter)]

    # Print frequencies
    frequencies = {}
    for s in set(samples):
        frequencies[s] = samples.count(s)
    print("Randrange Test Frequencies:", frequencies)

    plt.hist(samples, bins=range(start, stop + 1, step),
             align='mid', rwidth=0.8)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(
        f'Distribution of QuantumRandom.randrange({start}, {stop}, {step}) over {num_iter} samples')
    plt.show()


def test_quantum_random_choice_and_choices():
    """
    Rigorous test for the choice and choices functions.
    """
    q = QuantumRandom()
    sequence = [1, 2, 3, 4, 5]
    num_iter = 100000
    single_choices = [q.choice(sequence) for _ in range(num_iter)]
    multiple_choices = q.choices(sequence, k=3)
    print(
        f"Single choice frequencies: {[(i, single_choices.count(i)) for i in sequence]}")
    print(
        f"Multiple choices frequencies: {[(i, multiple_choices.count(i)) for i in sequence]}")


def test_quantum_random_shuffle():
    """
    Rigorous test for the shuffle function.
    """
    q = QuantumRandom()
    sequence = list(range(10))
    positions = {i: [0] * len(sequence) for i in sequence}
    num_iter = 100000
    for _ in range(num_iter):
        shuffled = sequence.copy()
        q.shuffle(shuffled)
        for idx, val in enumerate(shuffled):
            positions[val][idx] += 1
    print(f"Position frequencies after {num_iter} shuffles: {positions}")


def test_quantum_random_sample():
    """
    Rigorous test for the sample function.
    """
    q = QuantumRandom()
    sequence = list(range(10))
    num_samples = 5
    num_iter = 100000
    frequencies = {i: 0 for i in sequence}
    for _ in range(num_iter):
        for val in q.sample(sequence, num_samples):
            frequencies[val] += 1
    print(
        f"Frequencies after {num_iter} samples of size {num_samples}: {frequencies}")


def test_quantum_random_random():
    """
    Rigorous test for the random function.
    """
    q = QuantumRandom()
    num_iter = 100000
    samples = [q.random() for _ in range(num_iter)]
    plt.hist(samples, bins=100, align='mid', rwidth=0.8)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(
        f'Distribution of QuantumRandom.random() over {num_iter} samples')
    plt.show()


if __name__ == "__main__":
    # test_quantum_random_integers()
    # test_quantum_random_uniform()
    test_quantum_random_randrange()
    # test_quantum_random_choice_and_choices()
    # test_quantum_random_shuffle()
    # test_quantum_random_sample()
    # test_quantum_random_random()
