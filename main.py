import importlib
import sys
import pdoc

def main():
    mod_name = sys.argv[1]
    mod = importlib.import_module(mod_name)
    
    doc = pdoc.doc.Module(mod)
    
    for key, val in doc.members.items():
        print(type(val))
        print(f"{key} -- {val}")


if __name__ == "__main__":
    main()
