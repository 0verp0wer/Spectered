import os
import re

from pystyle import Center, Anime, Colors, Colorate, System, Write


banner = '''
 $$$$$$\                                  $$\                                         $$\ 
$$  __$$\                                 $$ |                                        $$ |
$$ /  \__| $$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$ |
\$$$$$$\  $$  __$$\ $$  __$$\ $$  _____|\_$$  _|  $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$ |
 \____$$\ $$ /  $$ |$$$$$$$$ |$$ /        $$ |    $$$$$$$$ |$$ |  \__|$$$$$$$$ |$$ /  $$ |
$$\   $$ |$$ |  $$ |$$   ____|$$ |        $$ |$$\ $$   ____|$$ |      $$   ____|$$ |  $$ |
\$$$$$$  |$$$$$$$  |\$$$$$$$\ \$$$$$$$\   \$$$$  |\$$$$$$$\ $$ |      \$$$$$$$\ \$$$$$$$ |
 \______/ $$  ____/  \_______| \_______|   \____/  \_______|\__|       \_______| \_______|
          $$ |                                                                            
          $$ |                                                                            
          \__|          
'''[1:]

text = '''                                                                                                 
 .M"""bgd                             mm                                `7MM  
,MI    "Y                             MM                                  MM  
`MMb.   `7MMpdMAo.  .gP"Ya   ,p6"bo mmMMmm .gP"Ya `7Mb,od8 .gP"Ya    ,M""bMM  
  `YMMNq. MM   `Wb ,M'   Yb 6M'  OO   MM  ,M'   Yb  MM' "',M'   Yb ,AP    MM  
.     `MM MM    M8 8M"""""" 8M        MM  8M""""""  MM    8M"""""" 8MI    MM  
Mb     dM MM   ,AP YM.    , YM.    ,  MM  YM.    ,  MM    YM.    , `Mb    MM  
P"Ybmmd"  MMbmmd'   `Mbmmd'  YMbmd'   `Mbmo`Mbmmd'.JMML.   `Mbmmd'  `Wbmd"MML.
          MM                                                                  
        .JMML.   
                    a Specter deobfuscator
'''[1:]

System.Clear()
System.Title("Spectered by ꧁𝕆𝕧𝕖𝕣𝕡𝕠𝕨𝕖𝕣༄꧂#2524")
System.Size(140, 45)
Anime.Fade(Center.Center(banner), Colors.red_to_yellow, Colorate.Vertical, enter=True)
System.Size(130, 30)
print(Colorate.Diagonal(Colors.red_to_yellow, Center.XCenter(text)))

def deobfuscate(a: list, k: int) -> str:
    return ''.join(''.join(chr(int(c)-k) for c in b.split('\\x00') if c) for b in a)


file = Write.Input("Insert the file name:", Colors.red_to_yellow, interval=0.005)
output_set = set()

with open(file, "r") as f:
    content = f.read()
    f.seek(0)
    for line in f:
        match = re.search(r"__(\d+)__", line)
        if match:
            output_set.add(match.group(0))

output_str = ''
with open(file, "r") as f:
    for line in f:
        for output in output_set:
            if output in line:
                output_str += output + '[1]+'
                break

output_str = output_str[:-13]
space = " "*500

with open(file, "w") as f:
    content = content.replace(f"    Specter(__code__){space},exec(__import__('marshal').loads({output_str}),globals())", f"""
    import struct
    import sys
    import marshal

    def code_to_bytecode(code):
        def uint32(val):
            return struct.pack("<I", val)
    
        if sys.version_info >= (3,4):
            from importlib.util import MAGIC_NUMBER

        data = bytearray(MAGIC_NUMBER)
        if sys.version_info >= (3,7):
            data.extend(uint32(0))

        data.extend(uint32(int(0)))

        if sys.version_info >= (3,2):
            data.extend(uint32(0))

        data.extend(marshal.dumps(code))
        return data
    
    with open("temp.pyc", "wb") as f:
        f.write(code_to_bytecode(marshal.loads({output_str})))""")
    f.write(content)

os.system(f"py {file}")
os.system("pycdas.exe temp.pyc > dis.txt")

with open("dis.txt", "r") as dis:
    content = dis.read()

    values = re.findall(r"b'([3-9]|[12][0-9]|3[0-3])'(?!\d)", content)

    for value in values:
        key = value

    values = re.findall(r"(?:LOAD_CONST|LOAD_NAME)\s*?(?:\d.*?): (?:b|globals)(.*)", content)[1:]

    keys = re.findall(r"STORE_NAME\s*?(?:\d*?): (__.*?__)", content)[:-1]

    order = re.findall(r"LOAD_NAME\s*?(?:\d*?): (__.*?__)", content)

    unordered = {}
    for i in range(len(values)):
        unordered[keys[i]] = values[i]

    ordered = []
    for i in range(len(order)):
        ordered.append(unordered[order[i]].replace("'", ""))

    with open("out.py", 'w', encoding="utf-8") as f:
        f.write(deobfuscate(ordered, int(key)).replace("\r", ""))

Write.Print("Done...", Colors.red_to_yellow, interval=0.005)

os.remove("dis.txt")
os.remove("temp.pyc")