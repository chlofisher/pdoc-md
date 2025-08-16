import importlib
import sys
import pdoc
import pdoc.doc


def main():
    mod_name = sys.argv[1]
    mod = importlib.import_module(mod_name)
    doc = pdoc.doc.Module(mod)
    # crawl_recursive(doc)
    crawl(doc)


def crawl_recursive(doc):
    if not isprivate(doc):
        print(f"{doc.kind} :: {doc.fullname}")

    if not isinstance(doc, pdoc.doc.Namespace):
        return

    for name, member in doc.members.items():
        crawl_recursive(member)


def crawl(doc):
    stack = [doc]
    depth_stack = [0]

    while len(stack) > 0:
        curr_doc = stack.pop(-1)
        curr_depth = depth_stack.pop(-1)

        if not isprivate(curr_doc):
            print(f"{"  " * curr_depth}{curr_doc.kind} :: {curr_doc.fullname}")

        if not isinstance(curr_doc, pdoc.doc.Namespace):
            continue

        members = list(curr_doc.members.values())
        for member in members[::-1]:
            stack.append(member)
            depth_stack.append(curr_depth + 1)


def isprivate(doc):
    name = doc.fullname.rsplit(".")[-1]
    return name[0] == "_"


if __name__ == "__main__":
    main()
