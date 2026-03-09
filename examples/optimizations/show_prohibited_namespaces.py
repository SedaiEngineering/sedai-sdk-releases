from sedai.optimizations import prohibited_namespaces

def show_prohibited_namespaces():
    prohibited_namespaces_list = prohibited_namespaces.get_prohibited_namespaces()
    if prohibited_namespaces_list is not None:
        print("Prohibited namespaces: ")
        for i in prohibited_namespaces_list:
            print(i)


if __name__ == '__main__':
    show_prohibited_namespaces()