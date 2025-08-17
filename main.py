import importlib
import sys
import pdoc
import pdoc.doc
import pdoc.docstrings


def main():
    mod_name = sys.argv[1]
    mod = importlib.import_module(mod_name)
    mod_doc = pdoc.doc.Module(mod)
    # crawl_recursive(doc)
    print(f"---\ntitle: {mod_doc.name}\n---\n")
    crawl(mod_doc)


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
    if depth == 1:
        print("\n---")

    if isinstance(doc, pdoc.doc.Function):
        print(f"{"##" * depth} {doc.name}")
        print("```python")

        for decorator in doc.decorators:
            print(f"{decorator}")

        print(f"{doc.funcdef} {doc.name}{doc.signature}:")
        print("```")
    elif isinstance(doc, pdoc.doc.Class):
        print(f"{"##" * depth} {doc.name}")
        print("```python")

        definition = f"class {doc.name}"

        if len(doc.bases) > 0:
            definition += f"({", ".join([base[2] for base in doc.bases])})"

        definition += ":"

        print(definition)
        print("```")
    elif isinstance(doc, pdoc.doc.Variable):
        print(f"{"##" * depth} {doc.name}")
        print("```python")

        definition = f"{doc.name}{doc.annotation_str}"
        default = doc.default_value_str
        if default:
            definition += f" = {default}"
        print(definition)

        print("```")

    formatted_docstring = pdoc.docstrings.google(doc.docstring)
    print(formatted_docstring)

def is_private(doc):
    name = doc.fullname.rsplit(".")[-1]
    return name[0] == "_"


if __name__ == "__main__":
    main()
