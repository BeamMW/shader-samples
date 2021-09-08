import os
import sys

def print_usage():
    print('Usage: %s %s contract_name' % (sys.executable, sys.argv[0]))

if len(sys.argv) != 2:
    print_usage()
    sys.exit(1)

contract_name = sys.argv[1]
shader_name = contract_name + 'Shader'

try:
    os.mkdir(os.path.join('shaders', shader_name))
except FileExistsError:
    print('Error: Contract %s already exists!' % contract_name)
    sys.exit(1)

with open(os.path.join('shaders', 'CMakeLists.txt'), 'a') as f:
    f.write('add_subdirectory(%s)\n' % shader_name)

for i in os.listdir(os.path.join('samples', 'Initial')):
    f = open(os.path.join('samples', 'Initial', i), 'r')
    txt = f.read()
    f.close()
    f = open(os.path.join('shaders', shader_name, i), 'w')
    f.write(txt.replace('_INITIAL_CONTRACT_', contract_name))
    f.close()

print('Shader %s created successfully!' % shader_name)
