def exercise_2(a):
    for i in range(0, len(a), 2):
        print(a[i])

exercise_2([int(i) for i in input().split()])