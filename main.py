import importlib
import sys
import pdoc
import pdoc.doc
import pdoc.docstrings


def main():
    mod_name = sys.argv[1]
    mod = importlib.import_module(mod_name)
    doc = pdoc.doc.Module(mod)
    # crawl_recursive(doc)
    crawl(doc)


def crawl(doc):
    stack = [doc]
    depth_stack = [0]

    while len(stack) > 0:
        curr_doc = stack.pop(-1)
        curr_depth = depth_stack.pop(-1)

        if not is_private(curr_doc):
            render_markdown(curr_doc, curr_depth)

        if not isinstance(curr_doc, pdoc.doc.Namespace):
            continue

        members = list(curr_doc.own_members)
        for member in members[::-1]:
            stack.append(member)
            depth_stack.append(curr_depth + 1)


def render_markdown(doc, depth):
    print(f"{"#" * (depth + 1)} {doc.name}")
    if isinstance(doc, pdoc.doc.Function):
        print("```python")

        for decorator in doc.decorators:
            print(f"{decorator}")

        print(f"{doc.funcdef} {doc.name}{doc.signature}:")
        print("```")
    elif isinstance(doc, pdoc.doc.Class):
        print("```python")

        definition = f"class {doc.name}"

        if len(doc.bases) > 0:
            definition += f"({", ".join([base[2] for base in doc.bases])})"

        definition += ":"

        print(definition)
        print("```")
    elif isinstance(doc, pdoc.doc.Variable):
        ...

    formatted_docstring = pdoc.docstrings.google(doc.docstring)
    print(formatted_docstring)
    print("\n---")


def is_private(doc):
    name = doc.fullname.rsplit(".")[-1]
    return name[0] == "_"


if __name__ == "__main__":
    main()
