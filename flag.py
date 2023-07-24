import r2pipe

def script_in_debug_mode(binary_path):
    r2 = r2pipe.open(binary_path, flags=["-d"])  # Open Radare2 in debug mode

    # Wait for Radare2 to finish loading the binary and symbols
    r2.cmd("doo")

    # Set a breakpoint at the main function
    r2.cmd("db main")

    # Run the binary until the breakpoint is hit
    r2.cmd("dc")

    # Continue execution until the breakpoint at address 0x0040119a is hit
    r2.cmd("db 0x0040119a")
    r2.cmd("dc")

    # Analyze all functions to ensure accurate disassembly
    r2.cmd("aa")

    # Run afvd var_8h command to define the variable var_8h
    r2.cmd("afvd var_8h")

    # Use the `pf S @ rbp-8` command to print the flag
    flag_value = r2.cmd("pf S @ rbp-8")
    print(f"The flag is: {flag_value}")

    # Quit Radare2
    r2.quit()

if __name__ == "__main__":
    binary_path = "path_to_binary"  # Replace this with the actual path to the binary
    script_in_debug_mode(binary_path)
