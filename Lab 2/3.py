def exercise_3(a, b):
    print(a[0 : b] + [i * i for i in a[b :]])

exercise_3([int(i) for i in input().split()], int(input()))