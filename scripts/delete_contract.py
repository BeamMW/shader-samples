import os
import sys
from shutil import rmtree

def print_usage():
    print('Usage: %s %s contract_name' % (sys.executable, sys.argv[0]))

if len(sys.argv) != 2:
    print_usage()
    sys.exit(1)

contract_name = sys.argv[1]
shader_name = contract_name + 'Shader'

f = open(os.path.join('shaders', 'CMakeLists.txt'), 'r')
txt = f.read()
f.close()
if txt.find(shader_name) == -1:
    print('Error: Shader %s doesn\'t exist!' % shader_name)
    sys.exit(1)
else:
    f = open(os.path.join('shaders', 'CMakeLists.txt'), 'w')
    f.write(txt.replace('add_subdirectory(%s)\n' % shader_name, ''))
    f.close()

rmtree(os.path.join('shaders', shader_name))
print('Shader %s deleted successfully!' % shader_name)
