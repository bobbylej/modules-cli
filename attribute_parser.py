import argparse


def get_command_attributes():
    """
    Parses command-line arguments and returns an `argparse.Namespace` object containing the parsed arguments.

    Parameters:
      None

    Returns:
      An `argparse.Namespace` object containing the parsed arguments.
    """

    # Create the argument parser
    parser = argparse.ArgumentParser()

    # Add the arguments you want to parse
    parser.add_argument("--files", nargs="+", help="Array with paths to files")
    parser.add_argument(
        "--exclude", nargs="+", help="Array of RegExp for excluding modules"
    )
    parser.add_argument(
        "--ts-config",
        nargs="+",
        help="TypeScript config for resolving aliased modules - a path to a tsconfig file",
    )
    parser.add_argument(
        "--webpack-config",
        nargs="+",
        help="Webpack config for resolving aliased modules - a path to a webpack config file",
    )
    parser.add_argument(
        "--require-config",
        nargs="+",
        help="RequireJS config for resolving aliased modules - a path to a require config file",
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        help="Array of valid file extensions used to find files in directories",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Print the arguments
    print("Args:", args)

    return args
