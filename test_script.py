final_list = ['B>A', 'C<A', 'D>B']
# final_list = ['C>B', 'D<B', 'A>C']
# final_list = ['D>A', 'A>C', 'B<C']
# final_list = ['B<A', 'C>A', 'D>C']
# final_list = ['B>A', 'C<A', 'D>B']

weight = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

l2 = []
for item in final_list:
    if '<' in item:
        item_elems = item.split('<')
        new_item = item_elems[1] + '>' + item_elems[0]
    else:
       new_item = item
    l2.append(new_item)


gt_dict = {item.split('>')[0]: item.split('>')[1] for item in l2}
gt_str = '>'.join(list(gt_dict.items())[0])
print(gt_str)
gt_str += '>' + gt_dict[gt_str.split('>')[-1]]
print(gt_str)
# gt_str += '>' + gt_dict[gt_str.split('>')[-2]]

i = 4
for item in l2:
    weight[(item.split('>')[0])] = i
    weight[(item.split('>')[1])] = i - 1
        



# res = l2[2] + '>' + l2[1]

# gt_str += '>' + gt_dict[gt_str.split('>')[-1]]


print(weight)



print(final_list)
print(l2)
print(gt_dict)
print(gt_str)
# print(res)
