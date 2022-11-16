import copy


class Item:
    def __init__(
            self,
            long_name: str = 'NA',  short_name: str = '_',
            weight: int = 0, points: int = 0
    ):
        self.points = points
        self.weight = weight
        self.long_name = long_name
        self.short_name = short_name


class Knapsack:
    def __init__(self, size: (int, int) = (3, 3), start_points: int = 10):
        self.size = size
        self.max_capacity = size[0] * size[1]
        self.weight = 0
        self.total_points = start_points
        self.items = list()

    def print(self):
        print(f'score: {self.total_points}')

        s_items = list()
        for itm in self.items:
            s_items += [itm.short_name for _ in range(itm.weight)]
        s_items += ['_' for _ in range(self._get_free_capacity())]

        for row_i in range(self.size[1]):
            print(f'[{"],[".join(s_items[row_i * self.size[0]:(row_i + 1) * self.size[0]])}]',
                  end='')
            print((',', '')[row_i == self.size[1] - 1])

    def _get_free_capacity(self):
        return self.max_capacity - self.weight

    def put_item(self, item_obj: Item):
        if item_obj.weight > self._get_free_capacity():
            raise ValueError('You crashed a knapsack!')
        self.items.append(item_obj)
        self.total_points += item_obj.points
        self.weight += item_obj.weight

    def dont_put_item(self, item_obj: Item):
        self.total_points -= item_obj.points

    def dont_put_items(self, item_lst: list[Item]):
        for itm in item_lst:
            self.total_points -= itm.points

    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        obj.items = self.items.copy()
        return obj


def print_kpk_solution(
        width: int, height: int, score: int, all_items: list[tuple[str, str, int, int]]
):
    items_list = [None] + [
        Item(*data) for data in all_items
    ]
    dp_mtx_knapsacks = list()

    for curr_item_i, item in enumerate(items_list):
        dp_mtx_knapsacks.append(list())

        for capacity in range(width * height + 1):
            if item is None or capacity == 0:  # first line or column
                dp_mtx_knapsacks[-1].append(Knapsack(size=(width, height), start_points=score))
                if capacity == 0:  # first column
                    dp_mtx_knapsacks[-1][-1].dont_put_items(items_list[1:curr_item_i + 1])
                continue

            dont_put_kpk = dp_mtx_knapsacks[-2][capacity]
            dont_put_score = dont_put_kpk.total_points - item.points
            put_score = None
            # if there are enough space for current item
            if item.weight <= capacity:
                put_kpk = dp_mtx_knapsacks[-2][capacity - item.weight]
                put_score = item.points + put_kpk.total_points
                # we put current item if it's better choice
                if put_score >= dont_put_score:
                    dp_mtx_knapsacks[-1].append(copy.copy(put_kpk))
                    dp_mtx_knapsacks[-1][-1].put_item(item)
                else:  # use None put_score as 'do not put' flag
                    put_score = None
            # else we don't put current item
            if put_score is None:
                dp_mtx_knapsacks[-1].append(copy.copy(dont_put_kpk))
                dp_mtx_knapsacks[-1][-1].dont_put_item(item)

    print('DP TABLE\n    ', end='')
    for i in range(width * height + 1):
        print(f'{i:>5}', end='')
    for ln_i, ln in enumerate(dp_mtx_knapsacks):
        if ln_i == 0:
            print('\nnone ', end='')
        else:
            print(f'{all_items[ln_i - 1][2]} {all_items[ln_i - 1][3]:>2} ', end='')
        for kpk in dp_mtx_knapsacks[ln_i]:
            print(f'{kpk.total_points:>5}', end='')
        print()

    print(f'\nBASE SOLUTION')
    win_kpk = dp_mtx_knapsacks[-1][-1]
    win_kpk.print()

    positive_solutions = list()
    for kpk in dp_mtx_knapsacks[-1][::-1]:
        if kpk.total_points > 0:
            positive_solutions.append(kpk)
    if len(positive_solutions) > 0:
        print('\nALL POSITIVE SOLUTIONS')
        for kpk in positive_solutions:
            kpk.print()


if __name__ == '__main__':
    items_data = [
        ('Винтовка', 'в', 3, 25),
        ('Пистолет', 'п', 2, 15),
        ('Боекомплект', 'б', 2, 15),
        ('Аптечка', 'а', 2, 20),
        ('Ингалятор', 'и', 1, 5),
        ('Нож', 'н', 1, 15),
        ('Топор', 'т', 3, 20),
        ('Оберег', 'о', 1, 25),
        ('Фляжка', 'ф', 1, 15),
        ('Антидот', 'д', 1, 10),
        ('Еда', 'к', 2, 20),
        ('Арбалет', 'р', 2, 20)
    ]
    print('>>> BASE TASK SOLUTION <<<')
    print_kpk_solution(
        width=3,
        height=3,
        score=10,
        all_items=items_data
    )
    print('\n\n>>> 7-CELLS KNAPSACK SOLUTION <<<')
    print_kpk_solution(
        width=7,
        height=1,
        score=10,
        all_items=items_data
    )
    print('As result: we can\'t get a solution on these items set.')
