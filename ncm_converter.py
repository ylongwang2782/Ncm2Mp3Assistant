import sys
import os
from ncmdump import dump

def convert_file(input_file, output_file):
    try:
        dump(input_file, output_file)
        print("success")
    except Exception as e:
        print(f"error:{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("error:Invalid arguments")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print("error:Input file does not exist")
        sys.exit(1)
    
    convert_file(input_file, output_file) 