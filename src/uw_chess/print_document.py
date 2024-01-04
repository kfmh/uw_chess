# ============================================================================
# print_document.py
# 
# ============================================================================

from .runtime_test import LogExecutionTime
import os


class Create_Document:
    def __init__(self, title="stt_doc"):
        self.file         = f"./print_documents/{title}.txt"
        self.string_obj   = ""

    def clear_screen(self):
        clear = os.system('cls' if os.name == 'nt' else 'clear')
        return clear

    def document(self, words:str, flushing:bool = False, cli_print:bool = True, ):
        self.clear_screen()
        if cli_print:
            if flushing:
                self.string_obj += f"[ {words}]"
                print(self.string_obj)
            else:
                print(self.string_obj + words)
                
        

