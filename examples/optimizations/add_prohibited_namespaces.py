from sedai.optimizations import prohibited_namespaces

def add_prohibited_namespaces(namespaces):
    updated_namespaces = prohibited_namespaces.add_prohibited_namespaces(namespaces)
    if updated_namespaces is not None:
        print("Prohibited namespaces: ")
        for i in updated_namespaces:
            print(i)



if __name__ == '__main__':
    namespaces = ["example1", "example2"]
    add_prohibited_namespaces(namespaces)