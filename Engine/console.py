# console.py
class ConsoleWindow:
    def __init__(self, command_receiver):
        self.command_receiver = command_receiver

    def open(self):
        print("=== MiniPyEngine Console Menu ===")
        print("[WARNING] Avoid closing the game while console is open. Type 'help'.")
        while True:
            try:
                cmd = input(">>> ")
            except Exception as e:
                print(f"[ERROR] Console is crashed: {e}")
                break

            if cmd.strip() == "":
                continue
            if cmd.lower() == "exit":
                print("[INFO] Console is closed")
                break
            if cmd.lower() == "help":
                print("Type 'god' to enable God Mode (health set to 9999).")
                print("Type 'noclip' to pass through walls freely.")
                print("Type 'nocrouch' to disable crouching.")
                print("Type 'nojump' to disable jumping.")
                print("Type 'exit' to close the console.")
                continue
            try:
                self.command_receiver(cmd)
            except Exception as e:
                print(f"[ERROR] Unknown command error: {e}")
