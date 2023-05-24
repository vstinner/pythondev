import sys
import stdlib_list

def get(version):
    names = stdlib_list.stdlib_list(version)
    modules = set(
        name.split('.')[0]
        for name in names)
    return modules

old=get('3.9')
new=get('3.10')
#new=sys.stdlib_module_names #get('3.10')
print(len(old), len(new))
print()

def public(names):
    names = set(name for name in names if not name.startswith('_'))
    names -= {'xxlimited', 'xxsubtype'}
    return names

new = public(new)
old = public(old)

diff = new - old
print(f"Added ({len(diff)}):")
for name in sorted(diff):
    print(f"* {name}")
print()

diff = old - new
print(f"Removed ({len(diff)}):")
for name in sorted(diff):
    print(f"* {name}")
print()
