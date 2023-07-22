import argparse


# By default, the `const` parameter to argparse.ArgumentParser.add_argument()
# only supports `nargs="?"`; it does not natively support `nargs="*"`; however,
# we can use a custom action to achieve this behavior (source:
# <https://stackoverflow.com/a/72803343/560642>)
class constForNargsStar(argparse.Action):
    """
    Customized argparse action, will set the
    value in the following way:

        1) If no option_string is supplied: set to None

        2) If option_string is supplied:

            2A) If values are supplied:
                set to list of values

            2B) If no values are supplied:
                set to default value (`self.const`)

    NOTES:
        If `const` is not set, default value (2A) will be None
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if option_string:
            setattr(namespace, self.dest, self.const)
        elif not values:
            setattr(namespace, self.dest, None)
        else:
            setattr(namespace, self.dest, values)
