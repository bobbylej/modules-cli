from javascript import require
import json

madge = require("madge")
JSON = require("./js/json.js")


def get_files_dependencies(path, config=None):
    """
    Gets dependencies of files in the specified path(s). It is using javascript package called madge (https://github.com/pahen/madge).

    Args:
        path (str | list[str]): A string or list of strings representing the path to the files or directories for which the dependencies need to be calculated.
        config (dict): A dictionary containing configuration options. List of options can be found here: https://github.com/pahen/madge#configuration.
        
    Returns:
        (Dict[str, Set[str]]): A dictionary mapping filenames to sets of dependent filenames.
    """
    config = {key: value for key, value in config.items() if value is not None}
    res = madge(path, config)
    return json.loads(JSON.stringify(res.obj()))
