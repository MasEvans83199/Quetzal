def run_quetzal_code(code):
    # This function would interface with your interpreter
    # Placeholder for actual interpreter call
    return "Output from running code"

def quetzal_shell():
    print("Welcome to the Quetzal interactive shell. Type 'exit' to exit.")
    while True:
        try:
            code = input("quetzal> ")
            if code.lower() == "exit":
                break
            output = run_quetzal_code(code)
            print(output)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    quetzal_shell()
