import r2pipe
import subprocess
#------------------------------------------------------------------------------------
def write_assemble(r2, memory_address, assembly_code):
    r2.cmd(f"s {memory_address}")
    r2.cmd(f"wa {assembly_code}")
#------------------------------------------------------------------------------------
def read_memory_content(binary_path, memory_address, num_bytes):
    r2 = r2pipe.open(binary_path)

    # Set the bin.cache flag to true
    r2.cmd("-e bin.cache=true")

    # Read the original memory content at the specified address
    r2.cmd(f"s {memory_address}")
    original_memory_content = r2.cmd(f"px {num_bytes}")

    # Seek to the memory address again after the update
    r2.cmd(f"s {memory_address}")
    updated_memory_content = r2.cmd(f"px {num_bytes}")

    # Use `pd` command to disassemble the updated memory content
    r2.cmd(f"s {memory_address}")
    disassembly = r2.cmd(f"pd {num_bytes}")

    # Close Radare2
    r2.quit()

    return original_memory_content, updated_memory_content, disassembly
#------------------------------------------------------------------------------------
def execute_binary(binary_path):
    try:
        # Use subprocess.run() to execute the binary
        subprocess.run([binary_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the binary: {e}")
    except FileNotFoundError:
        print("Binary not found. Please provide the correct path to the binary.")
#------------------------------------------------------------------------------------
def exploit():
    binary_path = 'path_to_binary'
    memory_address = '0x00000539'
    num_bytes = 16

    print(50 * '-')
    print('Welcome to Wonderful Exploiter!')
    print(50 * '-')

    # Take user input for varc and convert it to an integer
    varc = int(input('How many times do you want to print out the word wonderful?: '))

    # Convert varc to its hexadecimal representation
    hex_varc = hex(varc)

    # Pass hex_varc as an additional argument to read_memory_content function
    original_memory_content, updated_memory_content, disassembly = read_memory_content(binary_path, memory_address, num_bytes)

    print(50 * '-')
    print("Original Memory Content:")
    print(original_memory_content)
    print(50 * '-')

    print("Disassembly:")
    print(disassembly)
    print(50 * '-')

    # Reopen Radare2 in write mode
    r2 = r2pipe.open(binary_path, flags=["-w"])

    # Use the `write_assemble` function to update the memory address with the new assembly code
    # For example, if you want to change the `mov ebx, 8` to `mov ebx, {varc}`
    assembly_code = f"mov ebx, {hex_varc}"
    write_assemble(r2, memory_address, assembly_code)

    # Close Radare2
    r2.quit()
#------------------------------------------------------------------------------------
def post():
    # Here we are going to check the assembly again 
    binary_path = 'path_to_binary'
    memory_address = '0x00000539'
    num_bytes = 16
    original_memory_content, updated_memory_content, disassembly = read_memory_content(binary_path, memory_address, num_bytes)
    print(50 * '-')
    print("Modified Memory Content:")
    print(original_memory_content)
    print(50 * '-')

    print("Modified Disassembly:")
    print(disassembly)
    print(50 * '-')
    input('Press any key to execute the program: ')
    print(50 * '-')
    execute_binary(binary_path)
    print(50 * '-')
    print('Binary modified!')
    print(50 * '-')
    exit()
#------------------------------------------------------------------------------------
exploit()
post()
#------------------------------------------------------------------------------------