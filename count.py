import pickle


def main():
    print("Hello world")
    hunks_arr = pickle.load(open("dumps/hunks_array.pkl","rb"))
    print(len(hunks_arr))
if __name__=='__main__':
    main()