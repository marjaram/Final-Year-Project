import greedypacker

M = greedypacker.BinManager(8, 4, pack_algo='shelf', heuristic='best_width_fit', wastemap=True, rotation=True)

ITEM = greedypacker.Item(4, 2)

ITEM2 = greedypacker.Item(5, 2)

ITEM3 = greedypacker.Item(2, 2)

M.add_items(ITEM, ITEM2, ITEM3)

M.execute()

M.bins
