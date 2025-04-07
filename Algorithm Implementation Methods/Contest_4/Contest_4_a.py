def main(q):
    inputs, outputs = {}, {}
    for i in range(q):
        old, new = input().strip().split()
        if old in outputs:
            initial = outputs[old]
            inputs[initial] = new
            del outputs[old]
            outputs[new] = initial
        else:
            inputs[old] = new
            outputs[new] = old
    
    print(len(inputs))

    for i, j in inputs.items():
        print(f'{i} {j}')


if __name__ == '__main__':
    q = int(input())
    main(q)