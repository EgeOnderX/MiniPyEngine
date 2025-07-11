import pygame
class Config:
    def __init__(self) -> None:
        self.server_ip = "127.0.0.1"
        self.server_port = 7532
        self.screen_width = 1920
        self.screen_height = 1080
        self.sensitivity = 20

        self.config_filename = "config"

        self.read_config()

    def read_config(self):
        with open(self.config_filename, "r") as f:
            for line in f.readlines():
                tokens = line.split(":")

                if tokens[0] == "server-ip":
                    self.verify_type(str, tokens[0], tokens[1])
                    self.server_ip = tokens[1].rstrip("\n")
                elif tokens[0] == "server-port":
                    self.verify_type(int, tokens[0], tokens[1])
                    self.server_port = int(tokens[1])
                elif tokens[0] == "screen-width":
                    self.verify_type(int, tokens[0], tokens[1])
                    self.screen_width = int(tokens[1])
                elif tokens[0] == "screen-height":
                    self.verify_type(int, tokens[0], tokens[1])
                    self.screen_height = int(tokens[1])
                elif tokens[0] == "sensitivity":
                    self.verify_type(int, tokens[0], tokens[1])
                    self.sensitivity = int(tokens[1])
    
    def verify_type(self, var_type, *tokens):
        try:
            var_type(tokens[1])
        except ValueError as ex:
            print("CONFIG-ERROR: field '%s' is not of type %s" % (tokens[0], str(var_type)))
            exit()
        except Exception as ex:
            print("CONFIG-ERROR: Unkown error occured with field '%s': %s" % (tokens[0], ex.with_traceback()))
            exit()
