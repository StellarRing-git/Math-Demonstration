x=1

def func():
    x=3
    print("func")
    return x

while True:
    x=func()


    if x==3:
        print("yay")
        print(x)
        break
    else:
        print("no")
        print(x)
        break