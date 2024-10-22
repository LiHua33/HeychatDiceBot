import random as rd

def dn(N:int)->int:
    result = int(N*rd.random() + 1)
    return result

def Ndn(doseN:int, n:int)->str:
    result_list = []
    for _ in range(doseN):
            num = dn(n)
            result_list.append(num)
    str = "Dice result: {}".format(result_list)
    print(str)
    return result_list

if __name__ == "__main__":
    print(Ndn(2, 0))