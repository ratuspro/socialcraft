from . import core


def print_context(context: core.Context):
    ordered = {}

    for perception in context.get_perceptions():
        if perception.name not in ordered.keys():
            ordered[perception.name] = []
        ordered[perception.name].append(perception.value)

    for ps_name, ps_value in ordered.items():
        if len(ps_value) == 1:
            print(f"{ps_name} = {ps_value}")
        else:
            print(ps_name)
            for value in ps_value:
                print(" - " + value)
