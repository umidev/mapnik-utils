import compile, style
from compile import compile
from style import stylesheet_declarations

def load_map(map, input, dir=None):
    """
    """
    compile(input, dir).to_mapnik(map)
